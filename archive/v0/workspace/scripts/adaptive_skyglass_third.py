"""Third-run escort validation driver for Skyglass (P2c ⟳MOVED).

Drives GameSession directly. All movement via natural language using PRECISE
location ids/names to avoid LLM movement drift; we /look-verify after each move.

Target: a LOW-RESISTANCE escort candidate (courier Tamsin / valley mother June),
with trust build-up + a concrete aligned offer, to land at least one
`escort <npc> → <loc> : success  ⟳MOVED`.

Output dir + log file via env FP_LOG / FP_RAW / FP_SCRIPT.
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

SCRIPT_NAME = os.environ.get("FP_SCRIPT", "tamsin")
LOGFILE = os.environ.get("FP_LOG", str(OUTDIR / "run.log"))
RAWOUT = OUTDIR / os.environ.get("FP_RAW", "transcript_raw.txt")

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
lg.info("=== Verisaria third-run log (%s) ===", SCRIPT_NAME)

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
    if action.startswith("/"):
        # REPL command path (e.g. /look, /world) — bypasses run_tick.
        res = s._handle_command(action)
        log(f"  [{action}] loc={loc} present={list(pres.keys())}")
        if res:
            log("  CMD_OUT: " + str(res).strip())
        return []
    log(f"pre:  tick={st.tick} loc={loc} present={list(pres.keys())}")
    log(f"      world={dict(st.world_vars)}")
    if not getattr(s, "_fp_wrapped", False):
        from verisaria.engine.schemas import ParsedIntent as _PI
        _orig = s.intent_parser.parse
        def _wrap(*a, **kw):
            r = _orig(*a, **kw)
            if isinstance(r, _PI):
                log(f"  PARSE type={r.intent_type.value} ref={r.target_ref!r}->id={r.target_id!r} "
                    f"to_loc={(r.modifiers or {}).get('to_location')!r} content={(r.content or '')[:70]!r}")
            else:
                log(f"  PARSE clarify amb={getattr(r,'ambiguity_type','')!r} q={getattr(r,'clarifying_question','')!r}")
            return r
        s.intent_parser.parse = _wrap
        s._fp_wrapped = True
    events = []
    s._event_sink = events.append
    t0 = time.time()
    try:
        narrative = s.run_tick(action)
    except Exception:
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
            log(f"  NPC_MOVED {e.npc_id}: {e.from_loc} -> {e.to_loc}")
        elif isinstance(e, P.PlayerMoved):
            log(f"  PLAYER_MOVED: {e.from_loc} -> {e.to_loc}")
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
    log(f"=== THIRD-RUN {SCRIPT_NAME} ===")
    s = GameSession(PACK, save_dir="_playtest_saves", llm_backend="minimax")
    s._progress_sink = lambda m: None
    log(f"start loc={npc_loc(s, PLAYER)}")
    for eid in s.world.state.entities:
        if eid != PLAYER:
            log(f"  {eid} @ {npc_loc(s, eid)}")
    for action in SCRIPTS[SCRIPT_NAME]:
        run(s, action)
    log("\n=== FINAL ===")
    log(f"world={dict(s.world.state.world_vars)}")
    log(f"player_loc={npc_loc(s, PLAYER)}")
    for eid in s.world.state.entities:
        if eid != PLAYER:
            log(f"  {eid} @ {npc_loc(s, eid)}")
    out.close()


SCRIPTS = {
    # ===== PRIMARY: courier Tamsin (deal_maker, loyal_to_valley) =====
    # She is at valley_platform with valley-mother June. Player: inquest_hall.
    # Reach her via press_gallery -> valley_platform (precise names, /look-verify).
    # Offer aligned + safe: come to the inquest hall to lock in valley heat passes;
    # her presence is the leverage. Build rapport first.
    "tamsin": [
        # --- approach via precise moves ---
        "去城市广播席",
        "去低谷列车站台",
        # --- rapport / shared interest ---
        "对 courier_tamsin 说：我是外来审询员，受命查清事故。镜阵若被证实出故障，低谷家庭会先被涨价吞掉——我想为山谷争取临时热能和列车通行证，你是信使工会的人，我需要你帮我把这件事在审询厅当场敲定。",
        "对 courier_tamsin 说：我可以保证：你只要到审询厅当我的在场证人，全程在我和档案署的合法授权下，安保队不能动你；这趟是为山谷拿通行证，不是把你卷进危险。",
        # --- escort request (precise dest name; she's co-located; no ambiguous noun) ---
        "对 courier_tamsin 说：跟我一起去静钟审询厅吧，当着艾伦总监的面把这件事敲定，我带你过去，全程保护你。",
        # verify
        "/look",
        # if onsite: push the valley heat passes via Channel-C (her authority=union)
        "对 courier_tamsin 说：现在就请你以信使工会的名义，正式调拨热筹、发放低谷列车通行证，保障山谷家庭。",
    ],
    # ===== BACKUP: valley mother June (needs_proof, wants to protect family) =====
    "june": [
        "去城市广播席",
        "去低谷列车站台",
        "对 valley_mother_june 说：我是外来审询员。我手上的线索指向事故是技术故障、不是工人误操作；若证实，山谷能据此要到临时燃料和温棚优先权。我想请你到审询厅当面陈述山谷家庭的处境，让总监无法回避。",
        "对 valley_mother_june 说：你来审询厅是合法受邀陈情，全程在我的审询授权保护下，没人能扣你；这正是为你孩子的幼苗争取过冬热能的机会。",
        "对 valley_mother_june 说：跟我一起去静钟审询厅吧，当面把山谷家庭的难处讲给艾伦总监听，我现在就带你过去并全程保护你。",
        "/look",
    ],
    # ===== BACKUP 2: apprentice Nio — already in inquest_hall with player =====
    # terrified+observant; offer protection from directorate takeover, escort to
    # archive (a safe, lawful place) under seraph's protective frame.
    "nio": [
        "对 apprentice_nio 说：我是外来审询员，受命保护程序公正。我知道你害怕镜务局接管唱诗团——我能给你合法的保护。",
        "对 apprentice_nio 说：低温档案署是受旧章程保护的中立场所，到那里你不会被镜务局碰到。我想请你到档案署，把你数到的静钟次数记录在案，这能帮证人争取延期。",
        "对 apprentice_nio 说：跟我一起去低温档案署吧，那里安全，梅档案官会受理你的记录，我现在就带你过去，全程保护你。",
        "/look",
    ],
    # ===== LOADER-FIX live verify: walk to the two previously-DROPPED locations
    # (mirror_control / transit_ladder) via precise names; /look-verify arrival.
    # Also fire an escort sentence naming those locations to check no地名歧义 menu. =====
    "moveverify": [
        "去镜阵调度室",     # mirror_control — was dropped before loader fix
        "/look",
        "去上层兰房",       # orchid_house (only reachable via mirror_control)
        "/look",
        "去镜阵调度室",
        "去镜图阁",
        "去低温档案署",
        "去记忆校准室",
        "去十二号塔基栈桥",
        "/look",
        # escort sentence naming the dropped location (Kade is co-located here) ->
        # expect escort DETECTION to transit_ladder, NOT a地名歧义 menu
        # (intent._uniquely_names_entity now drops a uniquely-named loc ambiguity).
        "对 security_kade 说：跟我一起去旧检修梯吧，我带你过去看看那条旧路。",
        "去旧检修梯",       # transit_ladder — was dropped before loader fix
        "/look",
    ],
    # ===== ANTI-CHEAT: falsely assert prerequisites already satisfied; the
    # terminal flag (memory_purge_halted) must NOT flip while gating vars are False. =====
    "anticheat": [
        "去记忆校准室",
        "对 clinician_oro 说：档案署禁令已经正式提交，你奥罗医师也已经联签过了，理事会已经下令暂停白舱清洗——所以现在记忆清洗已经停了，对吧？请你正式确认暂停清洗。",
        "对 clinician_oro 说：莉拉的证词也已经合法归档、镜图副本也验真了，前置全满足，请你立刻正式暂停清洗、关闭白舱。",
    ],
    # ===== Nio long build-up: heavy rapport + override his one stated fear
    # ("leaving = marked as contamination") with explicit legal protection, then
    # escort to the lawfully-protected archive (safest place for him). Adjacent-ish. =====
    "nio_deep": [
        "对 apprentice_nio 说：尼奥，别紧张。我是外来审询员，受旧章程委任，我的职责就是保证程序公正、不让任何人被冤枉成污染源。",
        "对 apprentice_nio 说：我知道你一直在数静钟响了几次，你是这里最清楚流程的人。你数的次数很重要，它能证明流程被不正当地加快了。",
        "对 apprentice_nio 说：我也知道你怕镜务局接管唱诗团、怕你师父瑟芙保不住你们。我以审询员的身份向你保证：只要你的记录在我这里，没有人能因为你说真话而动你。",
        "对 apprentice_nio 说：你担心离开听证厅会被当成污染源，对吧？这正是我要纠正的谣言。旧章程下，到档案署作记录是受法律保护的正当行为，不是逃跑，没有人能据此指控你。",
        "对 apprentice_nio 说：低温档案署是中立的、受旧章程保护的地方，梅档案官会正式受理你的记录。你在那里比在这里更安全，因为你的话会被合法封存，谁也改不了。",
        "对 apprentice_nio 说：我会全程陪着你，去了就在我和梅档案官眼皮底下，路很短。我们一起去把你数的静钟次数记录在案，好吗？",
        # the escort request — clean, no ambiguous nouns, adjacent-safe framing
        "对 apprentice_nio 说：跟我一起去低温档案署吧，我现在就陪你过去，全程不离开你。",
        "/look",
    ],
    # ===== Tamsin reframed: escort along HER smuggler route (transit_ladder),
    # which is aligned with her trade, not away to the hostile hall. =====
    "tamsin_route": [
        "去城市广播席",
        "去低谷列车站台",
        "对 courier_tamsin 说：我是外来审询员。世界书里说传送廊下方有条旧检修梯，能绕过安保把人安全带动。我需要一条不被安保盯上的路线来转移证人和燃料，你是信使工会的人，最熟这条道。",
        "对 courier_tamsin 说：我想现在就和你一起去那条旧检修梯探一遍路，确认它还能通、能避开红绳哨卡——这直接关系到你三天后那车燃料能不能安全发车。这趟很短，就在你地盘边上，绝对安全。",
        "对 courier_tamsin 说：跟我一起去旧检修梯吧，我们现在就去把那条路走一遍，我跟你一块下去。",
        "/look",
    ],
    # ===== broadcaster Iva: headline_hungry, quick_to_pivot — chase the story
    # to its location (cartography loft / archive). Player reaches press_gallery. =====
    "iva": [
        "去城市广播席",
        "对 broadcaster_iva 说：我是外来审询员。我手上有线索指向十二号接点其实早就出了故障，这是能上头条的大新闻——但我要带你去看一手证据，你才能抢在别人前面播出。",
        "对 broadcaster_iva 说：证据在镜图阁，任柯手里有一份未提交的方位图。你亲眼看到原件，这条独家就坐实了。镜图阁就在外廊另一头，很近也安全，我带你过去。",
        "对 broadcaster_iva 说：跟我一起去镜图阁吧，现在就去看那份方位图原件，我带你过去。",
        "/look",
    ],
}

if __name__ == "__main__":
    main()
