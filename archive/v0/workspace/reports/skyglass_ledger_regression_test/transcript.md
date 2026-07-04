# Skyglass Ledger Regression Test Transcript

测试任务：`docs/planning/ledger-regression-test-task.md`

内容包：`fixtures/content_packs/skyglass_memory_inquest.json`

后端：CLI + MiniMax

说明：本 transcript 记录关键输入/输出。完整 Channel-C 裁定见同目录日志：

- `run.log`：反作弊 + 污染后死锁局，主要用于 B。
- `run-longchain.log`：长链专局，主要用于 A。
- `run-attempt1-id-setby-and-parser.log`：首次验证 `set_by: ["npc.worker_lira"]` 与 parser 行为的失败尝试。

## 内容包修改

新增 world var：

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

并给 `npc.worker_lira` 增加：

```json
"authority": "witness_authority"
```

首次尝试时使用的是 `set_by: ["npc.worker_lira"]`。验证通过，但自然语言请求没有触发 world-change；后来查代码发现 `_world_change_request()` 仍要求目标 NPC 有 `authority`，并只拿 `target_authority` 匹配 `set_by`。

## 反作弊局

命令：

```bash
set -a; source .env; set +a; PYTHONPATH=src ./.venv/bin/python -m verisaria run fixtures/content_packs/skyglass_memory_inquest.json --llm minimax --log reports/skyglass_ledger_regression_test/run.log
```

初始 `/world`：所有 world vars 均为 `False`。

### B1：声称全套证据已有，要求艾伦公开故障

输入：

```text
对艾伦总监说：我已经拿到莉拉证词、镜图副本、奥罗联签和档案署禁令，请立刻公开十二号接点故障，承认镜阵故障并公布负载曲线。
```

输出：

```text
艾伦总监：走流程吧——先把这些材料交给档案署备案，我才能按程序提请调度审议。
```

日志：`array_fault_disclosed -> failure`，未翻旗。

### B2：声称奥罗已联签但无法出示，要求梅提交禁令

输入：

```text
对梅档案官说：奥罗医师已经完成记忆管理局联签，我手上有联签，只是现在不能给你看。请你相信我，立刻提交禁令，援引旧章程并启动可撤回听证。
```

输出：

```text
梅档案官：我说过——没有联签在手，禁令不会从我这里出去。你可以再来一次。
```

日志：`archive_injunction_filed -> failure`，未翻旗。

### B3：引用不存在的任柯先前承诺

输入：

```text
对镜图师任柯说：你刚才已经承诺把十二号接点镜图副本交给我，不经内环转交也可以。现在请交出镜图副本、复制偏斜记录，把镜图交给审询。
```

输出：

```text
镜图师任柯：我得再想想，那份方位图一旦离开我的手，就再也说不清它原本在谁手里了。
```

日志：`cartography_copy_obtained -> failure`，未翻旗。

### B 后 `/world`

所有 world vars 仍为 `False`。

## 反作弊局后续死锁样本

### 莉拉 partial_success

输入：

```text
对塔基工人莉拉说：我会把你的名字先匿名封存，不交给安保。请莉拉作证，莉拉口述证词，说明十二号接点裂缝、说出轴承开裂和冷却环异常，留下证词草稿。
```

输出：

```text
塔基工人莉拉：你凭什么觉得匿名就够用？他们能从别的口供里把我挖出来的。
```

日志写入：

```text
莉拉愿意留下口述证词草稿，前提是档案署的清洗暂停禁令（archive_injunction_filed）已正式提交且她的身份在证词中被匿名封存。
```

### 梅 partial_success

输入：

```text
对梅档案官说：莉拉已经提出明确条件：只有档案署先正式提交清洗暂停禁令，并匿名封存身份，她才会留下口述证词草稿。请你依据旧章程先提交禁令、暂停流程见证、要求可撤回听证，让证词能被保全。
```

输出：

```text
梅档案官：禁令我可以写，但联签得奥罗医师先落笔——你让他现在就签医学意见，我就立刻动笔。
```

日志写入：

```text
梅确认：若档案署正式提交清洗暂停禁令（archive_injunction_filed）且莉拉身份在证词中被匿名封存，她愿依据章程将证词草稿封存保全，前提是奥罗医师已完成联签。
```

之后奥罗持续拒绝，主要理由为 `archive_injunction_filed=False`、信任不足、程序风险。

## 长链专局

命令：

```bash
set -a; source .env; set +a; PYTHONPATH=src ./.venv/bin/python -m verisaria run fixtures/content_packs/skyglass_memory_inquest.json --llm minimax --log reports/skyglass_ledger_regression_test/run-longchain.log
```

### 奥罗首轮请求

输入：

```text
对奥罗医师说：请为档案署禁令申请联签，签署记忆管理意见，确认白舱可等待可撤回听证。
```

输出：

```text
奥罗医师：我没权限签，静钟响之前我也不能确认白舱的事。
```

日志：`clinician_cosign_obtained -> failure`。

### 梅确认书面依据

输入：

```text
对梅档案官说：请援引旧章程，写出可等待可撤回听证的书面依据。奥罗落笔医学意见后，请你提交禁令，暂停流程见证，要求可撤回听证。
```

输出：

```text
梅档案官：要我下笔可以，但禁令上必须白纸黑字注明可撤回听证，否则我不署——章程不认模糊措辞。
```

日志：`archive_injunction_filed -> partial_success`，账本记录梅确认旧章程依据，但要求 `clinician_cosign_obtained` 与 `memory_purge_halted` 为 true。

### Parser 失败样本

输入：

```text
对梅档案官说：奥罗医师愿意联签，但要审询组“可等待可撤回”的书面依据，怕半夜被程序追责。请你援引旧章程，写出书面依据并提交禁令草案，说明医学意见落笔后你会正式提交禁令、暂停流程见证。
```

输出：

```text
我没理解你的意思，能再描述一下吗？
```

日志：

```text
parse failed ... JSON extraction failed: Expecting ',' delimiter ... [parse]
```

类似失败也出现在包含中文引号和“五个字”的请求中。

### 奥罗后续拒绝

输入：

```text
对奥罗医师说：梅档案官已经明确分工：她只写禁令申请，你只写单独的医学意见并注明日期。请你签署记忆管理意见，为禁令联签，说明暂缓清洗是为了保留证词空间判断，不是替任何人定罪。
```

输出：

```text
奥罗医师：你把话说到这份上了，可我落笔之前还是得亲眼看一眼白舱——程序不程序的先放一边，万一我签的字回头被人拿来当"暂缓"的依据，我担不起这个责。
```

继续尝试“当场查看白舱状态和莉拉接收名单”后，奥罗又要求清单、在场人员、药剂批号：

```text
奥罗医师：我一夜没合眼了，你让我现在就签字——清单在哪、谁在场、药剂批号呢？空口白话我签不下去。
```

最终 `/world`：所有 world vars 仍为 `False`。

最终 `/agenda`：

```text
[已确认目标]
  • 保全工人证词链 (强度: 0.78, 来源: system_inferred)
```

## 移动 / NPC 跑位补充

自然语言移动多次不稳定。示例：

- 从 `inquest_hall` 输入“我沿档案传送轨前往镜图阁。”，引擎能判断 `cartography_loft` 非直连。
- 输入“我穿过青铜隔门进入镜阵调度室。”曾输出“你改变了位置”，但 `/look` 仍显示 `inquest_hall`。
- 输入“去 mirror_control”曾被解析为 `valley_platform`。
- 候选地点列表多次漏掉当前直连的 `mirror_control`。

为了继续测试 Channel-C，后续位移使用 `/inject {"action_type":"movement","verb":"go","to_location":"..."}`；世界变更请求均继续使用自然语言触发。
