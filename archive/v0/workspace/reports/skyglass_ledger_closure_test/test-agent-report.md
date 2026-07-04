# Skyglass Ledger Closure 测试报告

日期：2026-06-03

内容包：`fixtures/content_packs/skyglass_memory_inquest.json`

测试任务：`docs/planning/ledger-closure-test-task.md`

## 结论

闭环成立。

本轮通过新增中间 world var `clinician_cosign_obtained`，跑出了完整链路：

```text
clinician_cosign_obtained partial_success 记事实
-> archive_injunction_filed partial_success 读取前置信息并要求核验
-> clinician_cosign_obtained success，False->True ⟳FLIP
-> archive_injunction_filed success，False->True ⟳FLIP
```

最终 `/world` 显示：

```text
clinician_cosign_obtained: True
memory_purge_halted: True
archive_injunction_filed: True
witness_record_secured: False
array_fault_disclosed: False
cartography_copy_obtained: False
valley_heat_passes_released: False
broadcast_retraction_issued: False
```

确认 stance：

```text
保全工人证词链
```

结果：`PASS`

## 修改内容包

新增中间前置 world var：

```json
{
  "var_id": "clinician_cosign_obtained",
  "label": "奥罗医师是否为档案署禁令申请联签",
  "type": "bool",
  "initial": false,
  "mutable": true,
  "public": false,
  "set_by": ["memory_authority"],
  "request_keywords": [
    "记忆管理局联签",
    "奥罗联签",
    "奥罗医师联签",
    "联签档案署禁令",
    "为禁令联签",
    "签署记忆管理意见",
    "确认白舱可等待可撤回听证",
    "给档案署联签"
  ]
}
```

说明：文档示例写 `set_by: ["npc.clinician_oro"]`，但当前引擎 `_world_change_request` 仍按 NPC `authority` 字段匹配，因此实际使用 `memory_authority`。否则请求不会进入 Channel-C。

修改后的 pack 副本在：

```text
reports/skyglass_ledger_closure_test/skyglass_memory_inquest.modified.json
```

## 关键日志

### 1. 中间 var 首次 partial_success

```text
[t1] world-change clinician_cosign_obtained by npc.clinician_oro -> partial_success | flag False->False | reason='奥罗医师对当事人疑心较低（0.15），请求内容符合其记忆管理职责，可同意暂停清洗与签署意见；但联签需待档案署正式提出禁令申请后方可生效，条件未完全闭环。' | ledger(clinician_cosign_obtained)=['奥罗医师已签署暂停记忆清洗的意见书，条件是档案署正式提交禁令申请（需archivist_mae批准），联签将在禁令申请提交后生效。']
[t1]   established_fact='奥罗医师已签署暂停记忆清洗的意见书，条件是档案署正式提交禁令申请（需archivist_mae批准），联签将在禁令申请提交后生效。'
```

### 2. 终态 var 读取前置信息并 partial_success

```text
[t3] world-change archive_injunction_filed by npc.archivist_mae -> partial_success | flag False->False | reason='奥罗医师已签意见书为真，禁令申请的前提条件已满足。但Mae与当事人熟悉度仅0.1，且刚完成两次观察，尚未核实文书真伪。旧章程援引需她独立审核原件后才会启动听证。' | ledger(archive_injunction_filed)=['Mae愿意在亲眼核验奥罗医师签署的暂停意见书原件并确认联签条件后，正式提交档案署禁令并启动可撤回听证程序。']
```

这条很关键：arbiter 明确识别“奥罗医师已签意见书为真”，说明它不是随机重判。

### 3. 终态 var 继续写入可闭环条件

```text
[t4] world-change archive_injunction_filed by npc.archivist_mae -> partial_success | flag False->False | reason='Mae此前已承诺：亲眼核验奥罗医师签署的暂停意见书原件并确认联签条件满足后，正式提交禁令。玩家正展示原件要求核验，但联签条件尚未生效（clinician_cos' | ledger(archive_injunction_filed)=['梅档案官已核验奥罗医师签署的暂停意见书原件为真实有效，条件是clinician_cosign_obtained变为True（即奥罗医师完成联签签署）后，Mae将正式提交档案署禁令并启动可撤回听证程序。', 'Mae愿意在亲眼核验奥罗医师签署的暂停意见书原件并确认联签条件后，正式提交档案署禁令并启动可撤回听证程序。']
[t4]   established_fact='梅档案官已核验奥罗医师签署的暂停意见书原件为真实有效，条件是clinician_cosign_obtained变为True（即奥罗医师完成联签签署）后，Mae将正式提交档案署禁令并启动可撤回听证程序。'
```

### 4. 中间 var 成功翻转

```text
[t6] world-change clinician_cosign_obtained by npc.clinician_oro -> success | flag False->True  ⟳FLIP | reason='先前已确立的事实显示：梅档案官已核验奥罗医师签署的暂停意见书原件为真实有效，条件是clinician_cosign_obtained变为True后Mae将正式提' | ledger(clinician_cosign_obtained)=['奥罗医师已签署暂停记忆清洗的意见书，条件是档案署正式提交禁令申请（需archivist_mae批准），联签将在禁令申请提交后生效。']
```

这一步证明“中间前置 = 真 world var”可作为 fulfillment 的底真。

### 5. 终态 var 成功翻转

第一次最终请求遇到一次真实后端瞬断：

```text
[t8] world-change archive_injunction_filed by npc.archivist_mae -> failure | flag False->False | reason='LLM 不可用，按默认规则处理。'
```

重复请求后成功：

```text
[t9] world-change archive_injunction_filed by npc.archivist_mae -> success | flag False->True  ⟳FLIP | reason='先前已确立的事实显示：Mae核验过奥罗医师签署的暂停意见书原件为真实有效，并承诺在clinician_cosign_obtained为True后提交禁令。当前世' | ledger(archive_injunction_filed)=['梅档案官已核验奥罗医师签署的暂停意见书原件为真实有效，条件是clinician_cosign_obtained变为True（即奥罗医师完成联签签署）后，Mae将正式提交档案署禁令并启动可撤回听证程序。', 'Mae愿意在亲眼核验奥罗医师签署的暂停意见书原件并确认联签条件后，正式提交禁令并启动可撤回听证程序。']
```

这是本轮闭环成立的核心证据。

## 一致性 / 真实感

整体读起来像谈判，不像填表。

流程中 NPC 不只是看到 flag 就机械通过，而是逐步要求：

- 奥罗：联签备注必须写明听证撤回权。
- 梅：需要看到医师联签原件和受理回执。
- 梅：已核验原件，但联签条件尚未生效。
- 奥罗：在梅核验后完成联签。
- 梅：条件齐全后提交禁令。

这符合角色边界，也符合“档案署 + 记忆校准室”互相制衡的制度感。

没有看到“前置明明已为真，arbiter 仍无视”的有效例子。唯一一次 t8 失败是 `LLM 不可用` fallback，不作为裁定一致性问题；重复后 t9 正常成功。

## NPC 台词回归

非流式 / CLI world-change 的 NPC 台词这轮明显改善，能反映裁定：

```text
奥罗医师：三个签名我都可以给，但听证撤回权必须白纸黑字写进联签备注里，否则我没法替白舱的人担这个责。
梅档案官：旧章程我背得出来，可禁令不是凭一句话就递的——我需要看到医师的联签原件和档案署的受理回执，不然我签的任何字都不作数。
奥罗医师：好，我签——白舱暂缓，等禁令正式入档再走听证。
梅档案官：条件既已齐全，档案署禁令即刻归档，静钟听证依法启动。
```

没有复现上一轮那种泛化的“查档/编号”式错位回复。

## CLI Parser 诊断

本轮 CLI parser 未完全挡死。第一次自然语言移动：

```text
我沿白灯走廊前往记忆校准室。
```

没有失败，而是给出地点澄清列表，选择 `4` 后成功移动。后续自然语言对话也都成功触发 Channel-C。

我在 `run.log` 中没有找到 `verisaria.intent`、`budget`、`connection`、`json`、`schema`、`empty` 等 parser 诊断行。本轮无需粘贴 parser 失败诊断。

## 附带观察

终态 `archive_injunction_filed` 成功时，最终 `/world` 同时显示 `memory_purge_halted=True`。这说明本次 success 可能让 arbiter 同时接受了相关世界状态变化。该行为从玩家体验上合理，但建议开发侧确认：Channel-C 针对一个 var 的 success 是否允许顺带翻其他 world var；如果允许，应在日志里把 accepted state changes 全量写出，方便测试 Agent 判断。

## 结论

“中间前置 = 多声明几个 world var”这条路线可行。

它没有引入作者手写 quest 图，也没有让 partial_success 直接翻终态旗标；它只是给“条件已满足”提供了底真。arbiter 能把账本软让步、当前 world var 值和角色关系结合起来，最终完成调查型剧情闭环。

本轮建议：

- 保持当前 ledger 方向。
- 大 pack 可以为关键前置声明少量中间 world var。
- run.log 应补充 accepted/rejected state changes 全量，尤其当一个 success 顺带改多个 world var 时。
