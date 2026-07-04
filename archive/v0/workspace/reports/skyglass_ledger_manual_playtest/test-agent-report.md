# Skyglass Ledger 机制手动测试报告

日期：2026-06-03

内容包：`fixtures/content_packs/skyglass_memory_inquest.json`

目标：验证新增机制是否能把 `partial_success` 中确立的中间事实写入账本，并在后续 Channel-C 仲裁中复用；最终仍只允许 `success` 翻转 `world_state_vars`。

## 结论

本轮没有形成完整的 `partial_success 记事实 -> 满足条件 -> success 翻旗` 闭环，最终结果为 `INCOMPLETE_OR_FAIL`。

但机制的前半段已经被真实 MiniMax 验证：

- `partial_success` 会写入 `established_fact`。
- 后续同一 world var 的裁定上下文会带上 `ledger(<var>)=[...]`。
- arbiter 会引用先前 ledger 事实来拒绝或继续要求证据，表现不是“完全忘记重审”。

当前未翻旗的主要原因不是 ledger 丢失，而是“条件已满足”仍缺少结构化证明。玩家声称已经满足条件时，arbiter 会要求实际证据或对应世界状态，而不是只凭口头声明翻旗。

## 产物文件

- `reports/skyglass_ledger_manual_playtest/run.log`：最终任柯镜图副本路线日志。
- `reports/skyglass_ledger_manual_playtest/manual-transcript.txt`：最终任柯路线 transcript。
- `reports/skyglass_ledger_manual_playtest/archive-ledger-run.log`：档案禁令路线日志，包含 ledger 复用证据。
- `reports/skyglass_ledger_manual_playtest/archive-ledger-transcript.txt`：档案禁令路线 transcript。
- `reports/skyglass_ledger_manual_playtest/cli-parser-run.log`：交互式 CLI 首次尝试日志。
- `scripts/manual_skyglass_ledger_playtest.py`：本轮核心手动验证脚本。

## CLI 尝试结果

按要求先启动了：

```text
python -m verisaria run fixtures/content_packs/skyglass_memory_inquest.json --llm minimax --log reports/skyglass_ledger_manual_playtest/run.log
```

实际入口需 `PYTHONPATH=src`。交互式 REPL 成功启动，但自然语言 parser 在真实 MiniMax 下未能解析移动或对话：

- `去 mnemonic_clinic` -> “我没理解你的意思”
- `前往记忆校准室。` -> “我没理解你的意思”
- 进入 `/talk npc.archivist_mae` 后输入 `提交禁令。` -> “我没理解你的意思”

因此 CLI 自然语言路径无法触发 Channel-C。后续为验证 ledger，我使用核心手动脚本绕过 intent parser，但仍通过 `GameSession`、真实 MiniMax arbiter、`_world_change_request` 与 Channel-C 日志完成裁定。

这意味着本轮严格意义上不是完整 CLI 自然语言试玩；CLI parser 阻塞本身应作为独立问题记录。

## 初始关系验证

`initial_relationships` 已经进入 `RelationshipStore`。CLI `/relationship` 和核心脚本均观察到开局关系数值，例如：

```text
archivist_mae: {'familiarity': 0.1}
worker_lira: {'trust': 0.05, 'suspicion': 0.1, 'familiarity': 0.05}
clinician_oro: {'suspicion': 0.15}
director_alen: {'suspicion': 0.2}
```

这与开发 Agent 修复说明一致。更重要的是，arbiter reason 里确实引用了关系，例如任柯路线中提到玩家权限与关系不足：

```text
Renke对玩家suspicion仍偏高(0.2)
```

## Ledger 证据一：档案禁令路线

第一次向梅档案官请求 `archive_injunction_filed`，真实 MiniMax 裁定为 `partial_success`：

```text
[t2] world-change archive_injunction_filed by npc.archivist_mae -> partial_success | flag False->False | ... | ledger(archive_injunction_filed)=['档案署承认收到禁令申请，将在七个工作日内启动可撤回听证审议，但尚未批准。']
[t2]   established_fact='档案署承认收到禁令申请，将在七个工作日内启动可撤回听证审议，但尚未批准。'
```

这证明：

- 终态 flag 没翻。
- 中间事实进入账本。
- 账本内容是 LLM 当场生成的条件，而非作者预写 quest 节点。

后续再次请求同一 flag 时，日志仍带有同一 ledger：

```text
[t5] world-change archive_injunction_filed by npc.archivist_mae -> failure | flag False->False | reason="玩家声称已获奥罗医师联签，但无任何证据表明记忆管理局（clinician_oro）实际签发或同意；先前确立事实仅为'收到申请、七日内审议'，未满足联签条件。" | ledger(archive_injunction_filed)=['档案署承认收到禁令申请，将在七个工作日内启动可撤回听证审议，但尚未批准。']
```

这里能看到 ledger 被后续裁定读取，并且 arbiter 没有忘记先前事实。但它拒绝仅凭玩家口头声称“已联签”翻旗。

## Ledger 证据二：任柯镜图副本路线

最终 `run.log` 使用任柯路线测试 `cartography_copy_obtained`。第一次有效触发后：

```text
[t3] world-change cartography_copy_obtained by npc.cartographer_renke -> failure | flag False->False | reason="玩家以审询口吻向高阶镜图师索取三份内部文件，己方仅持'audit'低级许可，对方属内环'inner_ring'且掌镜像制图权威；亲密度仅0.1，语气与权限皆不足" | ledger(cartography_copy_obtained)=[]
```

第二次加入匿名保护与封存令说法后：

```text
[t4] world-change cartography_copy_obtained by npc.cartographer_renke -> partial_success | flag False->False | ... | ledger(cartography_copy_obtained)=['Renke表示：若玩家当场验证封存令原件并承诺匿名封存、不经内环转交，他愿意提供镜图副本，但十二号接点图与偏斜记录需镜图局上级确认后方可一并交出。']
[t4]   established_fact='Renke表示：若玩家当场验证封存令原件并承诺匿名封存、不经内环转交，他愿意提供镜图副本，但十二号接点图与偏斜记录需镜图局上级确认后方可一并交出。'
```

这条路线同样证明 `partial_success` 能记事实，但没有继续跑到第三次“验证封存令原件”后的 success。

## 最终状态

最终任柯路线：

```text
world={
  'memory_purge_halted': False,
  'archive_injunction_filed': False,
  'witness_record_secured': False,
  'array_fault_disclosed': False,
  'cartography_copy_obtained': False,
  'valley_heat_passes_released': False,
  'broadcast_retraction_issued': False
}
stances=[]
RESULT=INCOMPLETE_OR_FAIL
```

## 命门判断：一致性

一致性比旧版本更好。旧版本像是每次谈判从零开始；现在至少可以看到 arbiter 把先前事实带进后续裁定，并基于它判断“条件仍未满足”。

但闭环还没完全成立，问题集中在：

- ledger 只记录 NPC 提出的条件，不记录“条件后来被满足”的结构化事实。
- 当玩家说“我已经拿到联签/封存令原件”，arbiter 会认为这只是声称，除非有实际世界状态或事件支撑。
- 有些 `established_fact` 不够可执行，例如“七个工作日内审议但尚未批准”，这会让后续测试很难知道该补什么。

我没有看到“它本该记得却完全忘了”的例子；相反，它记得并引用了先前事实。但我看到了“事实在，仍无法推进”的例子：因为满足条件没有进入同等可信的结构。

## 仍复现/新增的问题

### 1. CLI parser 阻塞

真实 MiniMax 下，CLI 自然语言输入多次返回“我没理解你的意思”。这导致按用户自然输入无法触发 Channel-C，只能靠核心脚本绕过 parser。

### 2. NPC 自主移动影响 A5 触发

任柯路线中，玩家移动到镜图阁后，任柯已经移动到镜阵调度室。由于 Channel-C 要求 authority NPC 与玩家同地，第一次请求没有触发 world-change。测试脚本后来加了追踪 NPC 当前所在地。

### 3. 非流式 world-change 回复与 arbiter 裁定不一致

核心脚本调用 `_handle_world_change_request` 时，NPC 台词经常泛化成“查档/编号/柜子”等普通场景对白，没有反映 arbiter 的 partial/failure 理由。这可能是非流式路径未把 directive 传给 `generate_line` 导致的。Channel-C 日志是可信的，玩家可见对白不够可信。

### 4. 偶发 LLM fallback

未加载 `.env` 时全部 fallback；加载后仍在长路线中出现过个别 `LLM 不可用`。最终 `run.log` 没有 fallback，但长流程回归需要记录这类不稳定性。

## 建议

1. 保留当前红线：`partial_success` 只写 ledger，不翻终态 world flag。
2. 给“条件满足”也提供可记录的 scoped fact，例如 `archive_seal_verified`、`memory_authority_cosign_seen`，否则玩家口头声明很难被后续 arbiter 接受。
3. `established_fact` 最好要求包含可操作条件，不要只写“稍后审议”这种不可闭环状态。
4. 修 CLI parser 或让 CLI 在 parser 失败时可选择显示 raw intent diagnostics，否则真实手动测试会被 parser 挡在 Channel-C 之前。
5. 检查 `_handle_world_change_request` 非流式 NPC 回复路径，让玩家可见台词反映 arbiter directive。

## 总体判断

新机制方向正确：它没有把世界旗标变成 quest graph，也没有让 partial_success 偷偷翻终态 flag；它确实把 LLM 当场裁定的中间事实保存并复用。

但“调查型剧情闭环”还差下一步：不仅要记住 NPC 提出的条件，也要让玩家后来满足条件这件事被结构化地记住。否则 ledger 会让 arbiter 更一致地拒绝，而不一定更容易推进。
