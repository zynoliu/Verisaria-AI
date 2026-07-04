"""P2c escort closed-loop · THIRD run — adaptive prereq-chaser (best shot at full chain).

After ⟳MOVED, ask the warden to open the sluice; the engine emerges SOME dynamic
prereq (stochastic: an Anya-eyewitness var, or a warden-authorization var, etc.).
We INSPECT each newly-emerged var's set_by:
  - if Anya is a set_by  → address Anya with that var's keywords to flip it, then
    re-ask the warden.
  - if only the warden/authority can set it (document/verification) → we record it
    as a legitimately-harder gate that in-scene testimony can't satisfy.
World-change asks are RETRIED (the world-change arbiter call intermittently fails
schema-VALIDATION on MiniMax → engine fallback; a retry usually parses).
Every tick watchdog-protected.
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
OUTDIR = ROOT / "reports" / "escort_moved_validation_third_run"
LOGFILE = str(OUTDIR / "run.log")
RAWOUT = OUTDIR / "main_raw.txt"
PER_TICK_TIMEOUT = float(os.environ.get("ESC_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("ESC_SOCK_TIMEOUT", "55"))

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== escort_moved THIRD prereq-chaser run log ===")
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

def keywords_for(s, var_id):
    return (specs(s).get(var_id, {}) or {}).get("request_keywords") or []
def setby_for(s, var_id):
    return (specs(s).get(var_id, {}) or {}).get("set_by") or []

def anya_settable_open_prereq(s):
    """Return (var_id) of a NOT-yet-true dynamic var that Anya can set, else None."""
    for vid, spec in specs(s).items():
        if not spec.get("dynamic"): continue
        if s.world.state.world_vars.get(vid): continue
        sb = spec.get("set_by") or []
        if ANYA in sb or "miller_anya" in sb:
            return vid
    return None

def ensure_here(s, who):
    if loc(s, who) != loc(s, PLAYER):
        tgt = loc(s, who)
        run(s, "去闸房" if tgt == "gatehouse" else "去院子")

def main():
    log(f"=== THIRD prereq-chaser: per_tick={PER_TICK_TIMEOUT}s sock={SOCK_TIMEOUT}s ===")
    s = GameSession(PACK, save_dir="_playtest_saves_escort3d", llm_backend="minimax")
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

    for rnd in range(6):
        if s.world.state.world_vars.get("sluice_opened"):
            log("*** sluice_opened ⟳FLIP=True ***"); break
        # 1) Ask warden to open the sluice (retry to dodge intermittent VALIDATION fallback).
        ensure_here(s, KANG)
        # keep Anya present too (warden often wants the eyewitness in the room)
        if loc(s, ANYA) != loc(s, PLAYER):
            ensure_here(s, ANYA)
            if loc(s, ANYA) != "gatehouse":
                run(s, ESCORT)
        log(f"\n--- OPEN-SLUICE ASK round {rnd+1} (vars={list(specs(s))}) ---")
        run(s, "对闸官老康说：上游塌方已有亲历者当面作证，险情属实，请你开闸放水。")
        if s.world.state.world_vars.get("sluice_opened"):
            log("*** sluice_opened ⟳FLIP=True ***"); break
        # 2) If an Anya-settable prereq emerged, flip it by having Anya speak its keywords.
        vid = anya_settable_open_prereq(s)
        if vid:
            kws = keywords_for(s, vid)
            log(f"\n--- ANYA FLIPS prereq {vid!r} set_by={setby_for(s,vid)} keywords={kws} ---")
            ensure_here(s, ANYA); ensure_here(s, KANG)
            if loc(s, ANYA) != "gatehouse":
                run(s, ESCORT)
            kw_hint = "、".join(kws[:4]) if kws else "安雅作证、当面陈述、塌方证词"
            run(s, f"对安雅说：安雅，当着闸官老康的面，把你亲眼见的上游塌方当面陈述清楚——"
                   f"这就是你的塌方证词，安雅作证、当面陈述给老康听。（{kw_hint}）"
                   f"你当时在渠口，看见整面山皮塌进河里、水头一下就断了。")
            if s.world.state.world_vars.get(vid):
                log(f"*** {vid} ⟳FLIP=True (Anya testified) ***")
        else:
            # Non-Anya prereq (authorization/verification) — record it; testimony can't satisfy.
            dyn = [v for v, sp in specs(s).items() if sp.get("dynamic")
                   and not s.world.state.world_vars.get(v)]
            log(f"\n--- NO Anya-settable prereq this round. Outstanding dynamic vars: "
                f"{[(v, setby_for(s,v)) for v in dyn]} ---")
            # Try once more anyway in case it was a transient fallback.

    _final(s)

def _final(s):
    log("\n=== FINAL ===")
    log(f"world={wv(s)}")
    log("world_var_specs (dynamic):")
    for v, sp in specs(s).items():
        if sp.get("dynamic"):
            log(f"  {v}: set_by={sp.get('set_by')} keywords={sp.get('request_keywords')} "
                f"value={s.world.state.world_vars.get(v)}")
    log(f"player@{loc(s,PLAYER)} anya@{loc(s,ANYA)} kang@{loc(s,KANG)}")
    out.close()

if __name__ == "__main__":
    main()
