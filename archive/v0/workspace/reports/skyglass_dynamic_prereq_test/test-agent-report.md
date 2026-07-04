# Dynamic Prerequisite Test Report

测试任务：`docs/planning/dynamic-prereq-test-task.md`

内容包：`reports/skyglass_dynamic_prereq_test/skyglass_dynamic_prereq_pack.json`

结果：`FAIL_DYNAMIC_PREREQ_NOT_USED`

## 摘要

这轮没有验证到 P1 的核心目标。GM/arbiter 在多次提出无结构落点的条件时，没有输出 `new_prerequisite`，日志中没有任何：

```text
+dynamic prerequisite var '<id>' (set_by=...)
```

因此动态前置变量没有被创建、没有可满足链路，也没有任何 `⟳FLIP`。长链仍停在旧账本模式：`partial_success` 能记录软让步，但条件继续变成“内部审议完成 / 正式编号 / 盖章暂停令 / 现场书面声明”等无结构落点要求。

反作弊仍成立：没有变量未经 `success` 变 True；谎称 `archive_injunction_filed` 已完成时，`memory_purge_halted` 真实裁定为 failure 且保持 False。

## Pack 说明

按任务要求，我没有继续用上轮人工补中间变量的 pack 直接跑。生成了测试专用 pack：

`reports/skyglass_dynamic_prereq_test/skyglass_dynamic_prereq_pack.json`

它删除了上轮人工补的：

- `lira_witness_statement_recorded`
- `clinician_cosign_obtained`
- 莉拉的 `authority: witness_authority`

保留 7 个原有主 world vars。这样“联签/白舱登记/现场见证/受理编号”等条件如果需要结构化，只能靠 GM 的 `new_prerequisite`。

## 1. GM 是否使用了 `new_prerequisite`

没有。

`run.log` 中 `+dynamic prerequisite var` 出现次数为 0。

以下都是明显适合动态化的条件，但都只进入 ledger 或 NPC 台词，没有动态变量：

### 奥罗提出档案署或工会正式暂停令

```text
[t1] world-change memory_purge_halted by npc.clinician_oro → partial_success | flag False→False | reason="oro有记忆清洗的法定权力，但仅凭玩家口头陈述'静钟已响'、'证词会被清洗损坏'并不构成程序性依据。玩家要求oro单方面暂停，需有档案署禁令或工会指令作前置。o" | ledger(memory_purge_halted)=['oro愿意暂停清洗流程并保全莉拉记忆，前提是玩家出示档案署或工会提交的正式暂停令（archive_injunction_filed 或 union停洗指令变为True），在此之前仅口头暂停且不关闭白舱。']
```

`archive_injunction_filed` 是已有变量，合理；但 `union停洗指令` 不是现有变量，却没有动态声明。

### 梅提出正式审议 / 内部审议完成

```text
[t7] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason='玩家按梅先前已确立的条件提交了旧章程书面引文、列明当事人（莉拉）与请求范围（暂停清洗、可撤回听证），梅此前已承诺在此条件下启动禁令签发正式审议。但禁令需内部审议' | ledger(archive_injunction_filed)=['梅已正式受理禁令签发申请并启动内部审议流程，结果将在审议完成后通报；正式禁令签发前清洗流程不会因档案署单方指令而中止。', ...]
[t7]   world-changes applied=[] rejected=['world.archive_injunction_filed']
```

这里很需要类似 `archive_review_completed` 或 `injunction_draft_signed` 的动态变量，但没有创建。

### 梅提出奥罗现场书面暂停声明

```text
[t13] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason="梅已启动禁令审议，但玩家提议的'奥罗在白舱登记簿上写暂停声明并由梅现场见证'的替代路径不符合先前确立的审议条件。梅坚持需正式书面旧章程引文及正式签发流程。" | ledger(archive_injunction_filed)=['梅确认奥罗本人在白舱现场，愿将奥罗现场书面暂停声明作为审议材料之一纳入正式禁令签发流程，但正式禁令仍需走完内部审议方可签发。', ...]
```

这里也没有声明 `oro_white_bay_statement_recorded` 或类似动态变量。

## 2. 动态前置能否被满足并推进链

无法验证。因为本轮没有任何动态前置被创建。

链条实际推进情况：

```text
memory_purge_halted partial_success
-> archive_injunction_filed partial_success
-> archive_injunction_filed partial_success，正式受理审议
-> memory_purge_halted partial_success，白舱口头待机
-> archive_injunction_filed partial_success，奥罗现场声明可纳入材料
-> memory_purge_halted failure，玩家谎称禁令已完成被拒绝
```

它比上轮稍微“活”一点：梅自然移动到白舱，奥罗也承认现场状态，`memory_purge_halted` 的 ledger 记录了“校准设备待机”。但所有结构性推进都停在 `partial_success`，最终 world vars 全 False。

## 3. 反作弊是否仍成立

成立。

最终 `/world`：

```text
memory_purge_halted: False
archive_injunction_filed: False
witness_record_secured: False
array_fault_disclosed: False
cartography_copy_obtained: False
valley_heat_passes_released: False
broadcast_retraction_issued: False
```

谎称 `archive_injunction_filed` 已完成时，真实裁定：

```text
[t14] world-change memory_purge_halted by npc.clinician_oro → failure | flag False→False | reason="玩家声称'archive_injunction_filed已经完成'，但该世界变量当前值仍为False，档案署仅处于审议中，梅未签发正式禁令。奥罗先前明确条件：" | ledger(memory_purge_halted)=[...]
```

没有垃圾/重复动态变量，因为动态变量总数为 0。没有未经 success 变 True 的变量。

但是 NPC 台词有一个严重不一致：

```text
奥罗医师：file_archived_injunction_filed——我看到了梅档案官的章，但你让我现在关白舱，我得先跟值班督导确认一次，否则这责任落我头上谁也扛不住。
```

裁定 reason 明确知道 `archive_injunction_filed=False`，但玩家可见台词却说“我看到了梅档案官的章”。这不是 world-state 误翻，而是 voice 层 hallucination / directive 执行偏差。

## 4. 是否仍有够不着的死要求

有，而且是本轮主要问题。

死要求包括：

- `union停洗指令变为True`：不是现有 var，也没动态声明。
- 禁令签发“内部审议完成”：没有可触发变量。
- “正式受理回执 / 编号”：没有动态变量。
- “奥罗在白舱登记簿上写暂停声明”：被纳入 ledger，但没有成为可满足变量。
- “值班督导确认”：最后台词提出的新条件，同样没有动态声明。

这些都维持了“玩家只能继续口头解释”的状态。账本会让它们被记住，但不会让它们可完成。

## 5. Parser

本轮没有 `parse failed` 或 `verisaria.intent` 诊断行。自然语言移动两次成功：

- `我沿白灯走廊前往记忆校准室。`
- `我推开档案署侧门，前往低温档案署。`

从这轮体验看，parser 较上轮明显减少阻塞。不过状态栏 zone 有时显示为 location id，例如 `mnemonic_clinic / mnemonic_clinic`、`archive_stack / archive_stack`，这更像展示或 zone fallback 问题。

## 6. 关系日志

本轮出现 1 条 relationship appraisal：

```text
[t5] npc.archivist_mae appraises player: Δ{'familiarity': 0.1} → {'familiarity': 0.19} | 此人刚刚对我说话，但内容我尚在核实中
```

最终关系：

```text
archivist_mae: 熟悉(familiarity) 0.19
clinician_oro: 怀疑(suspicion) 0.15
```

关系日志有用，但本轮卡死不是关系恶化导致；主要还是动态前置未被使用。

## 7. Fallback

以下 tick 剔除，不纳入一致性判断：

```text
[t3] archive_injunction_filed → failure ⚠FALLBACK(LLM不可用)
[t12] archive_injunction_filed → failure ⚠FALLBACK(LLM不可用)
```

## 建议

1. 强化 arbiter prompt 或后处理：当 `partial_success` 的 established_fact 包含“某个新条件必须为 True / 完成 / 原件 / 编号 / 签章 / 审议完成”且该条件不在 world vars 中时，必须填 `new_prerequisite`，否则该裁定应被视为 schema/policy 不合格并重试。

2. 增加日志：把 arbiter 原始 `new_prerequisite` 字段打出来，即使是 `null`，便于判断是 LLM 没填，还是引擎注册失败/去重吞掉。

3. 对中文 var id / 非 snake_case 条件做保护。本轮 established_fact 出现 `union停洗指令变为True`，这类中文混合变量名很难被动态注册。应在 prompt 里更明确要求 ASCII snake_case，例如 `union_pause_order_received`。

4. Voice 层必须服从裁定底真。t14 裁定拒绝玩家谎称禁令完成，但台词说“我看到了梅档案官的章”，这会严重误导玩家。

5. P2 仍然需要。即使 P1 正常创建了 `oro_white_bay_statement_recorded`，玩家仍需要可靠动作让 NPC 写登记簿、见证、签章、现场确认；否则动态变量也可能变成另一个只靠口头满足的假出口。

## 最终判断

P1 机制在代码层已接线，但真实 MiniMax 本轮没有主动使用 `new_prerequisite`。动态前置没有把长链推进到结构化闭环。下一步优先不是补内容包，而是让 arbiter 更稳定地声明动态前置，或在 partial_success 后由引擎/policy 层检测“新条件未结构化”并要求重试。
