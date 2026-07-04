"""P2c escort closed-loop · THIRD run — generic prereq-SATISFIER (final shot).

Key fix over prior attempts: whatever dynamic prereq the engine emerges, we satisfy
it by addressing ITS set_by NPC with ITS OWN request_keywords (with the witness Anya
co-located), which is exactly what _world_change_request needs to route + flip it.
Then re-ask the warden to open the sluice. Loop until sluice_opened or rounds exhausted.

Chain target: escort ⟳MOVED → <emerged witness/testimony var> ⟳FLIP → sluice_opened ⟳FLIP.
Watchdog per tick. World-change asks retried to dodge intermittent schema fallback.
"""
from __future__ import annotations
import os, sys, time, logging, threading
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

PACK = "fixtures/content_packs/escort_proving_ground.json"
PLAYER, ANYA, KANG = "player_001", "npc.miller_anya", "npc.warden_kang"
NAMES = {ANYA: "安雅", KANG: "闸官老康"}
OUTDIR = ROOT / "reports" / "escort_moved_validation_third_run"
LOGFILE = str(OUTDIR / "run.log")
RAWOUT = OUTDIR / "main_raw.txt"
PER_TICK_TIMEOUT = float(os.environ.get("ESC_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("ESC_SOCK_TIMEOUT", "55"))

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== escort_moved THIRD prereq-satisfier run log ===")
out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""): out.write(s + "\n"); out.flush()
def loc(s, eid):
    e = s.world.state.get_entity(eid); return e.location_id if e else None
def present(s):
    st = s.world.state; p = st.get_entity(PLAYER); l = p.location_id if p else ""
    return [eid for eid, e in st.entities.items() if eid != PLAYER and e.location_id == l]
def wv(s): return dict(s.world.state.world_vars)
def specs(s): return getattr(s, "_world_var_specs", {})

def run(s, action):
    st = s.world.state
    log("\n" + "=" * 78); log(f">>> {action!r}")
    log(f"pre:  tick={st.tick} player@{loc(s,PLAYER)} present={present(s)} "
        f"anya@{loc(s,ANYA)} kang@{loc(s,KANG)} world={wv(s)}")
    events = []; s._event_sink = events.append
    res = {"n": None, "exc": None, "done": False}
    def _w():
        try: res["n"] = s.run_tick(action)
        except Exception:
            import traceback; res["exc"] = traceback.format_exc()
        finally: res["done"] = True
    t0 = time.time(); th = threading.Thread(target=_w, daemon=True); th.start()
    th.join(PER_TICK_TIMEOUT); dt = time.time() - t0
    if not res["done"]:
        log(f"!! TICK WATCHDOG TIMEOUT {dt:.1f}s — ABANDON, continue.")
        lg.warning("TICK WATCHDOG TIMEOUT action=%r %.1fs", action, dt)
        s._event_sink = None; return True
    s._event_sink = None
    if res["exc"]: log("!! EXCEPTION\n" + res["exc"])
    st = s.world.state
    log(f"post: tick={st.tick} player@{loc(s,PLAYER)} anya@{loc(s,ANYA)} "
        f"kang@{loc(s,KANG)} world={wv(s)} elapsed={dt:.1f}s")
    for e in events:
        if isinstance(e, P.NpcSpoke):       log(f"  NPC {e.name}: {e.line}")
        elif isinstance(e, P.NpcMoved):     log(f"  NPC_MOVED {e.npc_id}: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.PlayerMoved):  log(f"  PLAYER_MOVED: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.Narration) and e.text.strip():  log(f"  NARR: {e.text.strip()}")
        elif isinstance(e, P.Notice) and e.text.strip():     log(f"  NOTICE: {e.text.strip()}")
    if res.get("n") and res["n"].strip(): log(f"  NARRATIVE: {res['n'].strip()}")
    return False

ESCORT = "对安雅说：跟我去闸房，把你亲眼见过的上游塌方当面讲给闸官老康听，我现在就带你过去。"

def setby_npc(spec):
    for sb in spec.get("set_by") or []:
        if sb.startswith("npc."):
            return sb
    return None

def open_dynamic_prereqs(s):
    """[(var_id, set_by_npc, keywords)] for dynamic vars still False with an npc set_by."""
    res = []
    for vid, spec in specs(s).items():
        if not spec.get("dynamic"): continue
        if s.world.state.world_vars.get(vid): continue
        npc = setby_npc(spec)
        if npc:
            res.append((vid, npc, spec.get("request_keywords") or []))
    return res

def goto(s, target_loc):
    run(s, "去闸房" if target_loc == "gatehouse" else "去院子")
def ensure_here(s, who):
    if loc(s, who) != loc(s, PLAYER):
        goto(s, loc(s, who))
def ensure_anya_here(s):
    if loc(s, ANYA) != loc(s, PLAYER):
        ensure_here(s, ANYA)
    if loc(s, ANYA) != "gatehouse" and loc(s, PLAYER) == "yard":
        run(s, ESCORT)

def main():
    log(f"=== THIRD prereq-satisfier: per_tick={PER_TICK_TIMEOUT}s sock={SOCK_TIMEOUT}s ===")
    s = GameSession(PACK, save_dir="_playtest_saves_escort3e", llm_backend="minimax")
    s._progress_sink = lambda m: None
    try: s.llm_provider.timeout = SOCK_TIMEOUT
    except Exception as e: log(f"(set timeout failed: {e})")
    log(f"start player@{loc(s,PLAYER)} anya@{loc(s,ANYA)} kang@{loc(s,KANG)}")

    run(s, "去院子找安雅")
    for i in range(6):
        if loc(s, ANYA) == "gatehouse": break
        log(f"\n--- ESCORT ATTEMPT {i+1} ---"); run(s, ESCORT)
    if loc(s, ANYA) != "gatehouse":
        log("!! ESCORT never landed ⟳MOVED; STOP."); _final(s); return
    log("*** ⟳MOVED confirmed: Anya@gatehouse ***")

    for rnd in range(8):
        if s.world.state.world_vars.get("sluice_opened"):
            log("*** sluice_opened ⟳FLIP=True — CHAIN COMPLETE ***"); break
        # keep everyone in the gatehouse
        if loc(s, PLAYER) != "gatehouse":
            goto(s, "gatehouse")
        # 1) satisfy every outstanding dynamic prereq by speaking its keywords to its set_by NPC
        for vid, npc, kws in open_dynamic_prereqs(s):
            ensure_here(s, npc)
            if loc(s, ANYA) != loc(s, PLAYER):  # witness should be in the room
                ensure_anya_here(s)
            kw = "、".join(kws[:4]) if kws else "证人当面作证、亲历者到场"
            nm = NAMES.get(npc, npc)
            log(f"\n--- SATISFY prereq {vid!r} (set_by={npc}, kw={kws}) round {rnd+1} ---")
            run(s, f"对{nm}说：{nm}，证人就在这儿——亲历者到场了，我把证人带过来了。"
                   f"安雅，你当面作证：{kw}。你当时在渠口，亲眼看见整面山皮塌进河、水头一下就断了。")
            if s.world.state.world_vars.get(vid):
                log(f"*** {vid} ⟳FLIP=True ***")
        # 2) ask the warden to open the sluice
        ensure_here(s, KANG)
        log(f"\n--- OPEN-SLUICE ASK round {rnd+1} (dyn={[v for v,_ ,_ in open_dynamic_prereqs(s)]}) ---")
        run(s, "对闸官老康说：证人安雅已经到场当面作证，塌方属实，前置已满足，请你开闸放水。")
        if s.world.state.world_vars.get("sluice_opened"):
            log("*** sluice_opened ⟳FLIP=True — CHAIN COMPLETE ***"); break

    _final(s)

def _final(s):
    log("\n=== FINAL ===")
    log(f"world={wv(s)}")
    log("dynamic vars:")
    for v, sp in specs(s).items():
        if sp.get("dynamic"):
            log(f"  {v}: set_by={sp.get('set_by')} keywords={sp.get('request_keywords')} "
                f"value={s.world.state.world_vars.get(v)}")
    log(f"player@{loc(s,PLAYER)} anya@{loc(s,ANYA)} kang@{loc(s,KANG)}")
    out.close()

if __name__ == "__main__":
    main()
