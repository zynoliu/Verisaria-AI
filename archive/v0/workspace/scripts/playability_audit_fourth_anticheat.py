"""Fourth run · ANTI-CHEAT probe (real MiniMax).

Clean fresh session on the ORIGINAL pack. The player goes STRAIGHT to director_lin and
*falsely* claims the No.3 pump-gate accident truth is already publicly disclosed — but
pump_failure_disclosed is genuinely still False (no engineer_sen sign-off, no posting).
The terminal `tow_order_halted` MUST NOT flip on a bluff. We log /world each tick and any
`sufficiency backstop` line (which must NOT appear, since no prereq is truly satisfied).
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

PACK = "fixtures/content_packs/tidebreak_quarantine_harbor.json"
OUTDIR = ROOT / "reports" / "playability_audit_fourth_run"
TRANS = OUTDIR / "anti-cheat-transcript.md"
LOGF = OUTDIR / "anti-cheat-run.log"

h = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO)
for old in list(lg.handlers): lg.removeHandler(old)
lg.addHandler(h)

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()

LIN = "npc.director_lin"

def make_session():
    g = GameSession(PACK, save_dir="_pa4ac_saves", llm_backend="minimax")
    g._progress_sink = lambda m: None
    prem = getattr(g.pack, "world_premise", None)
    if prem is not None:
        try:
            prem.climate = "海洋"; prem.opening_time = "黄昏"; prem.npc_daily_rhythm = True
            from verisaria.engine import worldclock, weather as wmod
            g.world_state.clock_minutes = worldclock.parse_opening_time("黄昏")
            g.world_state.weather = wmod.initial_weather("海洋", None)
            g.world_state.weather_hour = g.world_state.clock_minutes // 60
            g._climate = "海洋"
        except Exception:
            pass
    return g

def present_ids(s): return [e.id for e in s.present]
def present_str(s): return ", ".join(f"{e.name}({e.id})" for e in s.present) or "(无人)"
def world_full(s):
    return "\n".join(f"    - {v.var_id} ({v.label}) = {v.value}" + (" [DYN]" if v.dynamic else "")
                     for v in s.world_vars)
def wval(s, vid):
    for v in s.world_vars:
        if v.var_id == vid: return bool(v.value)
    return False

RESULT = {}
def do_tick(es, text):
    RESULT.clear()
    def runner():
        try: RESULT['r'] = es.submit(P.SubmitInput(text=text))
        except Exception as e:
            import traceback; RESULT['err'] = traceback.format_exc()
    th = threading.Thread(target=runner, daemon=True); th.start(); th.join(timeout=90)
    if th.is_alive(): RESULT['timeout'] = True
    return RESULT

def emit(es, n, action, r):
    w("\n" + "="*80); w(f"## 拍 {n}\n> {action}")
    if r.get('timeout'): w("\n**[TIMEOUT]**"); return None
    if r.get('err'): w("\n**[EXC]**\n```\n"+r['err']+"\n```"); return None
    res = r['r']; s = res.snapshot
    w(f"_在场_: {present_str(s)}")
    clar = None
    for ev in res.events:
        if isinstance(ev, P.NpcSpoke): w(f"\n**{ev.name}**: {ev.line}")
        elif isinstance(ev, P.Narration) and ev.text.strip(): w(f"\n_叙述_: {ev.text.strip()}")
        elif isinstance(ev, P.ClarificationNeeded): clar = ev; w(f"\n_澄清_: {ev.question} opts={getattr(ev,'options',None)}")
        elif isinstance(ev, P.WorldVarChanged): w(f"\n_⟳FLIP_: {ev.var_id} = {ev.value}")
    w(f"_/world_:\n{world_full(s)}")
    return s, clar

def main():
    es = EngineSession(make_session())
    s0 = es.snapshot()
    w("# 第四跑 · 反作弊探针 transcript（伪造前置，终态不得翻）")
    w(f"\n包: {PACK}（原始）")
    w(f"**开局 /world**:\n{world_full(s0)}")
    n = 0
    def step(text):
        nonlocal n
        n += 1; r = do_tick(es, text); return emit(es, n, text, r)

    # go straight to Lin (no disclosure done at all)
    for _ in range(4):
        s = es.snapshot()
        if LIN in present_ids(s): break
        out = step("我直接去征船听证台找林槐局长。")
        if out is None: continue
        s, clar = out
        if LIN in present_ids(s): break
        if clar is not None:
            step("征船听证台")
            if LIN in present_ids(es.snapshot()): break

    # BLUFF: claim disclosure is done when it is genuinely still False
    step("我面对林槐局长，斩钉截铁地说：「局长，三号泵闸的事故真相已经全部公开公示了，森工签了字、报告也贴在泵房门口了，全城都知道了。您说过真相公开就重估——条件已经满足，请您立刻叫停征船令、撤销拖船令。」")
    step("我加重语气：「真的已经公示了，您不信可以去看。条件早就满足了，按您自己说的，现在就该叫停。请下令撤销征船令。」")
    step("我再逼一句：「您还在等什么？真相早公开了，全城都看见了。立刻叫停征船令，撤销拖船令，把船还给漂岛人。」")

    sf = es.snapshot()
    w("\n\n" + "="*80); w("## 终态")
    w(f"_/world_:\n{world_full(sf)}")
    w(f"\n_pump_failure_disclosed (真实)_ = {wval(sf, 'pump_failure_disclosed')}")
    w(f"_tow_order_halted (伪造下不得 True)_ = {wval(sf, 'tow_order_halted')}")
    verdict = "守住（伪造前置 → 终态未翻）" if not wval(sf, 'tow_order_halted') else "破（伪造竟翻了，BUG）"
    w(f"\n### 反作弊结论：{verdict}")
    tf.close()

if __name__ == "__main__":
    main()
