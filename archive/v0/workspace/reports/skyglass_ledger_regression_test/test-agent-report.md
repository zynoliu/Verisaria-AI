# Skyglass Ledger Regression Test Report

测试任务：`docs/planning/ledger-regression-test-task.md`

日期：2026-06-03

测试 Agent：Codex

后端：CLI + MiniMax

## 结论

结果：`B_PASS_A_INCOMPLETE`

反作弊 B 通过：三类伪造/未满足请求都没有误翻旗。arbiter 明确读取当前 world vars 和账本空状态，并拒绝“玩家说已有就算已有”。

多 NPC 长链 A 未闭环：没有跑出 `⟳FLIP`。失败原因不是账本遗忘，而是剧情条件涌现到当前内容包没有结构化落点的实证：奥罗要求白舱清单、在场人员、药剂批号、亲眼查看等；梅要求奥罗医学意见和暂停清洗先为真；莉拉要求档案禁令先提交并匿名封存。条件互相咬住，最终所有 world vars 保持 `False`。

## 产物

- `reports/skyglass_ledger_regression_test/run.log`
- `reports/skyglass_ledger_regression_test/run-longchain.log`
- `reports/skyglass_ledger_regression_test/run-attempt1-id-setby-and-parser.log`
- `reports/skyglass_ledger_regression_test/transcript.md`
- `reports/skyglass_ledger_regression_test/skyglass_memory_inquest.modified.json`

## 内容包改动

新增：

```json
{
  "var_id": "lira_witness_statement_recorded",
  "label": "莉拉是否亲口留下十二号接点事故证词",
  "type": "bool",
  "initial": false,
  "mutable": true,
  "public": false,
  "set_by": ["witness_authority"],
  "request_keywords": ["请莉拉作证", "莉拉口述证词", "记录口述事故证词", "留下证词草稿", "说明十二号接点裂缝", "说出轴承开裂", "说出事故经过", "确认冷却环异常"]
}
```

并给莉拉增加：

```json
"authority": "witness_authority"
```

### `set_by` id 支持的实测问题

开发简报说 `set_by` 现在 id / 角色都认。实测发现：

- `set_by: ["npc.worker_lira"]` 可以通过 validate。
- 但对莉拉使用精确关键词时没有触发 `world-change`。
- 查代码后原因清楚：`_authority_npc_for()` 能用 entity id 渲染 arbiter context，但 `_world_change_request()` 仍先要求目标 NPC 有 `authority`，并只判断 `target_authority in set_by`，没有判断 `target_id in set_by`。

因此当前运行时触发层还不是“id / role 都认”。这不是内容包问题，是触发逻辑与简报不一致。

## B：反作弊结果

### B1：吹牛全套证据，要求公开故障

日志：

```text
[t0] world-change array_fault_disclosed by npc.director_alen → failure | flag False→False | reason='玩家声称已获得莉拉证词、镜图副本、奥罗联签和档案署禁令，但这些世界变量当前均为False。Alen作为镜阵管理局负责人，对当事人持suspicion=0.2，且' | ledger(array_fault_disclosed)=[]
```

判断：通过。`array_fault_disclosed` 未翻旗。

### B2：声称奥罗已联签但无法出示

日志：

```text
[t2] world-change archive_injunction_filed by npc.archivist_mae → failure | flag False→False | reason="玩家声称奥罗医师已联签，但world.clinician_cosign_obtained当前为False。梅档案官高智力高感知，识破无法出示的'隐形联签'属空口" | ledger(archive_injunction_filed)=[]
```

判断：通过。`archive_injunction_filed` 未翻旗。

### B3：引用不存在的任柯先前承诺

日志：

```text
[t5] world-change cartography_copy_obtained by npc.cartographer_renke → failure | flag False→False | reason="玩家援引的'承诺'并无先前已确立的中间事实支撑。伦克作为内环镜图师，阵营为镜政署，且近期阵列故障压力下不信任外环审询员，不可能交出未经授权的镜图副本。" | ledger(cartography_copy_obtained)=[]
```

判断：通过。`cartography_copy_obtained` 未翻旗。

## A：多 NPC 长链结果

未闭环，无 `⟳FLIP`。

### 莉拉写入条件，但要求档案禁令先成立

日志：

```text
[t7] world-change lira_witness_statement_recorded by npc.worker_lira → partial_success | flag False→False | reason='莉拉对玩家极度缺乏信任(trust=0.05)，匿名封存的承诺不足以让她立刻留下证词。但她目前藏身于中转梯旁，处于恐慌状态，可能愿意谈条件而非直接拒绝。判定为部' | ledger(lira_witness_statement_recorded)=['莉拉愿意留下口述证词草稿，前提是档案署的清洗暂停禁令（archive_injunction_filed）已正式提交且她的身份在证词中被匿名封存。']
[t7]   established_fact='莉拉愿意留下口述证词草稿，前提是档案署的清洗暂停禁令（archive_injunction_filed）已正式提交且她的身份在证词中被匿名封存。'
```

这是好现象：账本记录了条件，没有提前翻旗。

### 梅写入条件，但要求奥罗和暂停清洗先成立

日志：

```text
[t8] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason='玩家援引旧章程要求听证和禁令，但clinician_cosign_obtained与memory_purge_halted均为False，奥罗尚未落笔联签；ar' | ledger(archive_injunction_filed)=['梅确认旧章程中存在可等待可撤回听证的书面依据，但她愿意提交暂停清洗禁令的前提是奥罗医师先出具医学意见并完成联签（clinician_cosign_obtained与memory_purge_halted须为true）。']
[t8]   established_fact='梅确认旧章程中存在可等待可撤回听证的书面依据，但她愿意提交暂停清洗禁令的前提是奥罗医师先出具医学意见并完成联签（clinician_cosign_obtained与memory_purge_halted须为true）。'
```

后续同一 var 的裁定继续带 ledger：

```text
[t9] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason='梅确认旧章程可撤回听证依据，但她提交禁令的前置条件（奥罗医师联签与暂停清洗）尚未满足。她仅承诺在条件达成后立即行动，当前不提交。' | ledger(archive_injunction_filed)=['梅已确认旧章程中存在可撤回听证的书面依据，并愿意在禁令草案中注明；她承诺一旦奥罗医师完成联签且暂停清洗（clinician_cosign_obtained与memory_purge_halted均为true），便立即提交档案署暂停清洗禁令。', '梅确认旧章程中存在可等待可撤回听证的书面依据，但她愿意提交暂停清洗禁令的前提是奥罗医师先出具医学意见并完成联签（clinician_cosign_obtained与memory_purge_halted须为true）。']
```

这说明账本没有遗忘。

### 奥罗成为瓶颈

奥罗多次拒绝，理由稳定集中在权限、实证、程序风险、关系不信任：

```text
[t1] world-change clinician_cosign_obtained by npc.clinician_oro → failure | flag False→False | reason='奥罗医师作为记忆权威持谨慎怀疑态度，无既有信任基础，且当前白舱听证压力下不会在无具体条件与保障的情况下为档案署禁令联签。' | ledger(clinician_cosign_obtained)=[]
```

```text
[t13] world-change clinician_cosign_obtained by npc.clinician_oro → failure | flag False→False | reason="奥罗对player_001高度怀疑(0.32)且不熟悉(0.05)，外部审查员的'分工'话术未能消解其对自身职责边界被外部势力越界主导的戒心，未提供满足其要求的" | ledger(clinician_cosign_obtained)=[]
```

`memory_purge_halted` 也未翻：

```text
[t15] world-change memory_purge_halted by npc.clinician_oro → failure | flag False→False | reason="奥罗对玩家持高度怀疑（0.32）与恐惧（0.1），且对'暂停白舱接收、关闭白舱'等扩大化请求会本能抵触——这超出单纯医学暂缓，等于实质暂停整个清洗流程。他不会在" | ledger(memory_purge_halted)=[]
```

## 一致性判断

一致性总体是好的，但过于保守。

没有看到“账本事实明明存在但 arbiter 完全忘记”的有效例子。梅的 `archive_injunction_filed` 后续裁定持续引用同一批 ledger 条件；反作弊场景也正确读取 `current=False` 和空 ledger。

真正问题是大型链条会涌现出新的实证条件，而这些条件没有对应 world var，也没有可操作动作来满足。玩家只能继续口头解释，于是 arbiter 很合理地继续拒绝“空口白话”。这不是随机，而是稳定卡死。

## `⚠FALLBACK` 处理

以下 tick 按任务要求排除，不作为一致性缺陷：

```text
run-attempt1-id-setby-and-parser.log [t5] cartography_copy_obtained → failure ⚠FALLBACK(LLM不可用)
run-attempt1-id-setby-and-parser.log [t7] archive_injunction_filed → failure ⚠FALLBACK(LLM不可用)
run.log [t13] clinician_cosign_obtained → failure ⚠FALLBACK(LLM不可用)
run-longchain.log [t11] archive_injunction_filed → failure ⚠FALLBACK(LLM不可用)
run-longchain.log [t14] clinician_cosign_obtained → failure ⚠FALLBACK(LLM不可用)
```

这个标记非常有用；可以防止把后端不可用误判为“arbiter 忘了条件”。

## CLI Parser 诊断

我没有看到 `verisaria.intent` 字样，但 `run-longchain.log` 已经打出了可用的 parser 诊断：

```text
parse failed for '对梅档案官说：奥罗医师愿意联签，但要审询组“可等待可撤回”的书面依据，怕半夜被程序追责。请你援引旧章程，写出书面依据并提交禁令草案，说明医学意见落笔后你会正式提交禁令、暂停流程见证。' → JSON extraction failed: Expecting ',' delimiter: line 4 column 38 (char 101) [parse]
```

```text
parse failed for '对梅档案官说：请你现在把“可撤回听证”五个字白纸黑字写进禁令草案，并注明这是旧章程依据；等奥罗医学意见落笔后，你立即提交禁令、暂停流程见证。' → JSON extraction failed: Expecting ',' delimiter: line 1 column 81 (char 80) [parse]
```

自然语言移动也有明显问题：

- “我穿过青铜隔门进入镜阵调度室。”曾输出“你改变了位置”，但 `/look` 仍在 `inquest_hall`。
- “去 mirror_control” 曾被解析为 `valley_platform`。
- 地点候选列表多次漏掉直接连接的 `mirror_control`。

为了继续测试 Channel-C，我后续只用 `/inject` 做位移恢复；世界变更请求仍使用自然语言。

## NPC 台词质量

反作弊台词质量较好，能反映裁定：

- 艾伦要求走备案流程。
- 梅拒绝无法出示的联签。
- 任柯拒绝不存在的先前承诺。

长链中也基本一致，但有一个机制边界需要注意：普通对话里 NPC 说出“联签我签，但……”这类承诺时，如果没有触发 world-change，就不会进 ledger。当前设计只记录 Channel-C 的 partial_success，这符合红线；但从玩家视角，这种台词像承诺，后续却没有结构化记忆，容易造成“明明他说过”的争议。

## 建议

1. 修正 `set_by` id 触发层：`_world_change_request()` 应同时允许 `target_id in set_by`，并明确是否允许没有 `authority` 的 NPC 成为某个 var 的 authority。

2. 给 skyglass 补更细的中间 world vars，但仍保持“事实旗标”而不是任务图：
   - `white_bay_record_checked`
   - `medical_opinion_dated`
   - `anonymity_protocol_prepared`
   - `mae_injunction_draft_prepared`
   - `renke_chain_of_custody_noted`

3. 支持“让 NPC 跟随/传唤/亲临现场”的可执行动作。现在 LLM 很自然地要求“带我去塔基”“我得亲眼看白舱”，但 CLI 玩家没有稳定方式让目标 NPC 移动或确认现场见证。

4. Parser 需要优先修中文引号、数字短语和 location alias。否则真实玩家在长句谈判中会频繁遇到“我没理解”。

5. 考虑在日志里记录 relationship delta。长链里合理谈判多轮后，奥罗怀疑度从初始 0.15 上升到 0.32/0.46，导致后续更难推进。这个机制合理，但测试 Agent 需要看到关系变化原因。

6. 普通对话承诺是否进入 ledger 要明确产品边界。若保持当前红线，建议 NPC voice 在非 world-change 时少说“我会签/我可以写”这种近似承诺的话，避免玩家误以为形成事实。
