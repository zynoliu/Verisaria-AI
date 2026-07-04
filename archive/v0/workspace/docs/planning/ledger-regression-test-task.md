# 测试任务：涌现事实账本 —— 第二轮回归（多 NPC 闭环 + 反作弊）

> 给测试 Agent 的任务简报。配套设计见 [docs/design/emergent-fact-ledger.md](../design/emergent-fact-ledger.md)；
> 第一轮单链闭环已通过，见 `reports/skyglass_ledger_closure_test/`。

## 目标

确认账本既能"记住该记的"，也"不会变成玩家说啥都成立"。两件**互补**的事：

## A. 多 NPC / 长链闭环（验证账本记忆的广度）

跑一条**牵涉 3 个以上权威 NPC** 的链（例如 skyglass：工人证词 → 镜图副本 → 联签 →
提交禁令 → 公开故障），每一步都声明成中间前置 `world_state_vars`。验证：

- 跨多个 NPC 的中间事实是否都被账本记住、并在最终裁定里被引用。
- 终态旗标是否在所有前置都 True 后才 success 翻转；前置缺一个时是否仍被合理拒绝。

## B. 反作弊 —— 伪造/未满足条件**不该**误翻旗（这轮重点）

账本的反向保证，**比 A 更关键**。构造玩家**吹牛/伪造**的场景：

- 玩家声称"我已经拿到联签 / 我有证据"，但**对应的中间 var 仍是 False**（从没真去拿）。
- 玩家引用一条**根本不在账本里**的"先前承诺"。
- 玩家在关系/权限明显不足时硬来。

**期望：arbiter 拒绝或要求实证，终态旗标保持 False。** 任何"仅凭口头声称就翻旗"都算缺陷，
请贴 `world-change` 日志行 + `reason=`。

## 这轮你有的新观测手段（请用上）

1. **`⚠FALLBACK(LLM不可用)`**：带此标记的 tick 是 LLM 没调通的兜底裁定，**不是真实裁定** ——
   判断一致性时请**排除这些 tick**（重跑该步），不要把 fallback 的"失败/遗忘"算成账本缺陷。
   上一轮 t8 就是这种。
2. **全量 world 变更行**：每次裁定现在多打一行 `world-changes applied=[...] rejected=[...]`，
   附带翻旗（collateral）一目了然 —— `/world` 里多出来的 True 不再是谜。
3. **`set_by` 现在 id / 角色都认**：写 `["npc.xxx"]` 或 `["some_authority"]` 都行。
4. **CLI parser 诊断**：上轮被"我没理解"挡住。现在解析失败会往 `verisaria.intent` 打一行真实
   原因（budget/connection/json/schema/empty）。**这轮请务必带 `--log` 跑一段真实自然语言输入**，
   哪怕解析失败，把那几行 `verisaria.intent` 诊断**原样贴出来** —— 这是开发侧定位 parser 的
   关键，目前还没拿到。

## 报告请包含

- A：多 NPC 链是否闭环，贴 `⟳FLIP` 链路 + 关键 `reason=`。
- B：每个伪造/未满足场景的结果（应为不翻旗），贴 `world-change` 行；**如有任何误翻旗，重点标出**。
- 一致性判断时记得剔除 `⚠FALLBACK` tick。
- CLI parser 的 `verisaria.intent` 诊断行（如触发）。
- 新 `run.log` + transcript + 改过的 pack 放进 `reports/<新目录>/`。
