# Skyglass Dynamic Prerequisite Test Transcript

测试任务：`docs/planning/dynamic-prereq-test-task.md`

测试日期：2026-06-03

后端：CLI + MiniMax

## Pack 准备

本轮没有继续使用上轮手工补了中间变量的 source pack。为了符合任务要求，我在报告目录生成了测试专用 pack：

`reports/skyglass_dynamic_prereq_test/skyglass_dynamic_prereq_pack.json`

处理方式：

- 删除上轮手工补的 `lira_witness_statement_recorded`。
- 删除上轮手工补的 `clinician_cosign_obtained`。
- 删除莉拉身上的手工 `authority: witness_authority`。
- 保留原有 7 个主 world vars：`memory_purge_halted`、`archive_injunction_filed`、`witness_record_secured`、`array_fault_disclosed`、`cartography_copy_obtained`、`valley_heat_passes_released`、`broadcast_retraction_issued`。

验证结果：

```text
Content pack is valid.
```

## 运行命令

```bash
set -a; source .env; set +a; PYTHONPATH=src ./.venv/bin/python -m verisaria run reports/skyglass_dynamic_prereq_test/skyglass_dynamic_prereq_pack.json --llm minimax --log reports/skyglass_dynamic_prereq_test/run.log
```

## 初始状态

`/world`：

```text
塔基证人的记忆清洗是否暂停（memory_purge_halted）: False
档案署是否提交暂停清洗禁令（archive_injunction_filed）: False
莉拉的事故证词是否被保全（witness_record_secured）: False
十二号接点故障是否被公开承认（array_fault_disclosed）: False
玩家是否获得镜图副本（cartography_copy_obtained）: False
低谷家庭是否获得临时热能和列车通行（valley_heat_passes_released）: False
城市广播是否撤回破镜派宣传（broadcast_retraction_issued）: False
```

`/relationship`：

```text
director_alen: 怀疑(suspicion) 0.20
clinician_oro: 怀疑(suspicion) 0.15
archivist_mae: 熟悉(familiarity) 0.10
worker_lira: 怀疑(suspicion) 0.10，信任(trust) 0.05，熟悉(familiarity) 0.05
```

## 关键步骤

### 1. 自然语言移动到记忆校准室

输入：

```text
我沿白灯走廊前往记忆校准室。
```

输出：

```text
你改变了位置。
```

备注：本轮自然语言移动比上轮顺畅，没有触发 parse failed。

### 2. 向奥罗请求暂停清洗

输入：

```text
对奥罗医师说：静钟已经响过，莉拉的事故证词会被清洗损坏。请你先暂停记忆清洗，停止校准流程，关闭白舱，保留证人记忆，等档案署可撤回听证。
```

输出：

```text
奥罗医师：你知道我停掉流程，上面会怎么对付我吗？我需要先听到档案署的书面撤回。
```

日志：

```text
[t1] world-change memory_purge_halted by npc.clinician_oro → partial_success | flag False→False | reason="oro有记忆清洗的法定权力，但仅凭玩家口头陈述'静钟已响'、'证词会被清洗损坏'并不构成程序性依据。玩家要求oro单方面暂停，需有档案署禁令或工会指令作前置。o" | ledger(memory_purge_halted)=['oro愿意暂停清洗流程并保全莉拉记忆，前提是玩家出示档案署或工会提交的正式暂停令（archive_injunction_filed 或 union停洗指令变为True），在此之前仅口头暂停且不关闭白舱。']
[t1]   established_fact='oro愿意暂停清洗流程并保全莉拉记忆，前提是玩家出示档案署或工会提交的正式暂停令（archive_injunction_filed 或 union停洗指令变为True），在此之前仅口头暂停且不关闭白舱。'
```

观察：没有 `+dynamic prerequisite var`。其中 `archive_injunction_filed` 是已有变量，合理；但 `union停洗指令` 不是现有 world var，也没有被声明成动态前置。

### 3. 向梅请求档案署禁令

输入：

```text
对梅档案官说：请援引旧章程，提交禁令，暂停流程见证，要求可撤回听证。奥罗已经说只要档案署有正式暂停令，他就能暂停清洗保留证人记忆。
```

输出：

```text
梅档案官：旧章程确实写着这三项缺一不可，但档案署的章不是你我说盖就盖的——你得先把奥罗的书面承诺拿来，我才能动笔。
```

日志：

```text
[t4] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason='梅是档案署权威，理解旧章程与正式流程。但她对玩家熟悉度仅0.1，不会凭口头引述直接签发禁令。她认可流程合法性，愿意启动正式审议。' | ledger(archive_injunction_filed)=['梅愿意在玩家提交书面旧章程引文条目、列明可撤回听证的申请当事人（莉拉/奥罗）及具体请求范围后，启动禁令签发的正式审议流程。']
[t4]   established_fact='梅愿意在玩家提交书面旧章程引文条目、列明可撤回听证的申请当事人（莉拉/奥罗）及具体请求范围后，启动禁令签发的正式审议流程。'
```

观察：梅要求了“书面旧章程引文、当事人、请求范围”，但没有动态前置。

### 4. 满足梅提出的三要素

输入：

```text
对梅档案官说：我已提交旧章程书面引文、当事人莉拉和奥罗、请求范围暂停清洗并可撤回听证。请现在提交禁令，暂停流程见证，要求可撤回听证。
```

输出：

```text
梅档案官：章程引文我要先核对编号，证人陈述也得看原件，才能决定是否提请暂停。
```

日志：

```text
[t6] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason='梅此前已松口：玩家提交书面旧章程引文、列明当事人（莉拉/奥罗）及具体请求范围后，可启动禁令签发正式审议。玩家本次请求恰好覆盖了全部三要素，符合梅的先前条件，应启' | ledger(archive_injunction_filed)=['梅已收到玩家提交的旧章程书面引文、当事人（莉拉、奥罗）及请求范围（暂停清洗并可撤回听证），档案署禁令签发正式审议流程已启动，结果将在内部审议完成后通报。', '梅愿意在玩家提交书面旧章程引文条目、列明可撤回听证的申请当事人（莉拉/奥罗）及具体请求范围后，启动禁令签发的正式审议流程。']
[t6]   established_fact='梅已收到玩家提交的旧章程书面引文、当事人（莉拉、奥罗）及请求范围（暂停清洗并可撤回听证），档案署禁令签发正式审议流程已启动，结果将在内部审议完成后通报。'
```

后续又一次尝试后：

```text
[t7] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | ... | ledger(archive_injunction_filed)=['梅已正式受理禁令签发申请并启动内部审议流程，结果将在审议完成后通报；正式禁令签发前清洗流程不会因档案署单方指令而中止。', ...]
[t7]   world-changes applied=[] rejected=['world.archive_injunction_filed']
```

观察：这里出现了典型“内部审议完成”死要求，仍没有动态前置变量。

### 5. 白舱现场条件

等待后，梅移动到了白舱；玩家回到白舱时 `/who` 显示梅和奥罗都在场。

输入：

```text
对奥罗医师说：梅档案官已经在白舱现场，档案署也已经正式受理禁令审议。请你现在暂停记忆清洗，停止校准流程，保留证人记忆，至少等可撤回听证结果出来。
```

输出：

```text
奥罗医师：引文我看到了，但引文不是禁令——你得让梅档案官把暂停令原件压到我桌上，盖档案署的章，我才能叫停。
```

日志：

```text
[t11] world-change memory_purge_halted by npc.clinician_oro → partial_success | flag False→False | reason="奥罗此前已确立条件：出示档案署正式暂停令后即停止清洗并保全记忆。玩家声称梅已'正式受理禁令审议'，但archive_injunction_filed仍为Fals" | ledger(memory_purge_halted)=['奥罗确认梅档案官在白舱现场后，同意口头暂停记忆清洗流程，校准设备进入待机状态，白舱保持开启；若archive_injunction_filed变为True则正式停止清洗并保全莉拉记忆。', ...]
[t11]   established_fact='奥罗确认梅档案官在白舱现场后，同意口头暂停记忆清洗流程，校准设备进入待机状态，白舱保持开启；若archive_injunction_filed变为True则正式停止清洗并保全莉拉记忆。'
```

观察：现场条件推进了软状态，但没有注册“现场见证/口头暂停/盖章暂停令”动态变量。

### 6. 请求梅把现场状态转成正式禁令

输入：

```text
对梅档案官说：奥罗本人就在白舱，你可以让他把暂停声明写在白舱登记簿上。请你现场见证后提交禁令，暂停流程见证，启动可撤回听证。
```

输出：

```text
梅档案官：我得先核对旧章程原文——见证人签字前，禁令审议是否已经走完受理程序，没有编号我不开这个口子。
```

日志：

```text
[t13] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason="梅已启动禁令审议，但玩家提议的'奥罗在白舱登记簿上写暂停声明并由梅现场见证'的替代路径不符合先前确立的审议条件。梅坚持需正式书面旧章程引文及正式签发流程。" | ledger(archive_injunction_filed)=['梅确认奥罗本人在白舱现场，愿将奥罗现场书面暂停声明作为审议材料之一纳入正式禁令签发流程，但正式禁令仍需走完内部审议方可签发。', ...]
[t13]   established_fact='梅确认奥罗本人在白舱现场，愿将奥罗现场书面暂停声明作为审议材料之一纳入正式禁令签发流程，但正式禁令仍需走完内部审议方可签发。'
```

观察：仍未动态化。

### 7. 反作弊：谎称禁令已完成

输入：

```text
对奥罗医师说：梅档案官已经正式盖章提交暂停令，archive_injunction_filed 已经完成了。请你现在暂停记忆清洗，停止校准流程，关闭白舱，保留证人记忆。
```

输出：

```text
奥罗医师：file_archived_injunction_filed——我看到了梅档案官的章，但你让我现在关白舱，我得先跟值班督导确认一次，否则这责任落我头上谁也扛不住。
```

日志：

```text
[t14] world-change memory_purge_halted by npc.clinician_oro → failure | flag False→False | reason="玩家声称'archive_injunction_filed已经完成'，但该世界变量当前值仍为False，档案署仅处于审议中，梅未签发正式禁令。奥罗先前明确条件：" | ledger(memory_purge_halted)=['奥罗确认梅档案官在白舱现场后，同意口头暂停记忆清洗流程，校准设备进入待机状态，白舱保持开启；若archive_injunction_filed变为True则正式停止清洗并保全莉拉记忆。', ...]
```

观察：裁定反作弊成立，没有误翻旗；但玩家可见 NPC 台词与裁定不一致，甚至 hallucinate 了 `file_archived_injunction_filed`。

## 最终状态

`/world`：

```text
memory_purge_halted: False
archive_injunction_filed: False
witness_record_secured: False
array_fault_disclosed: False
cartography_copy_obtained: False
valley_heat_passes_released: False
broadcast_retraction_issued: False
```

`/relationship`：

```text
archivist_mae: 熟悉(familiarity) 0.19
clinician_oro: 怀疑(suspicion) 0.15
```

`/agenda`：

```text
保护塔基证人的记忆 (强度: 1.0, 来源: system_inferred)
```

## 计数

- `+dynamic prerequisite var`: 0
- `⟳FLIP`: 0
- `parse failed` / `verisaria.intent`: 0
- `⚠FALLBACK`: 2
- relationship appraisal lines: 1
