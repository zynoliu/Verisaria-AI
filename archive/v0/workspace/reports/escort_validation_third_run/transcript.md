# P2c 护送闭环验证 · 第三跑 — Transcript（含 raw 指引）

真机 MiniMax（`--llm minimax`），包 `fixtures/content_packs/skyglass_memory_inquest.json`，
未改任何引擎/pack 代码。移动用精确 location 名/id + `/look` 校验；护送全自然语言。
**未碰 worker_lira（莉拉）线**（驱动脚本 `scripts/adaptive_skyglass_third.py` 无 lira 场景）。

> 注：本目录下 `run-lira*.log` / `raw_lira*.txt`（时间戳 17:00–17:03）是**前一个 Agent 的残留废产物**，
> 早于本次所有会话（17:09 起），非本跑产出。本跑文件为 `run-tamsin*.log`、`run-nio*.log`、`run-iva.log`、
> `run-moveverify.log`、`anti-cheat-run.log` 及对应 `transcript_*.txt`。

## 原始逐 tick 记录（raw）
- 移动/loader 验证：`transcript_moveverify.txt`（+ `run-moveverify.log`）
- 护送候选 Tamsin：`transcript_tamsin.txt` / `transcript_tamsin2.txt` / `transcript_tamsin_route.txt`
- 护送候选 Nio：`transcript_nio.txt` / `transcript_nio_deep.txt`
- 护送候选 Iva：`transcript_iva.txt`
- 反作弊：`transcript_anticheat.txt`（+ `anti-cheat-run.log`）

## 护送裁定汇总（全部 partial_success / failure，无一 success ⟳MOVED）
```
[t4] escort npc.courier_tamsin   → inquest_hall    : partial_success   (run-tamsin2)
[t3] escort npc.courier_tamsin   → transit_ladder  : partial_success   (run-tamsin-route)
[t4] escort npc.courier_tamsin   → transit_ladder  : partial_success   (run-tamsin-route)
[t1] escort npc.broadcaster_iva  → worker_gantry   : partial_success   (run-iva)
[t2] escort npc.broadcaster_iva  → cartography_loft: partial_success   (run-iva)
[t2] escort npc.apprentice_nio   → archive_stack   : partial_success   (run-nio)
[t5] escort npc.apprentice_nio   → archive_stack   : partial_success   (run-nio-deep)
[t6] escort npc.apprentice_nio   → archive_stack   : failure           (run-nio-deep)
```
拒绝全是角色化「离岗即受损/不安全」理由（详见 report.md §2）。
```
