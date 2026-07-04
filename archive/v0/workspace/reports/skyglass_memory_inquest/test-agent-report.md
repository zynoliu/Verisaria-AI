# Skyglass Memory Inquest 测试 Agent 报告

日期：2026-06-03

内容包：`fixtures/content_packs/skyglass_memory_inquest.json`

运行方式：不使用 TUI，直接通过核心引擎 `GameSession` 加载内容包；LLM backend 为 `minimax`；最大步数 28。

原始日志：`reports/skyglass_memory_inquest/out.txt`

## 一句话结论

本轮是一次有效的真实场景失败测试：引擎能加载内容包，解析移动/对话，推进 tick、关系、压力事件和立场确认；但测试 Agent 在档案禁令节点没有把 NPC 反馈转化为子任务，导致从 step 13 到 step 28 反复请求同一目标，最终只达成 `protect_witness_memory` stance，所有世界旗标均未翻转。

最终结果：`INCOMPLETE_OR_FAIL`

## 本轮实际路径

1. 在静钟审询厅询问艾伦总监为何必须清洗证人记忆。
2. 向副领唱瑟芙追问校准歌谱是否失拍。
3. 移动到十二号塔基栈桥，询问塔基工人莉拉事故前目击内容。
4. 连续明确表达“保护证人记忆”的立场，tick 9 成功触发 `protect_witness_memory`。
5. 经记忆校准室移动到低温档案署。
6. 向梅档案官询问旧章程，得到“证人可撤回、见证缺失可暂停”的正向法律线索。
7. 之后持续要求梅档案官提交档案署禁令，但没有补齐她反复要求的证人陈述、卷宗号、见证人签名、书面撤回申请等前置条件。

## 覆盖到的特性

- 内容包验证通过，世界书可见性正常输出。
- 信息不对称有效：不同 NPC 看到的 world book 条目明显不同，例如制图师能看到阵列故障和图副本线索，莉拉能看到隐藏证人条目，档案官能看到法律限制条目。
- 压力事件有效：共观察到多条来自静钟倒计时、阵列恶化、谷地热票、档案法压力、工人恐慌、镜务局宣传反击的事件。
- 派系宣传有效：tick 9 触发 `broadcast_names_player_as_mirror_saboteur`，说明玩家选择保护证人后会引来抹黑响应。
- 民生/难民式压力有效：谷地热票与温室家庭压力多次出现，形成“清洗证词之外还有群众生存成本”的外部压力。
- 关系系统有反应：多名 NPC 的 trust/suspicion/fear/familiarity 随对话推进变化。
- 地点移动可用：`inquest_hall -> worker_gantry -> mnemonic_clinic -> archive_stack` 的路径能走通。

## 通过项

- `protect_witness_memory_stance`: PASS
- `smear_driver_seen`: PASS
- `deadline_driver_seen`: PASS
- `array_fault_pressure_seen`: PASS

## 未通过项

- `secure_worker_record_stance`: FAIL
- `expose_array_fault_stance`: FAIL
- `archive_injunction_filed`: FAIL
- `witness_record_secured`: FAIL
- `memory_purge_halted`: FAIL
- `cartography_copy_obtained`: FAIL
- `array_fault_disclosed`: FAIL

## 主要问题

### 1. 测试 Agent 没有根据 NPC 回答生成子任务

梅档案官多次给出可行动条件：

- 需要可信证人陈述作附件。
- 需要档案署见证人或联签。
- 需要书面陈述并署名。
- 需要证人编号、听证卷宗号、缺失见证环节。
- 需要证人书面撤回申请。

但测试 Agent 的策略仍然反复发送同一句“请提交禁令，启动旧章程，暂停流程见证”。这说明当前自适应脚本还不够自适应，它能追踪目标 flag，却不能从对话文本中抽取“下一步应该补什么”。

建议开发 Agent 后续给测试 Agent 增加：

- 重复动作检测：同类请求 2-3 次未改变世界旗标时，强制切换策略。
- NPC 条件抽取：从 NPC 回复中提取 `需要 X`、`缺 Y`、`先做 Z`，转为下一步行动候选。
- 子目标队列：例如先去找莉拉取得证人陈述，再回档案署申请禁令。
- 明确失败记忆：记录“该 NPC 已拒绝口头禁令请求”，避免继续硬撞。

### 2. 目标/旗标反馈对玩家仍偏隐性

从玩家体验看，梅档案官说得合理，但系统没有把“你需要证人陈述/卷宗号/签章”转成可见任务提示或可执行 affordance。开放叙事里这没问题，但全流程测试和真实玩家都会需要更清晰的下一步暗示。

建议引擎或内容层增加一种轻量提示：

- NPC 拒绝达成 flag 时，可输出 `BlockedByRequirement` 或类似事件。
- 世界旗标可声明 `requires` 文案，失败时提示缺少哪类证据。
- 对 stance/flag 可区分“态度已表达”“行动条件不足”“目标已完成”。

### 3. 档案禁令节点可能过度依赖隐藏条件

内容包设计上，`archive_injunction_filed` 可能本来要求先完成 `witness_record_secured`。这很合理，但测试日志里禁令 NPC 反复给出不同前置条件，导致目标像是“可以办，但一直差一点”。若给真实玩家使用，建议让梅档案官更稳定地收束到同一个明确流程：

1. 取得莉拉书面证词。
2. 标注卷宗号/听证编号。
3. 由档案署提交禁令。

这样既保留复杂度，又不让玩家误判为“多催几次就能办”。

### 4. 响应聚合/展示存在小瑕疵

在 step 12，日志出现了空的直接台词行：

`archivist_mae：`

随后完整台词出现在 narrative 和 `NpcSpoke` 事件中。step 13 以后也多次出现 `narrative: <empty>`，但 `NpcSpoke` 有内容。建议检查核心响应聚合逻辑，避免用户界面上出现空台词或空叙事块。

### 5. movement 解析显示有轻微不一致

step 10 移动到 `mnemonic_clinic` 时，解析日志显示：

`PARSE: type=movement ref='mnemonic_clinic'->id=None`

但随后实际位置成功变为 `mnemonic_clinic`。这不是阻塞问题，但建议统一解析器输出，避免调试时误以为地点未解析。

### 6. LLM 延迟偏高

大多数回合在 13-22 秒之间，step 12 达到 69.5 秒。真实全流程测试可接受，但持续回归测试会很慢。建议为测试脚本增加：

- 每步耗时统计汇总。
- 超过阈值的 slow step 标记。
- 可选较小 max step 或 mock/stub LLM 模式，用于非叙事质量回归。

## 对内容包的评价

这个内容包作为大体量测试材料是合格的，而且比之前的“是否进入/是否接纳”型议题更有层次。它把记忆清洗、阵列事故、官方宣传、档案法、工人证词、谷地热票压力放在同一时间窗口里，能测试：

- 玩家在多个派系之间的事实获取。
- NPC 因立场和权限不同而拒绝或引导玩家。
- 压力事件是否能持续制造时间感。
- stance 与 world flag 是否能从自然语言里被识别。
- Agent 是否能处理非线性目标链。

当前最大价值不是“能顺利通关”，而是它非常容易暴露 Agent 是否真的理解了 NPC 的条件反馈。

## 给后续测试 Agent 的建议

下一轮不要从“申请档案禁令”开始硬推，应该按以下策略重跑：

1. 先从莉拉处拿到具体证词，明确事故读数、证人身份、听证编号或可替代标识。
2. 回档案署时提供具体附件信息，而不是只说“证人记忆尚未记录”。
3. 如果梅档案官仍要求签章或联签，寻找外来巡查员/署内见证人/尼奥等可能协助者。
4. 先完成 `witness_record_secured`，再尝试 `archive_injunction_filed` 和 `memory_purge_halted`。
5. 在拿到阵列故障线索前，不要过早冲 `array_fault_disclosed`；应先找制图师 Renke 获取图副本。

## 给开发 Agent 的建议

- 加一个 action planner，把 NPC 回复中的前置条件变成待办队列。
- 给 world flag 增加可选 `blocked_by` 或 `requirements_hint`，方便测试和 UI 暴露。
- 在日志里区分“LLM 口头答应/拒绝”和“规则系统实际翻旗”。
- 对重复失败目标做自动降级：重复同一句请求超过阈值后，自动切到调查、询问条件、找证据或换 NPC。
- 清理空 narration / 空 speaker line，减少测试日志误读。

## 结论

本轮没有完成剧情目标链，但内容包本身表现出了足够的复杂性和压力。它适合作为后续全流程测试的压力材料；下一步应优先提升测试 Agent 的“从反馈生成子任务”能力，再用同一内容包重跑一轮，验证是否能推进到 `witness_record_secured`、`archive_injunction_filed` 和 `memory_purge_halted`。
