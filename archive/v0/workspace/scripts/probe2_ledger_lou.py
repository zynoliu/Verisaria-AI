"""Probe2 — strict-discipline rerun: pin down charcoal_ledger_obtained (real MiniMax).

Single goal: with the player ACTUALLY at tally_house and 商会账房娄 confirmed present,
issue the imperative keyword request for the zero-prereq evidence var
`charcoal_ledger_obtained` and observe: True flip vs arbiter-injected prerequisite.

Driver discipline (this is what the two previous runs failed on):
  1. Move only with exact location names ("去 商会账房"); after EVERY move tick,
     verify snapshot.location.id; if a ClarificationNeeded menu pops, parse the
     options and answer with the matching NUMBER until arrival.
  2. Never speak to an NPC before snapshot.present confirms they are here.
  3. Player never self-identifies as 勘瓷/勘瓷使; request lines contain only the
     target NPC's form of address + var request keywords.
  4. Natural language only, no /inject. Flush transcript every beat; write a
     preliminary report-probe2.md immediately after the CORE beat.
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
from verisaria.protocol.engine_session import EngineSession

PACK = "fixtures/content_packs/emberfall_kiln_assize.json"
OUTDIR = ROOT / "reports" / "grand_integration_pack"
OUTDIR.mkdir(parents=True, exist_ok=True)
LOGF = OUTDIR / "probe2.log"
TRANS = OUTDIR / "probe2_transcript.md"
REPORT = OUTDIR / "report-probe2.md"

fh = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
for nm in ("verisaria", "verisaria.channel_c", "verisaria.relationship"):
    lg = logging.getLogger(nm); lg.setLevel(logging.INFO); lg.addHandler(fh)

class Ring(logging.Handler):
    def __init__(self): super().__init__(); self.buf = []
    def emit(self, rec): self.buf.append(self.format(rec))
ring = Ring(); ring.setFormatter(logging.Formatter("%(name)s %(levelname)s %(message)s"))
logging.getLogger("verisaria.channel_c").addHandler(ring)
logging.getLogger("verisaria").addHandler(ring)

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()

FALLBACK_COUNT = 0
TICK_NO = 0
CORE_EVIDENCE: list[str] = []   # raw log lines from the core beat

def wvars_str(s):
    return "\n".join(
        f"    - [{v.var_id}] {('★' if v.var_id=='charcoal_ledger_obtained' else '')}"
        f"{v.label[:40]}… = {v.value}"
        + (" (dynamic)" if v.dynamic else "")
        + (f" (pend{v.pending_in})" if v.pending_in else "")
        for v in s.world_vars)

def present_str(s):
    return ", ".join(f"{e.name}({e.id})" for e in s.present) or "(无人)"

def rel_str(s):
    out = []
    for r in s.relationships:
        ds = "; ".join(f"{d.dimension}={d.value:.2f}({d.band})" for d in r.descriptors) if r.descriptors else ""
        out.append(f"    - {r.name}({r.npc_id}): {ds}")
    return "\n".join(out) or "    (无)"

RESULT = {}
def raw_tick(es, text):
    RESULT.clear()
    def runner():
        try:
            RESULT['r'] = es.submit(P.SubmitInput(text=text))
        except Exception:
            import traceback; RESULT['err'] = traceback.format_exc()
    th = threading.Thread(target=runner, daemon=True); th.start()
    th.join(timeout=90)
    if th.is_alive(): RESULT['timeout'] = True
    return dict(RESULT)

def grep_ring():
    return [ln for ln in ring.buf if any(k in ln for k in (
        "world-change", "什么也没发生", "new_prerequisite", "ledger", "partial",
        "FALLBACK", "apprais", "sufficiency", "insufficient", "充分",
        "world-changes applied"))]

def beat(es, text, tag, core=False):
    """One logged tick with full dumps. Returns the TickResult or None."""
    global TICK_NO, FALLBACK_COUNT
    TICK_NO += 1
    ring.buf.clear()
    t0 = time.time()
    r = raw_tick(es, text)
    dt = time.time() - t0
    w("\n" + "=" * 80)
    w(f"## 拍 {TICK_NO} — [{tag}]{' ★核心拍' if core else ''}")
    w(f"> {text}")
    if r.get('timeout'):
        w("\n**[WATCHDOG TIMEOUT >90s — skipped]**"); return None
    if r.get('err'):
        w("\n**[EXCEPTION]**\n```\n" + r['err'] + "\n```"); return None
    res = r['r']; s = res.snapshot
    w(f"\n_位置_: {s.location.name}({s.location.id})  {s.time_of_day} {s.clock}")
    w(f"_在场_: {present_str(s)}")
    clar_opts = None
    for ev in res.events:
        if isinstance(ev, P.NpcSpoke):
            w(f"\n**{ev.name}**: {ev.line}")
        elif isinstance(ev, P.WorldVarChanged):
            w(f"\n_WORLD变化(event)_: [{ev.var_id}] = {ev.value}")
        elif isinstance(ev, P.StanceConfirmed):
            w(f"\n_立场确认_: {ev.label}")
        elif isinstance(ev, P.ClarificationNeeded):
            clar_opts = ev.options
            w(f"\n_澄清菜单_: {ev.question}")
            for i, o in enumerate(ev.options, 1):
                w(f"    {i}. {o}")
        elif isinstance(ev, P.Notice):
            w(f"\n_Notice_: {ev.text}")
    if res.text and res.text.strip():
        w(f"\n_引擎返回_: {res.text.strip()[:600]}")
    w("\n_/world 全量_:")
    w(wvars_str(s))
    w("\n_关系快照_:")
    w(rel_str(s))
    hits = grep_ring()
    w("\n_log grep [world-change/new_prerequisite/ledger/partial/FALLBACK/appraise]_:")
    if hits:
        for ln in hits:
            w(f"    | {ln[:400]}")
    else:
        w("    | (该 tick 日志无以上标记)")
    fb = sum(1 for ln in ring.buf if "FALLBACK" in ln)
    if fb:
        FALLBACK_COUNT += fb
        w(f"\n_⚠FALLBACK 本拍 {fb} 次_")
    w(f"\n_(tick {dt:.1f}s)_")
    tf.flush()
    if core:
        CORE_EVIDENCE.extend(hits)
        CORE_EVIDENCE.append(f"snapshot charcoal_ledger_obtained = {var_value(s)}")
    return res

def var_value(s, vid="charcoal_ledger_obtained"):
    for v in s.world_vars:
        if v.var_id == vid:
            return v.value
    return "(var不存在)"

def is_true(val):
    return val is True or (isinstance(val, str) and val.lower() == "true")

def clar_event(res):
    if res is None: return None
    for ev in res.events:
        if isinstance(ev, P.ClarificationNeeded):
            return ev
    return None

def ensure_at(es, loc_id, loc_name):
    """Move with strict discipline: exact name, parse menus by number, verify
    snapshot.location.id after every tick. Returns final snapshot or None."""
    for attempt in range(3):
        s = es.snapshot()
        if s.location.id == loc_id:
            w(f"\n_[移动核对] 已在 {loc_name}({loc_id})，在场: {present_str(s)}_")
            return s
        res = beat(es, f"去 {loc_name}", f"移动→{loc_name} (尝试{attempt+1})")
        # menu resolution loop
        for _ in range(3):
            ev = clar_event(res)
            if ev is None or not ev.options:
                break
            idx = next((i for i, o in enumerate(ev.options) if loc_name in o), None)
            if idx is None:
                idx = next((i for i, o in enumerate(ev.options) if "取消" in o), 0)
            w(f"\n_[菜单解析] 选编号 {idx+1} = {ev.options[idx]}_")
            res = beat(es, str(idx + 1), f"菜单选{idx+1}→{loc_name}")
        s = es.snapshot()
        if s.location.id == loc_id:
            w(f"\n_[移动核对 ✓] 到位 {loc_name}({loc_id})，在场: {present_str(s)}_")
            return s
        w(f"\n_[移动核对 ✗] 仍在 {s.location.name}({s.location.id})，重试_")
    return None

def npc_present(s, npc_id):
    return any(e.id == npc_id for e in s.present)

def write_prelim_report(core_lines, arrived, present_line, val, extra=""):
    REPORT.write_text(
        "# probe2 报告（核心拍即时落盘版）— emberfall_kiln_assize\n\n"
        f"- 玩家到账房 tally_house：**{'是' if arrived else '否'}**\n"
        f"- 核心拍时 `_在场_`：{present_line}\n"
        f"- ★核心拍后 `charcoal_ledger_obtained` = **{val}**\n\n"
        "## 核心拍原始证据（world-change / new_prerequisite / ledger）\n"
        + "\n".join(f"    | {ln[:500]}" for ln in core_lines) + "\n\n"
        + extra
        + "\n\n(本文件为核心拍后立即落盘的初版，终版在 probe 跑完后覆盖。)\n",
        encoding="utf-8")

def main():
    es = EngineSession(GameSession(PACK, save_dir="_probe2_saves", llm_backend="minimax"))
    s0 = es.snapshot()
    w("# probe2 transcript — 严纪律重跑：账房娄零前置物证判据\n")
    w(f"包: {PACK}（真机 MiniMax，未注入，无 /inject）")
    w(f"开局位置: {s0.location.name}({s0.location.id})  {s0.time_of_day} {s0.clock}")
    w(f"开局在场: {present_str(s0)}")
    w("\n目标: charcoal_ledger_obtained (set_by merchant_authority=npc.factor_lou @ tally_house)")
    w("关键词: 交出私账/给我炭账/官炭私运账/…/把账册交给勘瓷")
    w("\n开局 /world:")
    w(wvars_str(s0))
    tf.flush()

    # —— 1. 移动 assize_hall → potters_row → tally_house，每跳核对 ——
    s = ensure_at(es, "potters_row", "窑户巷")
    if s is None:
        w("\n**[ABORT] 第一跳未到窑户巷**"); finish(False, "(未到)", "未送达", ""); return
    s = ensure_at(es, "tally_house", "商会账房")
    if s is None:
        w("\n**[ABORT] 第二跳未到商会账房**"); finish(False, "(未到)", "未送达", ""); return

    arrived = s.location.id == "tally_house"
    lou_here = npc_present(s, "npc.factor_lou")
    present_line = present_str(s)
    w(f"\n_[到位判定] tally_house={arrived}, 娄在场={lou_here}_")
    if not lou_here:
        # one wait beat in case of rhythm, then re-check
        res = beat(es, "我在账房里站定，环顾四周。", "原地观察等娄")
        s = es.snapshot(); lou_here = npc_present(s, "npc.factor_lou")
        present_line = present_str(s)
        w(f"\n_[二次判定] 娄在场={lou_here}_")
    if not lou_here:
        w("\n**[ABORT] 娄不在账房，核心判据无法送达**")
        finish(arrived, present_line, "未送达(娄不在场)", ""); return

    # —— 2. 台阶拍（不提别人，不自称勘瓷）——
    beat(es, "对商会账房娄说：娄账房，我不写你的名字，账目来历也只字不提你，出了事我一人担着。",
         "台阶(娄)")

    # —— 3. ★核心拍：祈使 + 命中 request_keywords ——
    res = beat(es, "对商会账房娄说：娄账房，请把那本官炭私运账交给勘瓷。",
               "祈使+关键词·索要炭账", core=True)
    s = es.snapshot()
    val = var_value(s)
    write_prelim_report(CORE_EVIDENCE, arrived, present_line, val)
    w(f"\n_[核心拍后 charcoal_ledger_obtained = {val}]_（初版 report-probe2.md 已落盘）")

    # 若核心拍本身撞澄清菜单（如 '勘瓷' 歧义）：选『尝试执行』；再不行换不含勘瓷的关键词句
    ev = clar_event(res)
    if ev and ev.options:
        idx = next((i for i, o in enumerate(ev.options) if "尝试执行" in o), None)
        if idx is not None:
            w(f"\n_[菜单解析·核心拍] 选编号 {idx+1} = 尝试执行_")
            beat(es, str(idx + 1), "核心拍·尝试执行", core=True)
        else:
            beat(es, "对商会账房娄说：娄账房，请把那本官炭私运账交出来。",
                 "核心拍重发(去掉勘瓷)", core=True)
        s = es.snapshot(); val = var_value(s)
        write_prelim_report(CORE_EVIDENCE, arrived, present_line, val,
                            "（核心拍曾弹澄清菜单，已按编号/改写重发。）")

    # —— 4. 若 partial：追 1–2 拍直击它要的东西（台阶/保障），看给不给 ——
    if not is_true(val):
        beat(es, "对商会账房娄说：娄账房，账册我贴封条原样取证，画押来历只字不落你名，"
                 "若日后有人追问，我当面认下是我强索的——现在请把官炭私运账交出来。",
             "追拍1·直给台阶保障", core=True)
        s = es.snapshot(); val = var_value(s)
        if not is_true(val):
            beat(es, "对商会账房娄说：娄账房，你要的护身承诺我都给了。给我炭账，"
                     "那本官炭私运账，现在交到我手上。",
                 "追拍2·再祈使关键词", core=True)
            s = es.snapshot(); val = var_value(s)
        write_prelim_report(CORE_EVIDENCE, arrived, present_line, val,
                            "（含追拍：直击台阶/保障后的结果。）")

    # —— 5. （可选）若翻 True：单跳 guild_loft 用炭账撬阔 ——
    if is_true(val):
        s2 = ensure_at(es, "guild_loft", "窑监阁")
        if s2 is not None and npc_present(s2, "npc.warden_kuo"):
            beat(es, "对窑监阔说：阔窑监，官炭私运账已在我手上，画押俱全。"
                     "我不深究你个人、容你将功折罪——请你当众承认私运龙骨土、公开窑变真因。",
                 "杠杆·撬阔(kiln_fault_disclosed)")
            s3 = es.snapshot()
            w(f"\n_[撬阔后 kiln_fault_disclosed = {var_value(s3, 'kiln_fault_disclosed')}]_")

    finish(arrived, present_line, val, "")

def finish(arrived, present_line, val, note):
    w("\n" + "=" * 80)
    w(f"\n## 终局\n- 到账房: {arrived}\n- 在场: {present_line}\n"
      f"- charcoal_ledger_obtained: {val}\n- FALLBACK 总数: {FALLBACK_COUNT}\n- 总拍数: {TICK_NO}\n{note}")
    tf.close()

if __name__ == "__main__":
    main()
