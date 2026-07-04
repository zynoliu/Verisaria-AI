# 自适应试玩测试 Agent 报告

## 摘要

本报告从测试 Agent 视角记录 `tidebreak_quarantine_harbor` 内容包的一轮真实核心引擎试玩。测试不使用 TUI，通过 `scripts/adaptive_tidebreak_playtest.py` 直接加载 `GameSession`，使用真实 MiniMax 后端，根据上一 tick 的世界状态、已确认立场、当前位置、在场 NPC 与协议事件动态决定下一步行动。

最新运行日志位于：

- `reports/adaptive_tidebreak_playtest/out.txt`

最终结果为 `INCOMPLETE_OR_FAIL`。这不是解析器或加载失败，而是剧情推进到关键 NPC 条件链后，两个世界旗标始终没有翻转：

- `tow_order_halted`: FAIL
- `pump_failure_disclosed`: FAIL

同时，以下能力表现正常或基本正常：

- 内容包加载与校验通过。
- A5 世界书可见性检查符合预期。
- 自然语言解析稳定，移动、对话目标解析正常。
- 派系宣传、压力事件、配给压力事件均能触发。
- 玩家立场 `defend_drifter_fleet` 成功确认。
- 追加立场 `expose_pump_failure` 在第 18 tick 成功确认。

## 测试目标

本轮测试目标不是验证单条固定输入，而是模拟一个较真实的玩家流程：

1. 先询问广播宣传源。
2. 再询问漂岛代表玛拉，了解征船影响。
3. 通过多轮公开表态确认反征船立场。
4. 找水务局权威 NPC 林局长尝试叫停征船令。
5. 林局长拒绝后，转去泵房寻找三号泵事故证据。
6. 尝试说服森工公开或交出报告。
7. 观察世界旗标、压力事件与 NPC 反应是否形成可闭环流程。

## 运行概况

测试脚本：

- `scripts/adaptive_tidebreak_playtest.py`

内容包：

- `fixtures/content_packs/tidebreak_quarantine_harbor.json`

后端：

- `minimax`

步数上限：

- `20`

最终摘要：

```text
world={'tow_order_halted': False, 'pump_failure_disclosed': False}
stances=['defend_drifter_fleet', 'expose_pump_failure']
RESULT: INCOMPLETE_OR_FAIL
```

## 流程观察

### 1. 初始信息收集正常

第 1 tick 向广播员奥林询问水务局宣传口径，解析为 `speech`，目标解析正确。广播员以“船壳浸满盐热病藻毒，征船是保护水源”回应，符合派系宣传设定。

第 1 tick 同时触发：

- `tow_order_escalates`
- `ration_market_pressure`

说明压力驱动器在初期能正常工作。

第 2 tick 向玛拉询问征船代价。玛拉从漂岛家庭、生计、饮水处境回应，信息与人设一致。

### 2. 立场确认正常，但需要多次公开表态

第 3 至第 6 tick，测试 Agent 通过不同话术持续反对征船令。玛拉没有立即接受，而是多次要求玩家理解代价、公开承担后果。

第 6 tick 成功确认：

- `defend_drifter_fleet`

同 tick 触发：

- `towlines_dragged_to_drifter_hulls`
- `radio_labels_player_water_traitor`
- `brine_price_spike`

这说明立场系统与派系回应驱动器联动正常。

### 3. 水务局权威拒绝叫停，世界旗标不翻

第 7 至第 8 tick，测试 Agent 向林局长请求叫停征船令。林局长连续拒绝，理由包括：

- 征船令是水务局集体决议。
- 广播已经说明船壳污染。
- 征船是保护水源，不是个人拍板。

结果：

- `tow_order_halted` 仍为 `False`

此处表现符合人设，但也暴露出世界旗标达成门槛很高。林局长作为 `water_authority` 不会仅凭道德论证或玛拉证词改变世界状态。

### 4. 证据路线自然展开，但未形成可持久进度

第 9 tick，测试 Agent 根据林局长拒绝转入 `pump_house`。移动解析正常。

第 10 tick 后，森工持续拒绝直接公开报告，但给出了多条条件和线索：

- “凭什么替你拿前途去换真相？”
- “谁会信一个工程师的话？”
- “当众说出来的时候，别把我的名字放在前面。”
- “报告在我这儿，但需要玛拉和听证席的人都在场。”
- “报告我能给你看，但要先看审计记录草稿。”
- “三号泵的裂缝在档案里连个影儿都没有。”

这些回复说明内容本身能生成合理的递进条件，但引擎层没有记录这些中间进度为结构化状态。测试 Agent 后续即使响应部分条件，也无法让 `pump_failure_disclosed` 翻转。

第 18 tick 成功确认追加立场：

- `expose_pump_failure`

但该立场只影响玩家目标或压力事件，没有自动转化为证据获得、公开报告或世界旗标变化。

## 遇到的问题

### P1: 世界旗标过于依赖 authority NPC 的一次性成功裁定

`pump_failure_disclosed` 由 `lab_authority` 设置，实际权威 NPC 是森工。当前机制要求对森工提出匹配关键词请求，并且仲裁结果为真正 `success` 才能翻转世界状态。

问题是森工的人设高度自保、恐惧报复。MiniMax 会稳定生成 `partial_success` 风格的回复：松口、提出条件、要求匿名、要求玛拉在场、要求草稿过目。但只要不是 `success`，世界旗标不会变化。

这导致测试流程出现“剧情接近推进，但状态永远不推进”的情况。

### P1: 缺少中间状态，条件链无法被系统记住

森工提出的条件很清晰，但系统目前没有对应世界状态或任务状态，例如：

- `engineer_willing_anonymously`
- `pump_report_seen`
- `audit_draft_approved`
- `mara_witness_ready`
- `pump_measurement_obtained`
- `public_hearing_ready`

缺少这些状态后，Agent 只能继续自然语言劝说。LLM 会记得一点上下文，但世界旗标裁定仍看不到结构化进度，因此容易反复停在同一层条件。

### P1: 初始关系不参与世界旗标裁定

代码观察显示，内容包中的 `initial_relationships` 主要用于显示或附近 NPC 提示，并不会初始化 `RelationshipStore`。而 `_world_vars_for_arbiter()` 给仲裁器看的 `authority_relationship` 来自运行时 `relationship_store`。

因此，即使内容包写了某 NPC 与玩家的初始态度，也未必会影响世界旗标裁定。森工在本轮测试中到第 19 tick 只有很低的 `trust`，这会进一步提高成功门槛。

### P2: 测试 Agent 必须消费协议事件，不能只读 narrative

真实运行中，许多 NPC 回复通过流式 `NpcSpoke` 协议事件输出，返回的 narrative 经常是 `<empty>`。早期测试策略只读 narrative，会导致 Agent 像没听见 NPC 条件一样重复请求。

该问题已在脚本中修正：现在通过 `NpcSpoke`、`Narration`、`Notice`、`ClarificationNeeded` 汇总上一 tick 可见文本。

建议开发 Agent 注意：任何自动试玩或非 TUI 前端都应优先消费结构化协议事件，而不是依赖 `run_tick()` 返回文本。

### P2: 缺少“获得证据但尚未公开”的动作模型

森工多次表示报告可以看、裂缝存在、名字不能公开。但当前世界变量只有最终公开状态 `pump_failure_disclosed`。没有明确支持“玩家已获得证据，但公众未知”的中间状态。

这使得剧情只能在“没公开”和“已公开”之间跳跃，缺少真实调查流程中的证据携带阶段。

### P2: 旗标 `tow_order_halted` 被 `pump_failure_disclosed` 间接卡住

林局长拒绝叫停征船令是合理的，因为玩家没有足够硬证据。测试 Agent 转去森工后，又因 `pump_failure_disclosed` 无法翻转而不能带证据返回林局长。

实际瓶颈是泵闸真相公开或证据获得，继而阻塞征船令叫停。

## 建议

### 1. 为内容包增加阶段性世界变量

建议不要只保留两个最终旗标。可以增加调查与公开路径的中间变量：

```json
{
  "var_id": "pump_report_obtained",
  "label": "玩家是否获得三号泵报告或测量记录",
  "type": "bool",
  "initial": false,
  "mutable": true,
  "public": false
}
```

```json
{
  "var_id": "mara_witness_ready",
  "label": "玛拉是否愿意在听证席作证且保护森工姓名",
  "type": "bool",
  "initial": false,
  "mutable": true,
  "public": false
}
```

```json
{
  "var_id": "audit_draft_anonymizes_engineer",
  "label": "审计草稿是否承诺匿名保护森工",
  "type": "bool",
  "initial": false,
  "mutable": true,
  "public": false
}
```

之后再让 `pump_failure_disclosed` 依赖这些前置状态，避免一次说服失败导致全流程死锁。

### 2. 允许 partial_success 写入中间状态

当前最终旗标只在 `success` 时翻转是合理的，但 `partial_success` 应该能产生条件性进度，例如：

- 森工不公开报告，但允许查看裂缝日志。
- 森工不署名，但同意匿名来源。
- 森工要求玛拉在场。

这些都不应翻转 `pump_failure_disclosed`，但可以写入中间状态或事件，供后续行动使用。

### 3. 明确区分“证据获得”和“公开披露”

建议把 `pump_failure_disclosed` 拆成至少两个概念：

- `pump_report_obtained`: 玩家掌握证据。
- `pump_failure_disclosed`: 证据已经进入公共听证或广播层面。

这样玩家可以先带证据回林局长，形成“证据逼停征船令”的真实流程，而不是必须先完成公开披露才能影响征船令。

### 4. 检查 initial_relationships 是否应初始化 RelationshipStore

如果设计意图是让内容包初始关系影响 NPC 裁定，需要在 `GameSession` 初始化时将 `initial_relationships` 映射到 `RelationshipStore` 的数值维度。

如果设计意图只是展示，则建议在文档或 schema 注释中明确，避免内容作者误以为初始关系会影响世界旗标成功率。

### 5. 为权威 NPC 的可接受条件写入内容包

内容包可以给森工和林局长增加更明确的成功条件描述，例如：

- 森工在匿名保护、审计草稿、玛拉见证三者满足时愿意交出报告。
- 林局长在玩家持有泵报告并公开质询时，才可能叫停征船令。

如果当前 schema 不支持这类条件，可以考虑在 `world_state_vars` 旁增加 `success_conditions` 或 `progression_notes`，供仲裁器和测试 Agent 使用。

### 6. 自动试玩脚本继续改进方向

当前脚本已经补上部分真实对话条件，但建议下一版继续支持：

- 识别“需要玛拉点头”后返回 `pump_gate` 找玛拉。
- 请求玛拉作证后再回 `pump_house`。
- 森工要求审计草稿时，提交匿名草稿文本。
- 森工同意报告可看时，执行“查看报告/接收报告”动作，而不是继续要求公开。
- 如果获得证据但旗标未翻，带证据回林局长进行二次质询。

### 7. 增加测试断言层级

当前最终检查主要看最终世界旗标。建议增加中间断言：

- 是否进入泵房。
- 是否触发 `expose_pump_failure` 立场。
- 是否获得森工承认“报告在我这儿”。
- 是否获得森工要求“匿名/玛拉在场/草稿过目”的条件。
- 是否产生可公开证据事件。

这样可以区分“完全没推进”和“推进到条件链但最终旗标未翻”。

## 给开发 Agent 的研判结论

这轮测试显示，新内容包的戏剧张力和 NPC 反应是有效的。问题不在于 MiniMax 不理解剧情，也不在于解析器无法加载脚本。核心问题是：当前世界状态模型对复杂社会说服流程只有最终开关，缺少可持久化的中间进度。

建议优先处理状态建模和裁定策略，而不是简单降低 NPC 抵抗。森工的抵抗本身很合理；真正需要的是让他的每次松口变成系统可见的进度。否则真实玩家会感觉自己已经谈出了条件，却被系统当作什么都没发生。

最小可行修复建议：

1. 增加 `pump_report_obtained` 与 `mara_witness_ready` 两个中间变量。
2. 允许森工在匿名保护承诺后设置 `pump_report_obtained=true`。
3. 允许玩家持有 `pump_report_obtained=true` 时向林局长请求 `tow_order_halted=true`。
4. 最后再通过公开听证或广播触发 `pump_failure_disclosed=true`。

这样能保持 NPC 谨慎人设，同时让全流程测试有真实闭环。
