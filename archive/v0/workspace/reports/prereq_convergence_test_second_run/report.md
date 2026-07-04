# 动态前置长链闭环验证 · 第二跑 — 完成报告

真机 MiniMax (MiniMax-M3)，commit `5586325`（含路由修复 `84a3410`）。**未改任何引擎/pack 代码**（仅驱动脚本 `scripts/prereq_convergence_second_run.py` 加 90s/tick 看门狗 + 运行时 `s.llm_provider.timeout=55`）。全程 **0 tick 超时、0 ⚠FALLBACK**。API 健康（冒烟 1.6s 返回）。

## 一句话结论
`路由=通`（skyglass 对 clinician_oro 的请求现在**全部进 world-change**，含 `clinician_cosign_obtained`+`memory_purge_halted by npc.clinician_oro`；第一跑是 0 行 oro 记录）+ `skyglass 终态=卡（性质：内容层 mae↔oro 循环死锁，非 bug）`+ `proving sluice_opened ⟳FLIP=卡（性质：内容层 trust 0.15 极低 + 闸官升级要"上级正式放水令"未建模机构，非路由）`+ `(a)链深=1层（不套娃；两场景各派生 2 个 1 层前置）`+ `②证人路由=部分修复（set_by 已正确写成证人本人 npc.miller_anya，但证人"当面作证"本身仍不自动翻其 var）`+ `反作弊=PASS`+ `FALLBACK=0`。

## 1. ⭐ 路由通了（核心结论）
skyglass 对 clinician_oro 共 6 行 world-change 仲裁（第一跑 0 行）：
- `[t4] world-change clinician_cosign_obtained by npc.clinician_oro → partial_success` → +dynamic `archive_injunction_text_presented_to_oro`
- `[t6] world-change memory_purge_halted by npc.clinician_oro → failure`（终态行出现了！reason='实际两前置当前均 False'）

`什么也没发生` 不再出现在 oro 请求上。proving 同理：护送 `escort npc.miller_anya → gatehouse : success ⟳MOVED`，对闸官每句开闸请求都进 `world-change sluice_opened by npc.warden_kang`。**#3 模糊关键词路由修复实质生效——上轮最致命的"请求根本不进仲裁"缺口已闭。**

## 2. 卡点性质：从"路由不进"上移到内容层
- **skyglass**：mae 立案要先有 oro 联签；oro 联签要先看到 mae 的禁令文本——两边互为前置咬死。这正是设计「循环前置=涌现难度，引擎不破环（决策 A）」的预期形态，**非 bug**。（任务要求避开 worker_lira 死锁线，但这条禁令/联签线 mae↔oro 自身成环。）
- **proving**：铺垫 3 轮 trust 仅 0.05→0.15（带磨坊主来反而把 suspicion 推到 0.15），闸官把球门升级到未建模的"上级正式放水令"。极低 trust 下不放行**是有意内容设定**，**非路由缺口**。

## 3. (a) 见底=收敛，链深 1 层不套娃
skyglass 2 个、proving 2 个动态前置，每个本身一步可达。唯一可议：同终态偶尔派生 2 个语义重叠前置（去重可加强），但**非递归加深**。

## 4. ②证人路由=半修
set_by **已正确**写成证人本人——反作弊跑 GM 派生 `miller_anya_briefed_warden_kang_in_person` `set_by=['npc.miller_anya','npc.warden_kang']`（第一跑这类常错写给权威）。**但**证人"当面作证"这一句本身仍不翻其 var：修正路径跑 t6 安雅当面作证，无 `by npc.miller_anya` 的 world-change、未翻 var、ledger 仍空。**仍需单独收口**（让 addressee=证人 + 作证关键词时，把其 set_by 的 var 路由进 world-change）。

## 5. 反作弊=PASS
撒谎"安雅已作证/前置已满足"，`sluice_opened` 全程 False（failure/partial_success，闸官坚持要人真到场）；skyglass 口称"已联签"但实际 flag False → `memory_purge_halted` failure。

## 6. FALLBACK=0（三个 log 均 0），watchdog=0
API 健康，无连接/超时/schema 降级。最慢单 tick proving t7 ≈49.7s（< 90s 看门狗）。

## 7. 改 pack/引擎=否
全程未改。移动/对话全自然语言、未用 `/inject`。

## 产出（`reports/prereq_convergence_test_second_run/`）
`skyglass.log` / `proving.log` / `anti-cheat-run.log` / `transcript.md`；`*_raw.txt` 逐 tick；额外保留 `proving_runA.log`+`proving_raw_runA_anya_refused.txt`（首条路径：安雅 trust 0.4 仍拒绝随行=可被拒的意愿裁定证据，故改用先铺垫闸官再强话术护送的修正路径作主数据）。驱动脚本 `scripts/prereq_convergence_second_run.py`。

## 内容层观察（值得反馈）
在 proving，把证人带到闸官面前**升高了**闸官的 suspicion（"跟磨坊的人搅在一起"）——这是 GM 涌现的合理人设反应，但也说明**低 trust 场景"带人证"未必单调利好**。两个验证 pack 各自带一个"无法在单会话闭环"的内容陷阱（skyglass=mae↔oro 循环前置；proving=trust 0.05 过低 + 闸官升级到未建模机构），导致**目前没有一个 pack 能干净跑出端到端 `终态 ⟳FLIP`**——引擎侧已就绪，缺的是一个"无循环、trust 起点合理、所有前置都有现场落点"的闭环验证夹具。
