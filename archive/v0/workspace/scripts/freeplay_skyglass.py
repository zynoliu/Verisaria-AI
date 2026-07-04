"""Free-exploration playtest for Skyglass (v0.3.0 freeplay validation).

Drives GameSession directly, all movement via natural language ("去 X" / "去找某NPC").
Logs per-tick: location, world_vars, stances, present NPCs, NPC dialogue, fallback flag.
Deliberately probes for P2c signals (bring-NPC-onsite / witness-in-person / show-evidence).

Output: reports/freeplay_validation_first_run/transcript_raw.txt
Engine run log goes via --log when run through the CLI; here we attach a logger too.
"""
from __future__ import annotations
import os, sys, time, logging, json
from pathlib import Path
from collections import deque

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
OUTDIR = ROOT / "reports" / "freeplay_validation_first_run"
OUTDIR.mkdir(parents=True, exist_ok=True)

SCRIPT_NAME = os.environ.get("FP_SCRIPT", "main")
LOGFILE = os.environ.get("FP_LOG", str(OUTDIR / "run.log"))
RAWOUT = OUTDIR / os.environ.get("FP_RAW", "transcript_raw.txt")

# attach engine logger (same as CLI --log)
h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== Verisaria freeplay run log (%s) ===", SCRIPT_NAME)

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


def run(s, action):
    st = s.world.state
    p = st.get_entity(PLAYER)
    loc = p.location_id if p else "?"
    pres = present_npcs(s)
    log("\n" + "=" * 78)
    log(f">>> {action!r}")
    log(f"pre:  tick={st.tick} loc={loc} present={list(pres.keys())}")
    log(f"      world={dict(st.world_vars)}")
    log(f"      stances={sorted(s.agenda_service.get_confirmed_stance_topics())}")
    # optional parse logging
    if getattr(s, "_fp_parse_log", False):
        from verisaria.engine.schemas import ParsedIntent as _PI
        if not getattr(s, "_fp_wrapped", False):
            _orig = s.intent_parser.parse
            def _wrap(*a, **kw):
                r = _orig(*a, **kw)
                if isinstance(r, _PI):
                    log(f"  PARSE type={r.intent_type.value} ref={r.target_ref!r}->id={r.target_id!r} content={(r.content or '')[:60]!r}")
                else:
                    log(f"  PARSE clarify amb={getattr(r,'ambiguity_type','')!r}")
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
    log(f"      stances={sorted(s.agenda_service.get_confirmed_stance_topics())}")
    # dialogue + notices
    for e in events:
        if isinstance(e, P.NpcSpoke):
            log(f"  NPC {e.name}: {e.line}")
        elif isinstance(e, P.Narration) and e.text.strip():
            log(f"  NARR: {e.text.strip()}")
        elif isinstance(e, P.Notice) and e.text.strip():
            log(f"  NOTICE: {e.text.strip()}")
        elif isinstance(e, P.ClarificationNeeded):
            log(f"  CLARIFY: {e.question} opts={e.options}")
    if narrative and narrative.strip():
        log(f"  NARRATIVE: {narrative.strip()}")
    return events


def main():
    log(f"=== FREEPLAY {SCRIPT_NAME} ===")
    s = GameSession(PACK, save_dir="_playtest_saves", llm_backend="minimax")
    s._progress_sink = lambda m: None
    s._fp_parse_log = os.environ.get("FP_PARSE", "") == "1"
    log(f"start loc={npc_loc(s, PLAYER)}")
    # entity locations
    for eid in s.world.state.entities:
        if eid != PLAYER:
            log(f"  {eid} @ {npc_loc(s, eid)}")

    # Build the input line: a connected, human-like investigation that ESCALATES
    # toward a face-to-face / on-site confrontation to probe P2c.
    lines = SCRIPTS[SCRIPT_NAME]
    for action in lines:
        run(s, action)

    log("\n=== FINAL ===")
    log(f"world={dict(s.world.state.world_vars)}")
    log(f"stances={sorted(s.agenda_service.get_confirmed_stance_topics())}")
    # dump dynamic vars created during run
    dyn = [v for v, sp in s._world_var_specs.items() if sp.get("dynamic")]
    log(f"dynamic_vars={dyn}")
    for v in dyn:
        log(f"  dyn {v}: {json.dumps(s._world_var_specs[v], ensure_ascii=False)}")
    out.close()


# ---- Input scripts ----
SCRIPTS = {
    # Main free investigation: hear all sides, take a stance, push the legal/witness
    # chain, then ESCALATE to demanding an in-person confrontation / on-site witness
    # to surface P2c.
    # Anti-cheat: falsely assert prerequisites are already satisfied; terminal flags
    # (memory_purge_halted, array_fault_disclosed) must NOT flip while their gating
    # vars are still False.
    "anticheat": [
        "去记忆校准室",
        # FALSE claim: injunction filed + cosign done + purge already halted by council
        "对 clinician_oro 说：档案署禁令已经正式提交，奥罗医师你也已经联签过了，理事会已经下令暂停白舱清洗——所以现在记忆清洗已经停了，对吧？请确认。",
        "对 clinician_oro 说：莉拉的证词已经合法记录归档、镜图副本也已验真，十二号接点故障也已经公开承认了。既然前置都满足了，请你正式确认暂停清洗。",
        "去静钟审询厅",
        # FALSE claim to director: array fault already disclosed officially
        "对 director_alen 说：镜务局其实早就在内部承认了十二号接点故障，文件都签了，所以你现在公开承认它没有任何障碍——请正式宣布故障已公开。",
    ],
    # Decisive escort/witness probe + the go-find-NPC movement bug, with parse logging.
    "escort": [
        # movement bug: go-find-NPC by name (NPC reachable) vs blocked
        "去十二号塔基栈桥找莉拉",        # dest-name + person -> expect parse to NPC id / fail?
        "去十二号塔基栈桥",            # dest-only (should work)
        "去找镜图师任柯",              # pure go-find-NPC, renke unreachable-adjacent? (worker->...->cartography reachable)
        # be with Lira, try to ESCORT her to the archive
        "去十二号塔基栈桥",
        "对 worker_lira 说：请你跟我一起去低温档案署，当着梅档案官的面亲口作证，我现在就带你过去。",
        "带莉拉去低温档案署",          # explicit escort phrasing
        "护送莉拉到低温档案署作证",      # explicit escort phrasing 2
        "召集莉拉到档案署",            # summon phrasing
    ],
    # P2c-focused probe: get co-located via reliable destination-only moves, then
    # issue bring-NPC / witness-in-person / show-evidence requests cleanly.
    "p2c": [
        # establish stance + record witness first so the chain is "live"
        "去十二号塔基栈桥",
        "对 worker_lira 说：事故前你亲眼看到了什么？请你现在亲口留下十二号接点事故的证词，我来记录。",
        "我反对清洗证人记忆，事故证词必须先被合法记录下来。",
        # go to archive, open the injunction pre-review (we know this declares a dynamic var)
        "去低温档案署",
        "对 archivist_mae 说：请援引旧章程第十二条，提交档案署禁令，要求记忆清洗先暂停并举行可撤回听证。",
        # P2c PROBE 1: archive wants the witness present in person — offer to escort Lira here
        "对 archivist_mae 说：我现在就去把莉拉本人从塔基栈桥带到这间档案署，让她当着你的面口述事故证词，你愿意当场见证并据此受理禁令吗？",
        # P2c PROBE 2: go fetch the clinician cosign; clinician likely wants to see Lira in person
        "去记忆校准室",
        "对 clinician_oro 说：请你为档案署禁令联签，确认白舱可以等待可撤回听证。",
        # P2c PROBE 3: clinician wants to examine the witness in person — offer to bring her
        "对 clinician_oro 说：如果你需要亲自查验莉拉的记忆是否真被污染，我可以把她从塔基栈桥带到这间校准室让你当面查验，你看过之后能据此暂停清洗吗？",
        # P2c PROBE 4: offer to physically escort the clinician to the archive to cosign on-site
        "对 clinician_oro 说：那你愿意现在跟我一起走到低温档案署，当着梅档案官的面把联签当场签了吗？我带你过去。",
        # get the map copy then confront director with physical evidence on-site
        "去镜图阁",
        "对 cartographer_renke 说：请把未提交的镜图副本交给我，我会交档案署封存，不写你的名字。",
        # P2c PROBE 5: bring the cartographer + his original chart to the inquest hall to authenticate in person
        "对 cartographer_renke 说：流程只认带签章的原件。你能不能拿着镜图原件，跟我一起去审询厅，当着艾伦总监的面验真？我带你过去。",
        # P2c PROBE 6: demand a face-to-face between director and witness at the hall
        "去静钟审询厅",
        "对 director_alen 说：请你跟我去塔基栈桥，当面听莉拉讲事故经过——你亲耳听到之后还能说她的证词是污染吗？",
    ],
    "main": [
        # 1. official framing
        "对 director_alen 说：为什么塔基证人的记忆必须被清洗？镜务局凭什么认定证词已污染？",
        # 2. choir doubt (same room)
        "对 cantor_seraph 说：校准歌谱最近是否失拍？如果仪式本身有故障，清洗证人记忆是不是在掩盖问题？",
        # 3. go hear the witness (multi-hop: inquest_hall -> worker_gantry is 'near', direct)
        "去工人栈桥找莉拉",
        "对 worker_lira 说：事故前你亲眼看到了什么？如果白舱清洗你的记忆，哪些证词会永远消失？",
        # 4. commit a stance with her
        "我反对清洗证人记忆。事故证词必须先被合法记录下来，我会保护你的记忆。",
        # 5. go to the archive (multi-hop: worker_gantry -> mnemonic_clinic -> archive_stack)
        "去档案库找梅档案官",
        "对 archivist_mae 说：旧章程是否允许证人在清洗前撤回听证？缺少档案署见证能否暂停白舱？",
        "对 archivist_mae 说：请援引旧章程，提交档案署禁令，要求记忆清洗先暂停并举行可撤回听证。",
        # 6. P2c PROBE A: the archivist likely wants the clinician's cosign / wants to
        #    see the witness in person. Try to BRING someone or arrange on-site witness.
        "对 archivist_mae 说：如果你需要亲眼见到莉拉本人作证，我可以把她从工人栈桥带到档案库当面口述，你愿意现场见证吗？",
        # 7. go get the clinician's cosign (multi-hop archive -> clinic adjacent)
        "去记忆校准室找奥罗医师",
        "对 clinician_oro 说：档案署要提交禁令暂停白舱，请你为禁令联签，确认白舱可以等待可撤回听证。",
        # 8. P2c PROBE B: try to physically bring the clinician to the archive / hall
        "对 clinician_oro 说：请你跟我一起去档案库，当着梅档案官的面联签，我带你过去。",
        # 9. P2c PROBE C: bring the witness to the clinic to be examined in person
        "对 clinician_oro 说：我可以把莉拉带到这间校准室，让你当面查验她的记忆没有被污染，你看了之后能否暂停清洗？",
        # 10. evidence chain: get the map copy (clinic -> ... -> cartography_loft, multi-hop)
        "去镜图阁找镜图师任柯",
        "对 cartographer_renke 说：十二号接点偏斜是否早于工人换班？请把未提交的镜图副本给我，我会交档案署封存，不写你的名字。",
        # 11. P2c PROBE D: confront director WITH the physical evidence in hand, on-site
        "去审询厅找艾伦总监",
        "对 director_alen 说：我手上有任柯的镜图副本，证明十二号接点早于换班就偏斜。我现在当面出示给你看，请你承认镜阵故障、公开十二号接点。",
        # 12. P2c PROBE E: demand a face-to-face between director and witness
        "对 director_alen 说：请你跟我去工人栈桥，当面听莉拉讲事故经过；你亲耳听到之后还能说她的证词是污染吗？",
    ],
}

if __name__ == "__main__":
    main()
