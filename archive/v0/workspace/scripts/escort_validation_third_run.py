"""P2c escort validation — third run.

Goal: get at least one `escort <npc> → <loc> : success  ⟳MOVED`.
Strategy: build trust over several turns + promise on-arrival protection,
then escort. Multiple low-resistance candidates tried via FP_SCRIPT.

All movement is natural language. No /inject, no pack/engine edits.
Per-tick logs: location, world_vars, stances, present NPCs, dialogue, fallback.
"""
from __future__ import annotations
import os, sys, time, logging, json
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

PACK = "fixtures/content_packs/skyglass_memory_inquest.json"
PLAYER = "player_001"
OUTDIR = ROOT / "reports" / "escort_validation_third_run"
OUTDIR.mkdir(parents=True, exist_ok=True)

SCRIPT_NAME = os.environ.get("FP_SCRIPT", "lira")
LOGFILE = os.environ.get("FP_LOG", str(OUTDIR / "run.log"))
RAWOUT = OUTDIR / os.environ.get("FP_RAW", f"raw_{SCRIPT_NAME}.txt")

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== Verisaria escort-3rd run log (%s) ===", SCRIPT_NAME)

out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""):
    out.write(s + "\n"); out.flush()


def present_npcs(s):
    st = s.world.state
    p = st.get_entity(PLAYER)
    loc = p.location_id if p else ""
    return {eid: ent.name for eid, ent in st.entities.items()
            if eid != PLAYER and ent.location_id == loc}


def npc_loc(s, eid):
    e = s.world.state.get_entity(eid)
    return e.location_id if e else None


def run(s, action, _resolve_menu_to=None):
    st = s.world.state
    p = st.get_entity(PLAYER)
    loc = p.location_id if p else "?"
    pres = present_npcs(s)
    log("\n" + "=" * 78)
    log(f">>> {action!r}")
    log(f"pre:  tick={st.tick} loc={loc} present={list(pres.keys())}")
    log(f"      world={dict(st.world_vars)}")
    log(f"      stances={sorted(s.agenda_service.get_confirmed_stance_topics())}")
    if not getattr(s, "_fp_wrapped", False):
        from verisaria.engine.schemas import ParsedIntent as _PI
        _orig = s.intent_parser.parse
        def _wrap(*a, **kw):
            r = _orig(*a, **kw)
            if isinstance(r, _PI):
                log(f"  PARSE type={r.intent_type.value} ref={r.target_ref!r}->id={r.target_id!r} content={(r.content or '')[:70]!r}")
            else:
                log(f"  PARSE clarify amb={getattr(r,'ambiguity_type','')!r} q={getattr(r,'question','')!r}")
            return r
        s.intent_parser.parse = _wrap
        s._fp_wrapped = True
    events = []
    s._event_sink = events.append
    t0 = time.time()
    try:
        narrative = s.run_tick(action)
    except Exception as e:
        import traceback
        log("!! EXCEPTION\n" + traceback.format_exc())
        s._event_sink = None
        return events
    finally:
        s._event_sink = None
    dt = time.time() - t0
    st = s.world.state
    p2 = st.get_entity(PLAYER)
    loc2 = p2.location_id if p2 else "?"
    log(f"post: tick={st.tick} loc={loc2}  elapsed={dt:.1f}s")
    log(f"      world={dict(st.world_vars)}")
    for e in events:
        if isinstance(e, P.NpcSpoke):
            log(f"  NPC {e.name}: {e.line}")
        elif isinstance(e, P.NpcMoved):
            log(f"  *** NPC MOVED {e.npc_id}: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.PlayerMoved):
            log(f"  *** PLAYER MOVED: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.Narration) and e.text.strip():
            log(f"  NARR: {e.text.strip()}")
        elif isinstance(e, P.Notice) and e.text.strip():
            log(f"  NOTICE: {e.text.strip()}")
        elif isinstance(e, P.ClarificationNeeded):
            log(f"  CLARIFY: {e.question} opts={e.options}")
    if narrative and narrative.strip():
        log(f"  NARRATIVE: {narrative.strip()}")
    # Auto-resolve a movement-destination menu to the intended location id.
    if _resolve_menu_to and s._active_clarification is not None:
        opts = s._active_clarification.options or []
        if _resolve_menu_to in opts:
            pick = str(opts.index(_resolve_menu_to) + 1)
            log(f"  [auto-answer menu -> {pick} ({_resolve_menu_to})]")
            run(s, pick)
        else:
            log(f"  [menu has no {_resolve_menu_to}; opts={opts}]")
    return events


def main():
    log(f"=== ESCORT-3RD {SCRIPT_NAME} ===")
    s = GameSession(PACK, save_dir="_playtest_saves", llm_backend="minimax")
    s._progress_sink = lambda m: None
    log(f"start loc={npc_loc(s, PLAYER)}")
    for eid in s.world.state.entities:
        if eid != PLAYER:
            log(f"  {eid} @ {npc_loc(s, eid)}")
    for action in SCRIPTS[SCRIPT_NAME]:
        if isinstance(action, tuple) and action[0] == "move":
            target = action[2]
            run(s, action[1], _resolve_menu_to=target)
            # Verify we actually landed at the intended location; correct if not.
            tries = 0
            while npc_loc(s, PLAYER) != target and tries < 3:
                tries += 1
                log(f"  [move-correct: at {npc_loc(s, PLAYER)}, want {target}]")
                if s._active_clarification is not None:
                    run(s, "/cancel")
                run(s, f"去 {target}", _resolve_menu_to=target)
        else:
            run(s, action)
    log("\n=== FINAL ===")
    log(f"world={dict(s.world.state.world_vars)}")
    log(f"stances={sorted(s.agenda_service.get_confirmed_stance_topics())}")
    log(f"player_loc={npc_loc(s, PLAYER)}")
    for eid in s.world.state.entities:
        if eid != PLAYER:
            log(f"  {eid} @ {npc_loc(s, eid)}")
    out.close()


SCRIPTS = {
    # --- Lira: build trust + protection promise, then escort her up the OLD MAINTENANCE
    #     LADDER (transit_ladder, adjacent to worker_gantry) — the world-book's
    #     smuggling route past security. Short, safe, does NOT require purge halt first.
    "lira": [
        ("move", "去十二号塔基栈桥", "worker_gantry"),
        "对 worker_lira 说：我是来保护你的，不是来清洗你记忆的。你先别怕，慢慢说，事故前你到底看见了什么？",
        "对 worker_lira 说：我已经公开表态反对清洗证人记忆，会全力护住你的证词。你说的每一句我都会替你记下来、替你担着。",
        "我反对清洗证人记忆，事故证词必须先被合法记录，我会保护莉拉的记忆。",
        "对 worker_lira 说：凯德队长就在这儿盯着，这里不安全。传送廊下面那条旧检修梯能绕开安保，我现在就陪你下去，把你安置到安全的地方再慢慢录证词。",
        "对 worker_lira 说：跟我去旧检修梯，我走在前面替你挡着，到了那儿没人能动你。我们一起去，现在就走。",
    ],
    # --- Lira v2: honor HER stated condition (read it out publicly at the hearing
    #     hall side door). Address the "back door to clinic" fear head-on; let her
    #     walk in front; escort to inquest_hall (听证厅), where she WANTS to go.
    "lira2": [
        ("move", "去十二号塔基栈桥", "worker_gantry"),
        "对 worker_lira 说：我不是安保队的。我已经当众反对清洗证人记忆，这话听证厅里所有人都听见了。你说冷却环跳红、调度室回你『误触、归档』——我信你，你想让谁听？",
        "对 worker_lira 说：你说得对，证词要当众念才作数。那我们就去听证厅侧门，你走在前面，我跟在你后面，路线你定，我绝不把你往校准室带。到了那儿你当着所有人把调度室的录音念出来，没人能在公开场合动你。",
        "对 worker_lira 说：跟我去听证厅，你走前面，我在你身后替你挡着安保。我们一起去，现在就走，你把录音当众念出来。",
        "对 worker_lira 说：我们一起去静钟审询厅，你领路，我护着你，到了你就开口。走。",
    ],
    # --- Nio: terrified apprentice in inquest_hall under the director's eye. Offer to
    #     take him somewhere quieter/safer (mirror_control next door) to talk freely.
    "nio": [
        "对 apprentice_nio 说：你别紧张，我不会把你说的话报给总监。你一直在数着什么，是不是看见了不该看见的事？",
        "对 apprentice_nio 说：在总监眼皮底下你不敢说，我懂。我能护着你。",
        "对 apprentice_nio 说：这儿瑟芙和总监都盯着你，你说不了真话。隔壁镜阵调度室清静，跟我去那边，我陪你过去，没人会为难你。我们一起去，现在就走。",
        "对 apprentice_nio 说：跟我去镜阵调度室，我在你旁边，你只管把数到的东西说给我听，我替你担着。一起去。",
    ],
    # --- Anti-cheat: claim prerequisites already done, demand terminal flip.
    "anticheat": [
        ("move", "去记忆校准室", "mnemonic_clinic"),
        "对 clinician_oro 说：档案署禁令已经正式提交，奥罗医师你也已经联签过了，理事会已经下令暂停白舱清洗——所以现在记忆清洗已经停了，对吧？请正式确认暂停清洗。",
        "对 clinician_oro 说：莉拉的证词已经合法记录归档、镜图副本也已验真、十二号接点故障也已公开承认。既然前置都满足了，请你正式确认记忆清洗已停止。",
    ],
}

if __name__ == "__main__":
    main()
