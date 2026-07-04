"""slice 3b · 第二跑 — does the NPC really catch the snow/night?

frostgate_watchpost with world_premise declaring climate=寒带 + opening_weather=雪 +
opening_time=夜里 (declarative switches only — the committed fixture stays
byte-identical; we inject into an in-memory copy and load that). NO engine/other-pack
change.

We talk to the sentry (哨兵伏斯) and captain (队长布兰) for several rounds in the
snowy night (questions / chitchat / a plea) and capture their VERBATIM replies —
the core judgement is whether the reply naturally mentions THIS snow / THIS late
night (slice 3b feeds 「此刻是夜里，下着雪。」into the dialogue prompt), or is still a
template line unrelated to the moment.

Then we /skip to cross a time-of-day boundary (夜→晨) and to drive a weather change,
collecting every Narration event VERBATIM — the ambient transition line ("天黑了" /
"天气变了，下着雪。") must surface, at most one time line + one weather line per tick,
not spammy.

Real MiniMax. Per-tick 90s watchdog + 55s socket timeout. Natural language for
moves/dialogue (no /inject).
"""
from __future__ import annotations
import os, sys, time, json, logging, threading, tempfile
from pathlib import Path

ROOT = Path("/Users/gensliu/Documents/rpg")
os.chdir(ROOT); sys.path.insert(0, str(ROOT / "src"))
for raw in (ROOT / ".env").read_text().splitlines():
    line = raw.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip("'\""))

import verisaria.protocol as P
from verisaria.protocol.engine_session import EngineSession
from verisaria.engine.npc_dialogue import NPCDialogueGenerator

def when_phrase(state):
    return NPCDialogueGenerator._when_phrase(state)

OUTDIR = ROOT / "reports" / "worldclock_weather_test_second_run"
OUTDIR.mkdir(parents=True, exist_ok=True)
LOGFILE = str(OUTDIR / "run.log")
RAWOUT = OUTDIR / "raw_ticks.txt"
SRC_PACK = ROOT / "fixtures" / "content_packs" / "frostgate_watchpost.json"
PER_TICK_TIMEOUT = float(os.environ.get("PQ_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("PQ_SOCK_TIMEOUT", "55"))

# --- declarative world_premise switches only (authorized) ---
pack = json.loads(SRC_PACK.read_text())
pack["world_premise"]["climate"] = "寒带"
pack["world_premise"]["opening_weather"] = "雪"
# NB: the engine's named-opening vocabulary (worldclock._NAMED_OPENINGS) doesn't
# include the bare phase word "夜里"; "深夜"=01:00 lands squarely in the 夜 phase
# (time_phrase → "夜里"), giving exactly the intended snowy-night state without
# touching engine code. Still a declarative world_premise switch only.
pack["world_premise"]["opening_time"] = "深夜"
tmp = Path(tempfile.mkdtemp()) / "frostgate_3b.json"
tmp.write_text(json.dumps(pack, ensure_ascii=False))
PACK = str(tmp)

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== worldclock slice-3b second run (frostgate, 寒带/雪/夜里) ===")

out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""): out.write(s + "\n"); out.flush()

PLAYER = "player_001"
LOCNAMES = {"gatehouse": "门楼", "barracks": "兵营", "refugee_camp": "难民营"}

narration_log = []      # (tick, text)
npc_lines = []          # (tick, name, line)
fallbacks = 0
timeouts = 0
fallback_reasons = []

def ploc(s): return s.game.world.state.get_entity(PLAYER).location_id

def _watch(fn):
    res = {"v": None, "exc": None, "done": False}
    def _w():
        try: res["v"] = fn()
        except Exception:
            import traceback; res["exc"] = traceback.format_exc()
        finally: res["done"] = True
    t0 = time.time(); w = threading.Thread(target=_w, daemon=True)
    w.start(); w.join(PER_TICK_TIMEOUT); dt = time.time() - t0
    return res, dt

def header(s, snap, dt):
    log(f"  tick={snap.tick} pacing={snap.pacing} | {snap.time_of_day} {snap.clock} | 天气 {snap.weather} | {dt:.1f}s")
    log(f"  player@{LOCNAMES.get(ploc(s),ploc(s))}")

def scan_events(tr, snap):
    global fallbacks
    for ev in tr.events:
        if isinstance(ev, P.Narration):
            log(f"  ☁ NARRATION: {ev.text.strip()}")
            narration_log.append((snap.tick, ev.text.strip()))
        elif isinstance(ev, P.NpcSpoke):
            log(f"  💬 {ev.name}: {ev.line.strip()}")
            npc_lines.append((snap.tick, ev.name, ev.line.strip()))
        elif isinstance(ev, P.NpcMoved):
            nm = ev.name or ev.npc_id
            log(f"  ★NPC_MOVED {nm}: {LOCNAMES.get(ev.from_loc,ev.from_loc)} -> {LOCNAMES.get(ev.to_loc,ev.to_loc)}")
        elif isinstance(ev, P.PlayerMoved):
            log(f"  PLAYER_MOVED -> {LOCNAMES.get(ev.to_loc,ev.to_loc)}")
        else:
            cls = type(ev).__name__
            txt = getattr(ev, "text", "") or getattr(ev, "summary", "")
            if cls.upper().find("FALLBACK") >= 0 or "FALLBACK" in str(txt).upper():
                fallbacks += 1
                fallback_reasons.append(str(txt)[:160])
                log(f"  !!FALLBACK {cls}: {txt}")

def run_nl(s, text, label=""):
    global timeouts
    log("\n" + "=" * 78); log(f">>> {label or text}")
    res, dt = _watch(lambda: s.submit(P.SubmitInput(text=text)))
    if not res["done"]:
        log(f"!! TICK WATCHDOG TIMEOUT {dt:.1f}s"); timeouts += 1; return None
    if res["exc"]: log("!! EXC\n" + res["exc"]); return None
    tr = res["v"]; snap = tr.snapshot
    header(s, snap, dt)
    scan_events(tr, snap)
    # surface any free-form narrative the engine returned (the immediate prose)
    for attr in ("narration", "narrative", "text"):
        v = getattr(tr, attr, None)
        if isinstance(v, str) and v.strip():
            log(f"  [tr.{attr}] {v.strip()[:300]}")
    return tr

def run_skip(s, label="/skip"):
    global timeouts
    log("\n" + "=" * 78); log(f">>> {label}  (player@{LOCNAMES.get(ploc(s),ploc(s))})")
    before = s.game.world.state.clock_minutes
    phase_b = s.snapshot().time_of_day; wx_b = s.snapshot().weather
    s._buffer.clear()  # /skip emits to the EngineSession buffer (game._event_sink)
    res, dt = _watch(lambda: s.game._handle_command("/skip"))
    if not res["done"]:
        log(f"!! TICK WATCHDOG TIMEOUT {dt:.1f}s"); timeouts += 1; return None
    if res["exc"]: log("!! EXC\n" + res["exc"]); return None
    ret = res["v"]; snap = s.snapshot()
    log(f"  skip_ret: {str(ret).strip()[:140]}")
    header(s, snap, dt)
    log(f"  Δclock={snap.clock_minutes if hasattr(snap,'clock_minutes') else '?'} "
        f"phase {phase_b}->{snap.time_of_day}  weather {wx_b}->{snap.weather}")
    # /skip path buffers events on the session; drain via the engine event buffer
    drained = _drain_events(s)
    for ev in drained:
        if isinstance(ev, P.Narration):
            log(f"  ☁ NARRATION: {ev.text.strip()}")
            narration_log.append((snap.tick, ev.text.strip()))
        elif isinstance(ev, P.NpcMoved):
            nm = ev.name or ev.npc_id
            log(f"  ★NPC_MOVED {nm}: {LOCNAMES.get(ev.from_loc,ev.from_loc)} -> {LOCNAMES.get(ev.to_loc,ev.to_loc)}")
    return snap

def _drain_events(s):
    """Pull protocol events the /skip tick emitted to the EngineSession buffer
    (game._event_sink == s._buffer.append)."""
    evs = list(getattr(s, "_buffer", []))
    try: s._buffer.clear()
    except Exception: pass
    return evs

def main():
    log(f"=== 3b SECOND RUN (frostgate 寒带/雪/夜里) tick_to={PER_TICK_TIMEOUT}s ===")
    s = EngineSession.start(PACK, save_dir="_wc_3b", llm_backend="minimax")
    try: s.game.llm_provider.timeout = SOCK_TIMEOUT
    except Exception as e: log(f"(provider timeout set fail: {e})")
    snap = s.snapshot()
    log(f"START {snap.time_of_day} {snap.clock} 天气 {snap.weather}")
    log(f"  (clock_minutes={s.game.world.state.clock_minutes})")

    # confirm slice 3b prompt content: the exact env line the NPC dialogue prompt gets
    log(f"  when_phrase (slice-3b prompt env line) = {when_phrase(s.game.world.state)!r}")

    # ---- PHASE 1: talk to sentry/captain in the snowy night, several rounds ----
    log("\n----- PHASE 1: 雪夜里对哨兵/队长连说几轮 -----")
    # Address NPCs by name so the engine doesn't ask "你指谁?" — natural language,
    # one explicit target per line (no /talk, no /inject).
    turns = [
        ("我问哨兵伏斯：城外那些难民，在这天气里还撑得住吗？", "问哨兵(引天气)"),
        ("我对哨兵伏斯说：这么晚了，你还守在这门楼上啊。", "对哨兵闲聊(引深夜)"),
        ("我问哨兵伏斯：你守了几年了，这里每年冬天都这么冷吗？", "问哨兵(冬寒)"),
        ("我对哨兵伏斯说：城外那些人快冻死了，求你帮忙跟队长说说，开门放他们进来吧。", "对哨兵求情"),
        ("我问队长布兰：下这么大雪，山都封了，补给还能翻过来吗？", "问队长(雪封山)"),
        ("我对队长布兰说：这么深的夜还得值守，你们也不好过吧。", "对队长闲聊(深夜值守)"),
    ]
    for text, lbl in turns:
        run_nl(s, text, label=lbl)
        if timeouts >= 4: break

    # ---- PHASE 2: /skip to cross 夜→晨 + drive a weather change ----
    # The player must be alone for FAST /skip; step out to the (empty) barracks.
    log("\n----- PHASE 2: 独处快进，跨时段(夜→晨)并触发天气变化，收过渡Narration -----")
    run_nl(s, "我离开门楼，去兵营。", label="去兵营(独处以放行/skip)")
    for i in range(10):
        snap = run_skip(s, label=f"/skip #{i+1}")
        if snap is None:
            if timeouts >= 4: break
            continue
        # stop once we've crossed into morning AND seen at least one transition narration
        if s.game.world.state.clock_minutes >= 24*60 + 6*60:  # next-day ~06:00
            break
        if timeouts >= 4: break

    # ---- PHASE 3: one more dialogue round in the new (morning) light to contrast ----
    log("\n----- PHASE 3: 次日清晨回门楼，再对哨兵说一句作对照 -----")
    run_nl(s, "我回到门楼。", label="回门楼")
    log(f"  when_phrase now = {when_phrase(s.game.world.state)!r}")
    run_nl(s, "我问哨兵伏斯：天亮了，昨晚的雪好像小了些，你们换岗了吗？", label="清晨对照(引晨/雪变)")

    # ---- SUMMARY ----
    log("\n" + "#" * 78)
    log("# SUMMARY")
    log("#" * 78)
    log(f"\nNPC 对白原话 (共 {len(npc_lines)} 条):")
    for tk, nm, ln in npc_lines:
        log(f"   [t{tk}] {nm}: {ln}")
    log(f"\n过渡 Narration (共 {len(narration_log)} 条):")
    for tk, tx in narration_log:
        log(f"   [t{tk}] {tx}")
    log(f"\nFALLBACK={fallbacks}  tick_timeouts={timeouts}")
    if fallback_reasons:
        log("fallback reasons:")
        for r in fallback_reasons: log(f"   - {r}")
    out.close()
    print(f"DONE npc_lines={len(npc_lines)} narrations={len(narration_log)} "
          f"FALLBACK={fallbacks} timeouts={timeouts}")

if __name__ == "__main__":
    main()
