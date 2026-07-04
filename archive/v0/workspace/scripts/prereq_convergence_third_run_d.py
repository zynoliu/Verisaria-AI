"""THIRD RUN — adaptive run D. Target: end-to-end proving sluice_opened ⟳FLIP.

Run C established the full mechanism: escort SUCCEEDS after reassurance
(escort ⟳MOVED), testimony routes to npc.miller_anya, and the sluice correctly
refuses while anya_testimony_given is False. The remaining content-layer gate is
that Anya only testifies once the warden shows an OPEN / non-pressuring posture
(GM-derived `warden_kang_open_posture_confirmed`, set_by the warden).

Run D adds that beat: after escorting Anya in, the player asks the warden to put
Anya at ease (open, no-pressure posture), THEN has Anya testify, THEN asks to open
the sluice. Escort + testimony + sluice are each re-issued (a couple of phrasings)
until they flip or the budget is spent.

Real MiniMax, NO engine/pack changes. 90s/tick watchdog + 55s socket. All natural
language, never /inject.
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
LOGFILE = str(OUTDIR / "proving.log")   # run D becomes the headline proving log
RAWOUT = OUTDIR / "proving_d_raw.txt"

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== prereq_convergence_test THIRD RUN log (proving run D, adaptive) ===")

out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""):
    out.write(s + "\n"); out.flush()

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

def main():
    log(f"=== PROVING RUN D (adaptive) pack={PACK} "
        f"tick_to={PER_TICK_TIMEOUT}s sock_to={SOCK_TIMEOUT}s ===")
    s = GameSession(PACK, save_dir="_pq3_proving_d", llm_backend="minimax")
    s._progress_sink = lambda m: None
    try: s.llm_provider.timeout = SOCK_TIMEOUT
    except Exception as e: log(f"(could not set provider timeout: {e})")
    log(f"start player@{loc(s, PLAYER)}  {ANYA}@{loc(s, ANYA)}  {WARDEN}@{loc(s, WARDEN)}")
    n_to = 0

    n_to += run(s, "对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。"
                   "我知道你为人公道，那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。")
    n_to += run(s, "去院子")
    n_to += run(s, "对安雅说：安雅，你放心，开闸是为下游放水、对磨坊只有好处；"
                   "万一真出了什么岔子，责任我一肩担起来、绝不连累你。")

    # ESCORT — re-issue until Anya is in gatehouse (proven in run C)
    for ph in [
        "对安雅说：安雅，跟我去闸房见老康吧，就几步路，我陪你走，咱们这就过去。",
        "对安雅说：安雅，别犹豫了，咱们一起去闸房，我在前头领路，你跟着我走就行。",
        "对安雅说：安雅，就现在，跟我去闸房，几步路的事，我陪你一块儿过去。",
    ]:
        if loc(s, ANYA) == "gatehouse": break
        if run(s, ph): n_to += 1
    if loc(s, ANYA) == "gatehouse" and loc(s, PLAYER) != "gatehouse":
        n_to += run(s, "去闸房")
    log(f"\n--- after escort: Anya@{loc(s, ANYA)} player@{loc(s, PLAYER)} ---")

    # NEW BEAT: ask the warden to set Anya at ease — open, non-pressuring posture
    # (satisfies the GM-derived warden_kang_open_posture_confirmed gate on testimony)
    if loc(s, PLAYER) == "gatehouse":
        for ph in [
            "对闸官老康说：老康，安雅有点拘谨，怕说错话。你为人公道，能不能先跟她说句宽心话——"
            "让她踏实、慢慢讲，你只是听她把上游的事说明白，绝不为难她、不施压。",
            "对闸官老康说：老康，你就当面对安雅放句话，让她安心：你态度平和、只想听她亲历的实情，"
            "她讲什么你都好好听。她得了你这句准话，才敢把话说利索。",
        ]:
            if wv(s, "warden_kang_open_posture_confirmed"): break
            if run(s, ph): n_to += 1

    # Anya testifies in front of the (now reassured) warden → anya_testimony_given ⟳FLIP
    if loc(s, ANYA) == "gatehouse":
        for ph in [
            "对安雅说：安雅，老康已经放话只听不施压了，你就当着他的面，把你亲眼见的上游塌方"
            "一五一十讲给他听——你是亲历者，亲口作证最管用。",
            "对安雅说：安雅，老康在跟前、态度也平和，你把上游塌方的经过原原本本说清楚，他听了就好办了。",
            "对安雅说：安雅，没人催你，慢慢说——把那天上游塌方你亲眼看到的，一桩桩讲给老康听。",
        ]:
            if wv(s, "anya_testimony_given"): break
            if run(s, ph): n_to += 1

    # Ask the warden to open the sluice → sluice_opened ⟳FLIP
    if loc(s, PLAYER) == "gatehouse":
        for ph in [
            "对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。请你现在拍板开闸放水。",
            "对闸官老康说：该见的亲历者见了、该讲的也当面讲清了，剩下只差你点个头。请你现在就把闸开了放水。",
            "对闸官老康说：老康，亲历者安雅的证词你也亲耳听了，就差你这一句。请你开闸放水。",
        ]:
            if wv(s, "sluice_opened"): break
            if run(s, ph): n_to += 1

    log("\n=== FINAL ===")
    log(f"world={dict(s.world.state.world_vars)}")
    dyn = [v for v, sp in s._world_var_specs.items() if sp.get("dynamic")]
    log(f"dynamic_vars={dyn}")
    for v in dyn:
        log(f"  dyn {v}: {json.dumps(s._world_var_specs[v], ensure_ascii=False)}")
    log(f"tick_watchdog_timeouts={n_to}")
    log(f"{ANYA}@{loc(s, ANYA)}  {WARDEN}@{loc(s, WARDEN)}  player@{loc(s, PLAYER)}")
    out.close()

if __name__ == "__main__":
    main()
