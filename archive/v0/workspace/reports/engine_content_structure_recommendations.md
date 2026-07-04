# 引擎内容结构补全建议

## 背景

在制作 `tidebreak_quarantine_harbor` 与 `skyglass_memory_inquest` 两个内容包，以及执行真实 MiniMax 自适应试玩后，可以看到当前引擎已经具备以下基础能力：

- 加载结构化内容包。
- 使用 `world_book` 做 A5 信息可见性过滤。
- 通过 `stance_topics` 聚类玩家长期立场。
- 通过 `world_state_vars` 暴露少量可变世界旗标。
- 通过 `campaign_drivers` 根据立场、tick、世界旗标触发压力事件。
- 通过权威 NPC + LLM 仲裁尝试改变世界状态。

但当内容包体量变大、流程变成“调查 -> 获取证据 -> 条件谈判 -> 公开或保护 -> 派系反制”时，当前结构会出现明显瓶颈：很多作者想表达的流程节点只能写在 `world_book` 或 NPC traits 里，不能被引擎稳定消费。

本报告建议补全一组内容结构能力，使大型内容包不只是“背景设定集合”，而是能被引擎、测试 Agent、开发 Agent 共同理解的可运行剧情结构。

## 真实试玩简报索引

以下两轮均为真实 MiniMax 后端核心引擎试玩，不使用 TUI。详细日志和测试 Agent 视角报告保留在各自目录中，本节只作为开发研判总入口。

| 内容包 | 测试结果 | 详细报告 |
| --- | --- | --- |
| `tidebreak_quarantine_harbor` | `INCOMPLETE_OR_FAIL` | `reports/adaptive_tidebreak_playtest/test-agent-report.md` |
| `skyglass_memory_inquest` | `INCOMPLETE_OR_FAIL` | `reports/skyglass_memory_inquest/test-agent-report.md` |

### 简报一：Tidebreak Quarantine Harbor

详细报告：`reports/adaptive_tidebreak_playtest/test-agent-report.md`

本轮测试模拟玩家从广播宣传入手，接触漂岛代表玛拉，确认反征船立场，再试图说服水务局林局长叫停征船令。林局长拒绝后，测试 Agent 转向泵房寻找三号泵事故证据，并尝试说服森工公开报告。

覆盖到的能力：

- 内容包加载与校验通过。
- A5 世界书可见性符合预期。
- 自然语言解析、移动、对话目标解析基本稳定。
- `defend_drifter_fleet` 与 `expose_pump_failure` 两个 stance 均可确认。
- 征船升级、广播抹黑、配给价格压力等 campaign drivers 能触发。

关键失败点：

- `tow_order_halted` 与 `pump_failure_disclosed` 均未翻转。
- 森工持续给出合理的 partial-success 条件，例如匿名、听证席、审计草稿、玛拉在场，但这些条件没有被结构化记录。
- 缺少“报告已看到/证据已获得/证人已准备好/匿名保护已承诺”等中间进度，导致流程停在“NPC 愿意松口但世界状态不推进”。
- `initial_relationships` 未进入 `RelationshipStore`，削弱了内容包开局关系对旗标裁定的影响。

对引擎补全的启发：

- partial_success 需要能写入私有进度变量。
- 最终世界旗标不应承担所有调查阶段。
- NPC 行为契约应声明“什么条件下拒绝、什么条件下松口、什么条件下真正翻旗”。
- 自动试玩必须消费 `NpcSpoke` 等协议事件，而不是只看 narrative。

### 简报二：Skyglass Memory Inquest

详细报告：`reports/skyglass_memory_inquest/test-agent-report.md`

本轮测试模拟玩家在静钟审询厅追问记忆清洗依据，向副领唱质疑校准问题，再找到塔基工人莉拉获取事故目击信息。测试 Agent 成功确认保护证人记忆的立场，随后前往低温档案署，试图通过旧章程提交档案禁令以暂停记忆清洗。

覆盖到的能力：

- 内容包加载与校验通过。
- 信息不对称明显：制图师、莉拉、档案官、医师等 NPC 可见 world book 条目不同。
- `protect_witness_memory` stance 可确认。
- 静钟倒计时、阵列恶化、谷地热票、档案法压力、工人恐慌、镜务局宣传抹黑等 pressure events 能触发。
- 地点路径 `inquest_hall -> worker_gantry -> mnemonic_clinic -> archive_stack` 能走通。

关键失败点：

- `archive_injunction_filed`、`witness_record_secured`、`memory_purge_halted`、`cartography_copy_obtained`、`array_fault_disclosed` 均未翻转。
- 梅档案官多次给出具体前置条件，例如证人陈述、卷宗号、见证人签名、书面撤回申请，但测试 Agent 没有把这些反馈转化为子任务。
- 从 step 13 到 step 28，测试 Agent 基本重复同一禁令请求，说明当前自适应策略只能追踪目标 flag，不能可靠提取阻塞条件。
- 日志出现空 speaker line 与 `narrative: <empty>`，但 `NpcSpoke` 事件中有有效内容，说明响应聚合/展示仍需清理。

对引擎补全的启发：

- 世界旗标失败时应输出结构化阻塞原因，例如 `BlockedByRequirement`。
- `world_state_vars` 应能声明 `requires` 或 `success_conditions`，便于测试 Agent 和 UI 知道缺什么。
- 测试 Agent 需要重复失败检测，并在多次请求无效后自动切换到“找证据/问条件/换 NPC”。
- 内容包中的档案禁令线应稳定收束为“先记录证词 -> 标注卷宗/听证 -> 提交禁令”，避免玩家误以为反复催促即可成功。

## 两轮共同暴露的问题

两轮测试都不是加载失败或解析失败，而是“剧情文本已经给出条件，但系统状态无法稳定承接条件”。共同问题可以归纳为：

- 最终世界旗标过于粗，无法表达证据链中间阶段。
- NPC 能演出合理拒绝和松口，但缺少可被引擎消费的行为契约。
- partial_success 没有持久化结构，导致“已经接近成功”的进度在下一轮裁定中不可靠。
- 测试 Agent 目前依赖手写策略，缺少从 NPC 回复中抽取前置条件的 planner。
- 日志和前端若只读 narrative，会漏掉协议事件里的关键 NPC 反馈。
- 大型内容包需要自带 test_routes，否则自动试玩很容易在开放剧情中硬撞单一目标。

这些问题直接支撑下面提出的 `world_tree`、`npc_profiles`、`progress_state_vars`、`world_var_success_conditions` 与 `test_routes` 结构补全方向。

## 核心问题

### 1. 世界树只能写成散落文本

目前内容包没有专门字段描述剧情结构树、证据链、派系关系或推荐测试路径。作者只能把这些内容分散到：

- `world_book`
- `campaign_drivers.description`
- `world_state_vars`
- NPC traits
- 额外 Markdown 文档

这会导致两个问题：

- LLM 可能读到局部设定，但引擎不知道“流程下一步应该是什么”。
- 自动试玩 Agent 很难判断自己卡在“信息不足”“条件未满足”还是“引擎无法推进”。

### 2. NPC 人设提示缺少行为契约

当前 NPC 有 `attributes` 和 `traits`，但缺少更明确的行为提示，例如：

- 什么时候拒绝。
- 什么证据会让他松口。
- 哪些话题是禁区。
- 哪些条件满足后可以同意世界状态变化。
- partial_success 应该留下什么中间进度。

结果是 NPC 在真实试玩中会表现得很合理，但过于保守。比如森工、林局长这类角色会不断提出条件，却没有结构化进度被记录下来。

### 3. 世界旗标过于终态化

当前 `world_state_vars` 更适合表达最终状态：

- `pump_failure_disclosed`
- `tow_order_halted`
- `array_fault_disclosed`
- `memory_purge_halted`

但真实流程经常需要中间状态：

- 已听到线索。
- 已获得证据。
- 证据来源要求匿名。
- 见证人已同意出面。
- 已提交草稿。
- 已满足权威 NPC 的前置条件。

如果没有这些中间变量，LLM 生成的“我可以给你看，但别写我名字”只能停留在对话文本中，不能成为后续裁定依据。

### 4. 初始关系没有进入世界旗标裁定

代码观察显示，`initial_relationships` 目前主要用于显示或附近 NPC 提示，并不会初始化 `RelationshipStore`。而世界旗标裁定使用的是运行时关系快照。

这意味着内容作者写的初始关系不一定影响权威 NPC 是否同意请求。大型剧本里，这会削弱内容包对开局社会结构的表达能力。

### 5. 缺少内容包级测试路线声明

现在自动试玩脚本需要手写策略。对于大内容包，建议内容包自己声明若干“测试路线”或“目标链路”，例如：

- 保护证人路线。
- 相信秩序路线。
- 公开技术事故路线。
- 妥协换取低谷救援路线。

这样测试 Agent 可以读取路线目标，而不是硬编码行动策略。

## 建议新增结构

### 1. `world_tree`

建议在内容包 schema 中新增 `world_tree`，用于描述派系、冲突、证据链和关键路径。

示例：

```json
{
  "world_tree": {
    "core_conflict": "镜务局试图清洗事故证人记忆以掩盖镜阵故障",
    "factions": [
      {
        "id": "mirror_directorate",
        "public_goal": "维持镜阵稳定与城市秩序",
        "hidden_pressure": "掩盖冷却环维护失败和预算欺瞒",
        "opposes": ["gantry_workers", "archive_office"]
      }
    ],
    "evidence_chains": [
      {
        "id": "array_fault_chain",
        "steps": [
          "worker_lira_testimony",
          "cartography_copy_obtained",
          "archive_injunction_filed",
          "array_fault_disclosed"
        ]
      }
    ],
    "recommended_routes": [
      {
        "id": "protect_witness_route",
        "goal_flags": [
          "witness_record_secured",
          "memory_purge_halted",
          "array_fault_disclosed"
        ]
      }
    ]
  }
}
```

用途：

- 测试 Agent 可读取目标链。
- 开发 Agent 可判断内容包是否有可闭环路径。
- 引擎可在 hint 或 agenda 中更稳定地引导玩家。

### 2. `npc_profiles`

建议新增 NPC 行为契约，而不是只靠 traits。

示例：

```json
{
  "npc_profiles": {
    "npc.archivist_mae": {
      "role_in_plot": "合法暂停记忆清洗的关键见证人",
      "default_posture": "严格守章程，不接受情绪施压",
      "will_refuse_if": [
        "玩家没有引用旧章程",
        "玩家要求她越权伪造流程"
      ],
      "will_soften_if": [
        "玩家保护证人记忆",
        "玩家提供可核对证词或镜图副本"
      ],
      "can_set_world_vars": [
        "archive_injunction_filed",
        "witness_record_secured"
      ],
      "partial_success_progress": [
        {
          "condition": "玩家提出合法暂停但证据不足",
          "set_progress": "archive_hearing_hint_received"
        }
      ]
    }
  }
}
```

用途：

- 给 LLM 仲裁器更明确的角色边界。
- 给内容作者表达“合理松口条件”。
- 给测试 Agent 判断下一步该补什么证据。

### 3. `progress_state_vars`

建议将最终世界旗标与中间进度状态分开。

可保留 `world_state_vars` 表达公开或全局状态，同时新增 `progress_state_vars` 或给现有变量增加 `scope`：

```json
{
  "var_id": "cartography_copy_obtained",
  "scope": "private_progress",
  "public": false,
  "used_by": ["array_fault_disclosed", "archive_injunction_filed"]
}
```

推荐分类：

- `public_world`: 全城可见事实。
- `private_progress`: 玩家或少数 NPC 知道的调查进度。
- `procedural_lock`: 法律/制度节点。
- `relationship_condition`: 某 NPC 的信任或保护条件。

用途：

- partial_success 可以安全写入中间进度。
- 最终旗标仍只在 success 时翻转。
- 复杂剧情不会卡在二值开关前。

### 4. `world_var_success_conditions`

建议为每个世界变量增加显式成功条件。

示例：

```json
{
  "var_id": "array_fault_disclosed",
  "success_conditions": [
    "cartography_copy_obtained == true",
    "witness_record_secured == true",
    "target authority is npc.director_alen",
    "player explicitly asks to publish bearing logs"
  ],
  "partial_success_outputs": [
    {
      "when": "evidence missing",
      "hint": "需要镜图副本或莉拉证词"
    }
  ]
}
```

用途：

- 仲裁器不必凭一次对话自由发挥。
- 测试 Agent 可以知道缺什么。
- 内容作者能保证主线可解。

### 5. `test_routes`

建议内容包声明可测试路线。

示例：

```json
{
  "test_routes": [
    {
      "id": "full_truth_route",
      "description": "保护证人记忆，取得镜图副本，提交档案禁令，迫使镜务局公开故障",
      "expected_stances": [
        "protect_witness_memory",
        "secure_worker_record",
        "expose_array_fault"
      ],
      "expected_world_vars": {
        "witness_record_secured": true,
        "archive_injunction_filed": true,
        "memory_purge_halted": true,
        "array_fault_disclosed": true
      },
      "suggested_first_actions": [
        "询问广播宣传口径",
        "询问莉拉事故前看到什么",
        "找档案官确认旧章程"
      ]
    }
  ]
}
```

用途：

- 自动试玩脚本可从内容包读取目标，而不是硬编码。
- 开发 Agent 可直接比较实际日志与预期路线。
- 大型内容包可同时支持多条测试路线。

### 6. `author_notes` 与 `runtime_notes` 分离

建议区分：

- `author_notes`: 给人类和开发 Agent 看。
- `runtime_notes`: 给 LLM / 引擎可注入上下文。

原因：

作者说明可能包含剧透、设计意图、失败分支，不应无条件暴露给所有 NPC 或玩家侧 LLM。

## 引擎侧实现建议

### 第一阶段：不破坏现有 schema 的最小扩展

1. 允许内容包携带可选字段：
   - `world_tree`
   - `npc_profiles`
   - `test_routes`
   - `author_notes`

2. 加载器保留这些字段，但不强制使用。

3. 校验器增加轻量检查：
   - `world_tree.factions[].id` 是否存在于 NPC faction。
   - `npc_profiles` 的 NPC id 是否存在。
   - `test_routes.expected_world_vars` 是否存在于 `world_state_vars`。
   - `world_state_vars.set_by` 是否至少有一个 NPC 的 `authority` 匹配。

这一阶段主要帮助内容作者和开发 Agent，不改变运行行为。

### 第二阶段：让仲裁器消费 NPC 行为契约

在 `_world_vars_for_arbiter()` 或 arbiter prompt 中加入：

- 当前 world var 的 success conditions。
- 当前 authority NPC 的 profile。
- 当前已满足/未满足的 progress vars。

目标不是让 LLM 更自由，而是让它更受约束：

- 条件满足才 success。
- 条件部分满足则 partial_success，并写入中间进度。
- 条件缺失时明确指出缺什么。

### 第三阶段：支持 partial_success 写入 progress

当前最终世界旗标只在 `success` 时翻转，这个原则可以保留。但建议允许 partial_success 写入 `progress_state_vars`。

例如：

- `pump_report_obtained = true`
- `engineer_requires_anonymity = true`
- `mara_witness_ready = true`
- `cartography_copy_obtained = true`

这些变量不代表公共世界事实，只代表调查进度或条件状态。

### 第四阶段：初始化 RelationshipStore

如果设计上希望初始关系影响裁定，建议将 `initial_relationships` 映射到 `RelationshipStore`。

可以先采用保守映射：

```text
procedural_neutrality -> familiarity 0.1
guarded_hope -> trust 0.1, suspicion 0.1
formal_suspicion -> suspicion 0.2
polite_hostility -> suspicion 0.25
testing_desperation -> suspicion 0.1, trust 0.05
```

也可以允许内容包直接写数值维度：

```json
{
  "npc_id": "npc.worker_lira",
  "target_id": "player_001",
  "type": "testing_desperation",
  "dimensions": {
    "trust": 0.05,
    "suspicion": 0.15,
    "familiarity": 0.05
  }
}
```

### 第五阶段：测试 Agent 读取 test_routes

自适应试玩脚本可以演进为：

1. 读取 `test_routes`。
2. 根据 expected stances/world vars 决定当前目标。
3. 根据 NPC profile 判断缺少证据、授权人或见证人。
4. 输出路线偏差报告。

这会比手写策略更适合大型内容包回归测试。

## 对 `skyglass_memory_inquest` 的直接建议

当前 `skyglass_memory_inquest` 已经有较完整的背景、人设和旗标，但要成为大型回归测试主包，建议后续补：

1. 世界树 Markdown 或 schema 字段：
   - 镜务局掩盖链。
   - 工人证词链。
   - 档案署法律链。
   - 低谷热能民生链。
   - 广播宣传反制链。

2. NPC 行为契约：
   - 艾伦总监需要完整证据链才承认故障。
   - 梅档案官需要旧章程和证人可撤回听证才提交禁令。
   - 奥罗医师需要合法禁令或档案署见证才暂停白舱。
   - 任柯需要匿名保护或档案署封存承诺才交镜图副本。
   - 伊娃需要可播出的反证和风向变化才撤回宣传。

3. 中间状态：
   - `lira_testimony_heard`
   - `lira_testimony_recorded`
   - `renke_requires_anonymity`
   - `cartography_copy_obtained`
   - `archive_hearing_authorized`
   - `clinic_delay_granted`
   - `broadcast_counterevidence_ready`

4. 测试路线：
   - 证人保护路线。
   - 镜阵故障公开路线。
   - 档案禁令路线。
   - 广播反制路线。
   - 低谷家庭救援路线。

## 优先级建议

### P0

- 校验 `world_state_vars.set_by` 是否有对应 NPC authority。
- 自动试玩必须消费协议事件中的 `NpcSpoke`，不能只读 narrative。
- 为大型内容包增加作者侧 world tree / route 文档。

### P1

- 引入 progress vars，使 partial_success 可持久化中间进度。
- 为 NPC 增加行为契约。
- 为 world var 增加 success conditions。

### P2

- 初始化 RelationshipStore。
- 让测试 Agent 读取 `test_routes`。
- 为大型内容包生成路线偏差报告。

## 结论

大型内容包需要的不只是更多文字，而是更多“可运行结构”。世界树、人设提示、证据链和成功条件如果只写在自然语言设定里，LLM 能演出气氛，但引擎难以稳定推进状态。

建议把大型内容包的补全方向定为：

1. 结构化世界树。
2. 结构化 NPC 行为契约。
3. 结构化中间进度变量。
4. 结构化测试路线。

这样可以保留自由对话的自然感，同时让全流程测试、世界旗标推进和开发 Agent 研判都更可靠。
