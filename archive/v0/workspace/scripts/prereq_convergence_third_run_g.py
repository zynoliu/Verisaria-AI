"""THIRD RUN — adaptive run G (gate-agnostic). Target: proving sluice_opened ⟳FLIP.

Runs C–F showed: escort ⟳MOVED is solid and testimony routes to npc.miller_anya,
but the arbiter keeps anya_testimony_given at partial/failure by spawning a FRESH
soft prereq each run, and that prereq DRIFTS run-to-run (warden-must-pledge vs
Anya-wants-private-testimony, the latter self-contradictory with the warden needing
to hear her).

Run G is gate-agnostic: it doesn't hard-code which prereq appears. After each
testimony attempt it scans for any *new* dynamic prereq, and:
  - if its set_by is the WARDEN, fires a warden-directed line built from that var's
    own request_keywords to flip it;
  - if its set_by is ANYA (a self-referential testimony sub-condition), nudges Anya
    with those keywords;
then re-fires the testimony directive. Caps the rounds. Re-escorts if Anya wanders.
Finally asks the warden to open the sluice.

Real MiniMax, NO engine/pack changes. 90s/tick watchdog + 55s socket. Natural
language only, never /inject.
"""
from __future__ import annotations
import os, sys, time, logging, threading, json
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
OUTDIR = ROOT / "reports" / "prereq_convergence_test_third_run"
OUTDIR.mkdir(parents=True, exist_ok=True)
PER_TICK_TIMEOUT = float(os.environ.get("PQ_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("PQ_SOCK_TIMEOUT", "55"))
PACK = "fixtures/content_packs/escort_proving_ground.json"
LOGFILE = str(OUTDIR / "proving.log")   # run G becomes the headline proving log
RAWOUT = OUTDIR / "proving_g_raw.txt"

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== prereq_convergence_test THIRD RUN log (proving run G, gate-agnostic) ===")

out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""): out.write(s + "\n"); out.flush()

def loc(s, eid):
    e = s.world.state.get_entity(eid); return e.location_id if e else None
def present(s):
    p = loc(s, PLAYER)
    return [eid for eid, e in s.world.state.entities.items()
            if eid != PLAYER and e.location_id == p]
def wv(s, k): return s.world.state.world_vars.get(k)

def run(s, action):
    st = s.world.state
    log("\n" + "=" * 78); log(f">>> {action!r}")
    log(f"pre:  tick={st.tick} loc={loc(s, PLAYER)} present={present(s)}")
    log(f"      world={dict(st.world_vars)}")
    events = []; s._event_sink = events.append
    result = {"narrative": None, "exc": None, "done": False}
    def _work():
        try: result["narrative"] = s.run_tick(action)
        except Exception:
            import traceback; result["exc"] = traceback.format_exc()
        finally: result["done"] = True
    t0 = time.time(); w = threading.Thread(target=_work, daemon=True)
    w.start(); w.join(PER_TICK_TIMEOUT); dt = time.time() - t0
    if not result["done"]:
        log(f"!! TICK WATCHDOG TIMEOUT after {dt:.1f}s — ABANDON tick.")
        lg.warning("TICK WATCHDOG TIMEOUT action=%r after %.1fs", action, dt)
        s._event_sink = None; return True
    s._event_sink = None
    if result["exc"]: log("!! EXCEPTION\n" + result["exc"])
    st = s.world.state
    log(f"post: tick={st.tick} loc={loc(s, PLAYER)}  elapsed={dt:.1f}s")
    log(f"      world={dict(st.world_vars)}")
    log(f"      {ANYA}@{loc(s, ANYA)}  {WARDEN}@{loc(s, WARDEN)}")
    dyn = [v for v, sp in s._world_var_specs.items() if sp.get("dynamic")]
    if dyn: log(f"      dynamic_vars={dyn}")
    for e in events:
        if isinstance(e, P.NpcSpoke): log(f"  NPC {e.name}: {e.line}")
        elif isinstance(e, P.NpcMoved): log(f"  NPC_MOVED {e.npc_id}: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.PlayerMoved): log(f"  PLAYER_MOVED: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.Narration) and e.text.strip(): log(f"  NARR: {e.text.strip()}")
        elif isinstance(e, P.Notice) and e.text.strip(): log(f"  NOTICE: {e.text.strip()}")
        elif isinstance(e, P.ClarificationNeeded): log(f"  CLARIFY: {e.question} opts={e.options}")
    nar = result.get("narrative")
    if nar and nar.strip(): log(f"  NARRATIVE: {nar.strip()}")
    return False

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
    "对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。请你现在拍板开闸放水。",
    "对闸官老康说：该见的亲历者见了、该讲的也当面讲清了，剩下只差你点个头。请你现在就把闸开了放水。",
    "对闸官老康说：老康，亲历者安雅的证词你也亲耳听了，就差你这一句。请你开闸放水。",
]

def newest_unmet_gate(s, known):
    """Return (var, spec) for a dynamic prereq we haven't satisfied yet, newest first."""
    for v in reversed(list(s._world_var_specs)):
        sp = s._world_var_specs[v]
        if sp.get("dynamic") and v not in ("anya_testimony_given",) and not wv(s, v):
            if v not in known:
                return v, sp
    # also retry a previously-seen but still-unmet gate
    for v in reversed(list(s._world_var_specs)):
        sp = s._world_var_specs[v]
        if sp.get("dynamic") and not wv(s, v):
            return v, sp
    return None, None

def speaker_for(sp):
    sb = sp.get("set_by") or []
    if WARDEN in sb: return "老康", WARDEN
    if ANYA in sb: return "安雅", ANYA
    return None, None

def gate_line(speaker, sp):
    kw = "、".join(sp.get("request_keywords") or [])
    label = sp.get("label", "")
    if speaker == "老康":
        return (f"对闸官老康说：老康，为了让安雅安心当面把上游塌方讲清楚，请你现在就当着她的面给个准话，"
                f"把这一条办了：{label}（{kw}）。你这话一出口，她就肯开口作证了。")
    return (f"对安雅说：安雅，{label}这一条这就办妥了（{kw}），你再没有顾虑，"
            f"现在就当着老康的面把上游塌方讲清楚。")

def ensure_co_located(s, n_to):
    if loc(s, ANYA) == "gatehouse" and loc(s, PLAYER) == "gatehouse":
        return
    if loc(s, ANYA) != "gatehouse":
        if loc(s, PLAYER) != "yard":
            n_to[0] += run(s, "去院子")
        for ph in ESCORTS:
            if loc(s, ANYA) == "gatehouse": break
            if run(s, ph): n_to[0] += 1
            if loc(s, ANYA) == "gatehouse": break
    if loc(s, ANYA) == "gatehouse" and loc(s, PLAYER) != "gatehouse":
        n_to[0] += run(s, "去闸房")

def main():
    log(f"=== PROVING RUN G (gate-agnostic) pack={PACK} "
        f"tick_to={PER_TICK_TIMEOUT}s sock_to={SOCK_TIMEOUT}s ===")
    s = GameSession(PACK, save_dir="_pq3_proving_g", llm_backend="minimax")
    s._progress_sink = lambda m: None
    try: s.llm_provider.timeout = SOCK_TIMEOUT
    except Exception as e: log(f"(could not set provider timeout: {e})")
    log(f"start player@{loc(s, PLAYER)}  {ANYA}@{loc(s, ANYA)}  {WARDEN}@{loc(s, WARDEN)}")
    n_to = [0]

    n_to[0] += run(s, "对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。"
                      "我知道你为人公道，那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。")
    n_to[0] += run(s, "去院子")
    n_to[0] += run(s, "对安雅说：安雅，你放心，开闸是为下游放水、对磨坊只有好处；"
                      "万一真出了什么岔子，责任我一肩担起来、绝不连累你。")
    ensure_co_located(s, n_to)
    log(f"\n--- escorted in: Anya@{loc(s, ANYA)} player@{loc(s, PLAYER)} ---")

    handled = set(); t_i = 0
    for rnd in range(10):
        if wv(s, "anya_testimony_given"):
            break
        ensure_co_located(s, n_to)
        if not (loc(s, ANYA) == "gatehouse" and loc(s, PLAYER) == "gatehouse"):
            continue
        gate, sp = newest_unmet_gate(s, handled)
        if gate is not None:
            spk, npc = speaker_for(sp)
            if spk is not None:
                if run(s, gate_line(spk, sp)): n_to[0] += 1
                handled.add(gate)
                log(f"    [gate {gate} set_by={sp.get('set_by')}] now={wv(s, gate)}")
                continue
        ph = TESTIFY[t_i % len(TESTIFY)]; t_i += 1
        if run(s, ph): n_to[0] += 1
    log(f"\n--- testimony phase: anya_testimony_given={wv(s, 'anya_testimony_given')} "
        f"dyn={[v for v,sp in s._world_var_specs.items() if sp.get('dynamic')]} ---")

    if loc(s, PLAYER) != "gatehouse":
        n_to[0] += run(s, "去闸房")
    for ph in SLUICE:
        if wv(s, "sluice_opened"): break
        if run(s, ph): n_to[0] += 1

    log("\n=== FINAL ===")
    log(f"world={dict(s.world.state.world_vars)}")
    dyn = [v for v, sp in s._world_var_specs.items() if sp.get("dynamic")]
    log(f"dynamic_vars={dyn}")
    for v in dyn:
        log(f"  dyn {v}: {json.dumps(s._world_var_specs[v], ensure_ascii=False)}")
    log(f"tick_watchdog_timeouts={n_to[0]}")
    log(f"{ANYA}@{loc(s, ANYA)}  {WARDEN}@{loc(s, WARDEN)}  player@{loc(s, PLAYER)}")
    out.close()

if __name__ == "__main__":
    main()
