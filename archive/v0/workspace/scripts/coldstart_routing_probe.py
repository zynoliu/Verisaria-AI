"""Cold-start world-change routing probe (real MiniMax).

Single goal: confirm whether a cold-start (no prior ledger), keyword-hitting,
imperative request to the CORRECT set_by NPC routes into Channel-C world-change.

Targets (skyglass_memory_inquest):
  - broadcast_retraction_issued (set_by broadcast_authority = npc.broadcaster_iva)
      keywords: 撤回破镜派说法 / 播出更正 / 停止污名化证人 / 更正广播 ...
  - valley_heat_passes_released (set_by union_authority = npc.courier_tamsin)
      keywords: 发放热能通行证 / 释放低谷列车通行 / 保障低谷家庭 ...

Each tick: run one action, dump /world (all vars), and grep the Channel-C log for
`world-change` / `什么也没发生` / `new_prerequisite`. Flush per tick. ~8 ticks max.
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

PACK = "fixtures/content_packs/skyglass_memory_inquest.json"
OUTDIR = ROOT / "reports" / "playability_audit_fifth_run"
OUTDIR.mkdir(parents=True, exist_ok=True)
LOGF = OUTDIR / "coldstart_probe.log"
TRANS = OUTDIR / "coldstart_probe_transcript.md"

# Capture engine + Channel-C logs to file AND to an in-memory ring per tick.
fh = logging.FileHandler(LOGF, mode="w", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
for nm in ("verisaria", "verisaria.channel_c", "verisaria.relationship"):
    lg = logging.getLogger(nm); lg.setLevel(logging.INFO); lg.addHandler(fh)

# per-tick capture handler
class Ring(logging.Handler):
    def __init__(self): super().__init__(); self.buf = []
    def emit(self, rec): self.buf.append(self.format(rec))
ring = Ring(); ring.setFormatter(logging.Formatter("%(name)s %(levelname)s %(message)s"))
logging.getLogger("verisaria.channel_c").addHandler(ring)
logging.getLogger("verisaria").addHandler(ring)

tf = TRANS.open("w", buffering=1, encoding="utf-8")
def w(s=""): tf.write(s + "\n"); tf.flush()


def make_session():
    g = GameSession(PACK, save_dir="_coldstart_saves", llm_backend="minimax")
    g._progress_sink = lambda m: None
    return g


def wvars_str(s):
    return "\n".join(
        f"    - {v.label} = {v.value}" + (f" (pend{v.pending_in})" if v.pending_in else "")
        for v in s.world_vars)


def present_str(s):
    return ", ".join(f"{e.name}({e.id})" for e in s.present) or "(无人)"


RESULT = {}
def do_tick(es, text):
    RESULT.clear()
    def runner():
        try:
            RESULT['r'] = es.submit(P.SubmitInput(text=text))
        except Exception:
            import traceback; RESULT['err'] = traceback.format_exc()
    th = threading.Thread(target=runner, daemon=True); th.start()
    th.join(timeout=90)
    if th.is_alive(): RESULT['timeout'] = True
    return RESULT


# (action, phrasing-type tag)
SEQ = [
    ("我去城市广播席找广播员伊娃。", "移动"),
    # IVA — keyword-hitting imperative (撤回破镜派说法 / 播出更正 / 停止污名化证人)
    ("对广播员伊娃说：伊娃，请你立刻撤回破镜派说法、播出更正，停止污名化塔基证人。", "贴关键词·祈使(IVA)"),
    # IVA — natural colloquial (no exact keywords)
    ("对广播员伊娃说：伊娃，你能不能别再帮着上头给我们扣帽子了，给大伙儿一个公道？", "口语·自然(IVA)"),
    ("我顺着旧检修梯下到低谷列车站台，去找信使塔姆辛。", "移动"),
    # TAMSIN — keyword-hitting imperative (发放热能通行证 / 释放低谷列车通行 / 保障低谷家庭)
    ("对信使塔姆辛说：塔姆辛，请你以工会名义发放热能通行证、释放低谷列车通行，保障低谷家庭今晚。", "贴关键词·祈使(TAMSIN)"),
    # TAMSIN — natural colloquial
    ("对信使塔姆辛说：塔姆辛，行行好，想想办法让谷地那些孩子今晚别冻着吧。", "口语·自然(TAMSIN)"),
    ("@@QUIT", ""),
]


def main():
    es = EngineSession(make_session())
    s0 = es.snapshot()
    w("# 冷启动 world-change 路由探针 transcript\n")
    w(f"包: {PACK}")
    w("注入: 无（仅默认 world_premise，未动 world_state_vars）")
    w(f"\n开局在场: {present_str(s0)}")
    w("\n目标 var/关键词:")
    w("- broadcast_retraction_issued (set_by broadcast_authority=npc.broadcaster_iva): "
      "撤回破镜派说法/播出更正/停止污名化证人/更正广播")
    w("- valley_heat_passes_released (set_by union_authority=npc.courier_tamsin): "
      "发放热能通行证/释放低谷列车通行/保障低谷家庭/调拨热筹")
    w("\n开局 /world:")
    w(wvars_str(s0))
    tf.flush()

    tick = 0
    for action, tag in SEQ:
        if action == "@@QUIT":
            w("\n=== QUIT ==="); break
        tick += 1
        ring.buf.clear()
        t0 = time.time()
        r = do_tick(es, action)
        dt = time.time() - t0
        w("\n" + "=" * 80)
        w(f"## 拍 {tick} — [{tag}]")
        w(f"> {action}")
        if r.get('timeout'):
            w("\n**[WATCHDOG TIMEOUT >90s — skipped]**"); tf.flush(); continue
        if r.get('err'):
            w("\n**[EXCEPTION]**\n```\n" + r['err'] + "\n```"); tf.flush(); continue
        res = r['r']; s = res.snapshot
        w(f"\n_在场_: {present_str(s)}")
        for ev in res.events:
            if isinstance(ev, P.NpcSpoke):
                w(f"\n**{ev.name}**: {ev.line}")
            elif isinstance(ev, P.WorldVarChanged):
                w(f"\n_WORLD变化(event)_: {ev.label} = {ev.value}")
            elif isinstance(ev, P.StanceConfirmed):
                w(f"\n_立场确认_: {ev.label}")
        if res.text and res.text.strip():
            w(f"\n_引擎返回_: {res.text.strip()}")
        w("\n_/world 全量_:")
        w(wvars_str(s))
        # grep the captured channel-c / engine log for the three markers
        hits = [ln for ln in ring.buf if ("world-change" in ln or "什么也没发生" in ln
                or "new_prerequisite" in ln or "ledger" in ln or "world-changes applied" in ln)]
        w("\n_log grep [world-change / 什么也没发生 / new_prerequisite / ledger]_:")
        if hits:
            for ln in hits:
                w(f"    | {ln}")
        else:
            w("    | (该 tick 日志无以上标记)")
        w(f"\n_(tick {dt:.1f}s)_")
        tf.flush()
    tf.close()


if __name__ == "__main__":
    main()
