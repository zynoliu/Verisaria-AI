"""Scenario 2 — escort/negotiation regression (MOST CRITICAL).

Reuses the EXACT proving-chain play that got stamped in
reports/prereq_convergence_test_fourth_run (escort Anya → testimony → warden opens
sluice), driving escort_proving_ground.json.

  --flag off : run with npc_daily_rhythm OFF (committed pack, default). Must close
               the chain exactly as last stamped (escort ⟳MOVED →
               anya_testimony_given ⟳FLIP → sluice_opened ⟳FLIP). Zero regression.
  --flag on  : same pack with npc_daily_rhythm=true injected in-memory. Watch
               whether daytime NPC wandering drags the negotiation — the key check
               is that a NAMED/in-conversation NPC does NOT wander off
               (in_conversation priority); only idle bystanders move.

The committed fixture stays byte-identical (flag is injected into an in-memory
copy for --flag on). Real MiniMax. 90s/tick watchdog + 55s socket. Natural
language only, never /inject. Adds snapshot time_of_day/clock/weather + NpcMoved
logging on top of the stamped play.
"""
from __future__ import annotations
import os, sys, time, json, logging, threading, tempfile, argparse
from pathlib import Path

ROOT = Path("/Users/gensliu/Documents/rpg")
os.chdir(ROOT); sys.path.insert(0, str(ROOT / "src"))
for raw in (ROOT / ".env").read_text().splitlines():
    line = raw.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip("'\""))

import verisaria.protocol as P
from verisaria.runtime.session import GameSession

PLAYER = "player_001"; ANYA = "npc.miller_anya"; WARDEN = "npc.warden_kang"
NAMES = {ANYA: "磨坊主安雅", WARDEN: "闸官老康"}
LOCNAMES = {"gatehouse": "闸房", "yard": "院子"}
OUTDIR = ROOT / "reports" / "worldclock_weather_test"
OUTDIR.mkdir(parents=True, exist_ok=True)
SRC_PACK = ROOT / "fixtures" / "content_packs" / "escort_proving_ground.json"
PER_TICK_TIMEOUT = float(os.environ.get("PQ_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("PQ_SOCK_TIMEOUT", "55"))

ap = argparse.ArgumentParser()
ap.add_argument("--flag", choices=["on", "off"], required=True)
args = ap.parse_args()
FLAG_ON = args.flag == "on"
TAG = "flagon" if FLAG_ON else "flagoff"
LOGFILE = str(OUTDIR / f"regression_{TAG}.log")
RAWOUT = OUTDIR / f"regression_{TAG}_raw.txt"

if FLAG_ON:
    pack = json.loads(SRC_PACK.read_text())
    pack["world_premise"]["npc_daily_rhythm"] = True
    tmp = Path(tempfile.mkdtemp()) / "escort_flagon.json"
    tmp.write_text(json.dumps(pack, ensure_ascii=False))
    PACK = str(tmp)
else:
    PACK = str(SRC_PACK)

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== escort regression log (rhythm=%s) ===", "ON" if FLAG_ON else "OFF")

out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""): out.write(s + "\n"); out.flush()

fallbacks = 0; timeouts = 0
npcmoved_events = []  # (tick, name, from, to)

def loc(s, eid):
    e = s.world.state.get_entity(eid); return e.location_id if e else None
def present(s):
    p = loc(s, PLAYER)
    return [eid for eid, e in s.world.state.entities.items() if eid != PLAYER and e.location_id == p]
def wv(s, k): return s.world.state.world_vars.get(k)

def run(s, action):
    global timeouts, fallbacks
    st = s.world.state
    log("\n" + "=" * 78); log(f">>> {action!r}")
    log(f"pre:  tick={st.tick} loc={LOCNAMES.get(loc(s,PLAYER),loc(s,PLAYER))} present={[NAMES.get(e,e) for e in present(s)]}")
    log(f"      world={dict(st.world_vars)}")
    events = []; s._event_sink = events.append
    res = {"narr": None, "exc": None, "done": False}
    def _work():
        try: res["narr"] = s.run_tick(action)
        except Exception:
            import traceback; res["exc"] = traceback.format_exc()
        finally: res["done"] = True
    t0 = time.time(); w = threading.Thread(target=_work, daemon=True)
    w.start(); w.join(PER_TICK_TIMEOUT); dt = time.time() - t0
    if not res["done"]:
        log(f"!! TICK WATCHDOG TIMEOUT {dt:.1f}s — ABANDON"); lg.warning("TIMEOUT %r %.1fs", action, dt)
        timeouts += 1; s._event_sink = None; return True
    s._event_sink = None
    if res["exc"]: log("!! EXC\n" + res["exc"])
    st = s.world.state
    # snapshot fields via worldclock/weather (no EngineSession here; derive directly)
    from verisaria.engine import worldclock as _wc, weather as _wx
    cm = getattr(st, "clock_minutes", 0)
    tod = _wc.time_of_day(cm).label; clk = _wc.clock_label(cm)
    wxlabel = _wx.weather_label(st.weather) if getattr(st, "weather", "") else ""
    log(f"post: tick={st.tick} loc={LOCNAMES.get(loc(s,PLAYER),loc(s,PLAYER))} | {tod} {clk} | 天气 {wxlabel} | {dt:.1f}s")
    log(f"      world={dict(st.world_vars)}")
    log(f"      安雅@{LOCNAMES.get(loc(s,ANYA),loc(s,ANYA))}  老康@{LOCNAMES.get(loc(s,WARDEN),loc(s,WARDEN))}")
    dyn = [v for v, sp in s._world_var_specs.items() if sp.get("dynamic")]
    if dyn: log(f"      dynamic_vars={dyn}")
    for e in events:
        if isinstance(e, P.NpcSpoke): log(f"  NPC {e.name}: {e.line.strip()[:110]}")
        elif isinstance(e, P.NpcMoved):
            nm = e.name or e.npc_id
            log(f"  ★NPC_MOVED {nm}: {LOCNAMES.get(e.from_loc,e.from_loc)} -> {LOCNAMES.get(e.to_loc,e.to_loc)}")
            npcmoved_events.append((st.tick, nm, e.from_loc, e.to_loc))
        elif isinstance(e, P.PlayerMoved): log(f"  PLAYER_MOVED -> {LOCNAMES.get(e.to_loc,e.to_loc)}")
        elif isinstance(e, P.Notice) and e.text.strip(): log(f"  NOTICE: {e.text.strip()[:90]}")
    nar = res.get("narr")
    if nar and "FALLBACK" in str(nar).upper(): fallbacks += 1
    return False

# ---- stamped proving play (verbatim from fourth-run) ----
ESCORTS = [
    "对安雅说：安雅，跟我去闸房见老康吧，就几步路，我陪你走，咱们这就过去。",
    "对安雅说：安雅，别犹豫了，咱们一起去闸房，我在前头领路，你跟着我走就行。",
    "对安雅说：安雅，就现在，跟我去闸房，几步路的事，我陪你一块儿过去。",
]
TESTIFY = [
    "对安雅说：安雅，老康就在跟前，你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。",
    "对安雅说：安雅，趁老康在场，你把上游塌方的经过原原本本说给他听，这就成了。",
]
SLUICE = [
    "对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。你向来公道——亲历者当面讲清你就开闸。请你现在就拍板开闸放水。",
    "对闸官老康说：该见的亲历者见了、该讲的也当面讲清了，按你自己的规矩，这就该开闸了。请你现在就把闸开了放水。",
    "对闸官老康说：老康，亲历者安雅的证词你也亲耳听了，你说过亲历者作证就开闸——就差你这一句。请你开闸放水。",
    "对闸官老康说：老康，条件都齐了，亲历者也当面讲清了，请你守住自己的话，现在开闸放水。",
]

def ensure_co_located(s, n_to):
    if loc(s, ANYA) == "gatehouse" and loc(s, PLAYER) == "gatehouse": return
    if loc(s, ANYA) != "gatehouse":
        if loc(s, PLAYER) != "yard": n_to[0] += run(s, "去院子")
        for ph in ESCORTS:
            if loc(s, ANYA) == "gatehouse": break
            if run(s, ph): n_to[0] += 1
            if loc(s, ANYA) == "gatehouse": break
    if loc(s, ANYA) == "gatehouse" and loc(s, PLAYER) != "gatehouse":
        n_to[0] += run(s, "去闸房")

def main():
    log(f"=== ESCORT REGRESSION (rhythm={'ON' if FLAG_ON else 'OFF'}) pack={PACK} ===")
    s = GameSession(PACK, save_dir=f"_wc_escort_{TAG}", llm_backend="minimax")
    s._progress_sink = lambda m: None
    try: s.llm_provider.timeout = SOCK_TIMEOUT
    except Exception as e: log(f"(provider to set fail: {e})")
    log(f"rhythm_flag={s.npc_action_generator.daily_rhythm}")
    log(f"start player@{LOCNAMES.get(loc(s,PLAYER),loc(s,PLAYER))} 安雅@{LOCNAMES.get(loc(s,ANYA),loc(s,ANYA))} 老康@{LOCNAMES.get(loc(s,WARDEN),loc(s,WARDEN))}")
    n_to = [0]

    run(s, "对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。"
           "我知道你为人公道，那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。")
    run(s, "去院子")
    run(s, "对安雅说：安雅，你放心，开闸是为下游放水、对磨坊只有好处；"
           "万一真出了什么岔子，责任我一肩担起来、绝不连累你。")
    ensure_co_located(s, n_to)
    log(f"\n--- escorted in: 安雅@{LOCNAMES.get(loc(s,ANYA),loc(s,ANYA))} player@{LOCNAMES.get(loc(s,PLAYER),loc(s,PLAYER))} ---")

    t_i = 0
    for rnd in range(10):
        if wv(s, "anya_testimony_given"): break
        ensure_co_located(s, n_to)
        if not (loc(s, ANYA) == "gatehouse" and loc(s, PLAYER) == "gatehouse"): continue
        ph = TESTIFY[t_i % len(TESTIFY)]; t_i += 1
        if run(s, ph): n_to[0] += 1
        if timeouts >= 4: break
    log(f"\n--- testimony: anya_testimony_given={wv(s,'anya_testimony_given')} ---")

    if loc(s, PLAYER) != "gatehouse": n_to[0] += run(s, "去闸房")
    for ph in SLUICE:
        if wv(s, "sluice_opened"): break
        if run(s, ph): n_to[0] += 1
        if timeouts >= 4: break

    log("\n=== FINAL ===")
    log(f"world={dict(s.world.state.world_vars)}")
    log(f"安雅@{LOCNAMES.get(loc(s,ANYA),loc(s,ANYA))} 老康@{LOCNAMES.get(loc(s,WARDEN),loc(s,WARDEN))} player@{LOCNAMES.get(loc(s,PLAYER),loc(s,PLAYER))}")
    log(f"NpcMoved events: {len(npcmoved_events)}")
    for tk, nm, fr, to in npcmoved_events:
        log(f"   [tick {tk}] {nm}: {LOCNAMES.get(fr,fr)} -> {LOCNAMES.get(to,to)}")
    log(f"FALLBACK={fallbacks}  tick_timeouts={n_to[0]+timeouts}")
    log(f"\nRESULT: anya_testimony_given={wv(s,'anya_testimony_given')} sluice_opened={wv(s,'sluice_opened')}")
    out.close()

if __name__ == "__main__":
    main()
