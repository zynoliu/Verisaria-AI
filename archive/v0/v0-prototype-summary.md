# Verisaria v0 原型核心设计与价值总结

**版本**：v0.5.4-prototype  
**归档日期**：2026-07-04  
**用途**：作为 v1 重新设计前的参考基线与经验沉淀

---

## 1. 版本定位

Verisaria v0 是一个 **LLM 驱动的 RPG 世界引擎原型**，其核心目标是：

- 玩家用自然语言行动
- NPC 基于自身认知与立场回应
- 世界因玩家选择而真实改变
- 改变不依赖作者预写剧情图，而是通过结构化状态与 LLM 仲裁沉淀

v0 的设计哲学强调**强规则 + 可控后果**，而不是完全自由的生成式世界模拟。它验证了“把 LLM 降级为仲裁者/提案者，把世界真相放在结构化状态里”这条路的可行性，同时也暴露了在内容 authoring、系统扩展性、自动演化等方面的硬性限制。

**结论**：v0 已完成其历史使命，可以作为早期原型封存。后续若目标是“真实完整的模拟世界”，应启动 v1 重新设计，而非在此基础上持续叠加。

### 1.1 团队复核后的补充结论

本报告已由 architecture / content-testing / completeness 三个方向复核。复核后需要特别补充四点：

1. v0 的最大资产不只是后果三通道，也包括 **Command / Event / Snapshot 协议层**。它证明了“前端只是结构化 DTO 的适配器”这条路线是可行的，v1 不应回退到字符串渲染驱动。
2. A5 的核心不只是“不泄露私有记忆”，还包括 **world_book 的 faction-gated truth / forbidden knowledge 分层**。这套“不同阵营看到不同真相”的设计，是未来真实模拟世界里信息政治、谣言、宣传、误解系统的重要前身。
3. 内容包经验不能只总结为“lint 很重要”。真实教训是：**lint-green 仍可能不可玩**。路线可达、变量有效、关键词齐全，只能证明包结构合法；自然语言可发现性、路线提示、玩家是否知道该找谁、能否用自然措辞触发关键裁定，仍必须靠端到端玩测验证。
4. 测试规模表述必须带日期和命令。当前仓库的测试数与历史文档多次漂移，因此 v1 文档必须区分“历史基线”“当前收集结果”“特定命令下的通过结果”。

---

## 2. 核心设计原则（最值得继承）

以下原则在 v0 中被反复验证为正确，且对 v1 仍有直接指导意义：

### 2.1 A5 授权边界（A5 Principle）
- NPC 只能基于自己能感知/有权限知道的信息行动
- 协议层严格限制玩家可见的数据，绝不泄露 NPC 私有记忆或上帝视角
- **价值**：这是信息不对称与角色可信度的基础，v1 必须保留并强化

### 2.2 世界真相不在 Prompt 中
- 世界状态、事件、记忆、关系、世界变量、FactLedger 是唯一真相来源
- LLM 只能解释、提案、裁决、生成台词，不能直接改写世界
- **价值**：保证一致性、可解释、可回放，这是 v0 最核心的工程护城河

### 2.3 事件不可变（Event Log）
- 所有行动产生不可变事件，追加而非修改
- 观察（Observation）与信念（Belief）是主观投射，不等于事件本身
- **价值**：为长期记忆、传闻传播、历史追溯提供了可靠基础

### 2.4 后果三通道
- **Channel A**：关系（NPC 对玩家的多维评价，累积并影响后续仲裁）
- **Channel B**：立场（玩家长期态度聚类为可确认的 stance，可驱动剧情）
- **Channel C**：世界事实（权威 NPC + LLM 仲裁决定可变世界变量的翻转）
- **价值**：把“选择有后果”从口号变成可落地的机制，是 v0 最成功的玩家体验设计

### 2.5 FactLedger（涌现事实账本）
- `partial_success` 裁定中确立的中间事实会被记录，按 `regarding`（相关世界变量）过滤
- 只喂给 arbiter，不直接暴露给玩家
- **价值**：解决了“NPC 说了让步但下次就忘了”的问题，是长链谈判闭环的关键

### 2.6 动态世界模型 + 充分性闭环
- arbiter 可在裁定中声明新前置变量（`new_prerequisite`）
- 引擎支持去重、持久化、路由、流程成熟、护送、充分性兜底
- **价值**：让 GM（LLM）能在剧情需要时主动完善世界，而非完全依赖作者预写

### 2.7 可回放与确定性（A10）
- FakeLLM + 固定 seed + 确定性规则 = 关键路径可重放
- 这是调试、测试、内容验证的基石
- **价值**：v1 即使要增加涌现，也必须保留这条红线

### 2.8 协议先行与 UI 适配器原则

- v0 后期已经形成 `Command` / `Event` / `WorldSnapshot` 三族 DTO
- `EngineSession.submit_streaming` 证明长 tick 下事件流比同步返回字符串更适合作为 UI 基础
- TUI 的地图、附近 NPC、世界状态、关系、焦点、DEBUG god-view 等面板，本质都是 snapshot/event 的投影
- **价值**：v1 的 UI、调试器、自动测试 driver、外部客户端，都应共享同一个结构化协议，而不是各自读取内部状态或解析中文字符串

### 2.9 分层真相与信息政治

- v0 的 world_book 不只是 lore 文本，而是带访问控制的知识层
- canonical fact、faction propaganda、forbidden knowledge 等层级让不同 NPC 合法持有不同版本的世界解释
- **价值**：这可以自然扩展为 v1 的宣传、秘密、意识形态、阶级认知、政治叙事与谣言系统

---

## 3. 已验证的核心机制与价值

### 3.1 内容包与 CampaignLoader
- 内容包是纯 JSON，包含世界前提、实体、地点、世界书、世界变量、立场主题、campaign driver 等
- `CampaignLoader` 负责加载、校验、构建世界状态
- **lint 规则**（`PackEditor`）已覆盖：
  - `world_var_unsatisfiable`：set_by 必须指向真实 NPC
  - `world_var_no_keywords`：必须有 request_keywords
  - `world_var_near_duplicate`：避免语义重复
  - `world_var_unreachable`：满足者必须可达
- **经验**：lint + authoring guide 极大降低了内容闭环失败率

### 3.2 世界状态与事件系统
- `WorldCore` + `WorldState` + 不可变 `EventLog`
- 支持 tick 推进、移动、物理动作、状态变更路由
- `WorldState` 包含 entities、locations、world_vars、clock、weather 等
- **价值**：结构化状态 + 事件日志的组合，支撑了持久化、回放、调试

### 3.3 LLM 提供者层
- `FakeLLMProvider`：确定性测试/离线开发
- `OllamaProvider`：本地可选 provider（早期方案）
- `OpenAICompatibleProvider`：MiniMax 等云端主线 provider（通用类，只通过配置区分）
- `LLMOrchestrator`：预算控制、优先级降级、重试、fallback
- **经验**：
  - 把 MiniMax 当成配置而非专用类是正确决策
  - 可选 provider 的集成测试必须用 env/marker 隔离，否则会持续制造噪音

### 3.4 后果三通道实现
- **关系（Channel A）**：`RelationshipAppraiser` + `RelationshipStore`，支持并发评价、后台化、边际递减
- **立场（Channel B）**：`AgendaService` 支持聚合、自动确认、持久化、pack 主题聚类
- **世界变量（Channel C）**：`set_world_var` 带声明+mutable 闸门，支持动态前置、pending process、escort、充分性闭环
- **价值**：这三条通道是 v0 最能让玩家感受到“选择有分量”的部分

### 3.5 活世界系统
- **时间**：`worldclock` 模块，按 pacing 赋予不同分钟权重（SLOW≈3min，FAST≈30min）
- **天气**：气候阶梯随机游走，确定性、可重放
- **作息**：包级 opt-in（`npc_daily_rhythm`），支持 `stationed` 守岗 NPC
- **沉浸注入**：时段/天气进入 NPC 对白 prompt + 过渡环境叙述
- **价值**：让世界在玩家不行动时依然在运转，是“活世界”的基础

### 3.6 动态世界模型与 FactLedger
- arbiter 可声明新前置变量
- FactLedger 记录 partial_success 确立的中间事实
- 支持流程成熟、护送意愿裁定、充分性兜底
- **价值**：极大提升了长链调查/谈判的可玩性与真实感

### 3.7 协议与前端分离
- `EngineSession` 提供 `submit` / `submit_streaming` / `snapshot`
- Command / Event / Snapshot 三族 DTO，JSON 可序列化
- TUI 基于协议层实现，CLI 保留部分过渡命令处理
- **价值**：为未来多前端（TUI、像素 GUI、外部客户端）奠定了基础

复核补充：v0 的 UI 经验不应被视为“只是做了一个 TUI”。真正有价值的是：

- 前端不应该调用 `_show_world()`、`_show_agenda()` 这类字符串方法作为长期接口
- `Narration.text` 可以是成品散文，但关系、地图、议程、世界变量、附近实体、DEBUG 信息必须是结构化数据
- 长 tick 下必须支持 progress / streaming / partial event，否则 UI 会被真实 LLM 延迟拖垮
- DEBUG god-view 必须显式标记为越过 A5 的调试通道，不能混入玩家协议

### 3.8 Advisor / 第二人称模式的原型价值

`docs/design/game-modes-direction.md` 中的 advisor 模式没有实现，但它对 v1 很有启发：

- 当前 v0 默认玩家是世界里的行动者
- advisor 模式中，玩家是某个主角的脑内音 / 顾问，输入不是“我行动”，而是“我建议主角行动”
- 这要求区分“玩家身份”“焦点实体”“行动实体”
- **价值**：如果 v1 追求更完整模拟世界，advisor 模式提供了一条降低意图解析压力、强化角色自主性的产品路线

---

## 4. 架构与数据流总结

### 4.1 分层
- `engine/`：纯领域逻辑（world、rules、arbiter、memory、campaign、llm、validator 等）
- `runtime/`：`GameSession` —— 把引擎组装成一局游戏（tick 循环、存档、LLM 编排）
- `protocol/`：引擎与前端的类型化契约 + `EngineSession` 门面
- `frontends/`：CLI（REPL）、TUI（Textual）

### 4.2 典型一拍数据流
```
玩家输入
→ EngineSession.submit / GameSession.run_tick
→ IntentParser + CoherenceChecker
→ ActionComposer / InteractionService
→ 特殊路由（world-change、escort、arbiter、combat 等）
→ WorldCore 提交 Event + 状态变更
→ ObservationDispatcher
→ Subjectivity / Memory / Belief / Relationship
→ NPC 行为 + NPC-NPC 交互
→ Campaign Driver + 待处理流程
→ 协议事件推送
→ ResponseGenerator / 前端渲染
→ tick / 时间 / 天气 / pacing 推进
```

### 4.3 最大单点风险
- `GameSession` 方法极多、职责极重（300+ 引用）
- 建议 v1 在拆分前先提取稳定接缝（命令适配、world-change/escort 路由、持久化适配器、snapshot 映射）

---

## 5. 内容包模型与 Authoring 经验

### 5.1 当前内容包结构
- 纯手写 JSON
- 关键字段：`world_premise`、`initial_entities`、`initial_locations`、`world_book`（分层）、`world_state_vars`、`stance_topics`、`campaign_drivers`
- **没有**动态 schema、procedural 生成、经济/政治模型

### 5.2 Authoring 血泪经验（已固化进 `pack-authoring-guide.md`）
- 每个可变变量必须有真实可满足者（set_by）
- 必须有 request_keywords
- 避免近重复变量
- 终态放行条件要写进 label
- 前置要“够得着”
- 出口 NPC 必须可达
- 杠杆事实必须落在当事人自管的 var 上
- 护送/证人链需要特殊处理（关键词解耦、保障 var、合并重叠 var）

**经验**：即使机制完全正确，内容也极易卡死。lint + authoring guide 是目前最有效的降本手段。

### 5.3 lint-green 不等于可玩

团队复核指出，v0 总结原文仍低估了这一点。v0 的 playtest 经验显示：

- `CampaignLoader.validate` 和 `PackEditor.validate_pack` 只能证明结构合法，不能证明自然游玩可闭合
- 变量有 `set_by`、关键词、可达 NPC，也可能因为玩家不知道该找谁而不可玩
- 关键路线可能在作者表格里成立，但自然语言输入无法稳定触发对应 world-change 或 escort 路由
- 多跳移动、地名别名、NPC 职掌、第三方人名、同义关键词，都会影响“玩家是否能自然走到正确出口”
- 因此 v1 需要把 **line-level routeability / exit-reachability / natural-language discoverability** 当成内容质量指标，而不仅是 lint 指标

建议 v1 把内容验证拆成四层：

1. schema valid：JSON 和类型正确
2. lint clean：变量、关键词、可达性、近重复检查通过
3. routeable：自然语言能触发关键路径，至少有多种措辞样例
4. playable：端到端真人/driver 能在不知道答案的情况下走到结果

---

## 6. 测试与验证体系

### 6.1 测试规模
- 2026-07-04 使用 `uv run python -m pytest --collect-only -q` 收集到 1069 个测试项
- 同日使用 `uv run python -m pytest -q --ignore=tests/test_ollama_provider.py` 得到 1056 passed / 2 skipped
- 全量执行得到 1065 passed / 2 skipped / 2 failed，失败均为本机 Ollama 服务未运行导致的可选 provider 集成失败
- `docs/planning/TODO.md` 中仍保留历史基线 840 passed / 2 skipped，已明显滞后
- 覆盖 FakeLLM 确定性路径 + 大量端到端集成测试

### 6.2 验证方法
- FakeLLM + 固定 seed 实现关键路径可重放
- 真实 MiniMax / Ollama 集成测试（带 watchdog、日志、transcript）
- 反作弊专项验证（伪造前置不翻旗、吹牛不成功）
- 内容包 lint + load 验证

### 6.3 经验
- 可选 provider 的集成测试必须用 env/marker 隔离
- 真实 LLM 测试必须带超时与日志，否则极易中断丢失数据
- 反作弊是硬性红线，必须在每次真实玩测中抽查

### 6.4 端到端玩测优先于简化 harness

v0 多次证明：简化 harness 可能给出错误结论。例如只调用局部 NPC 行为收集，会绕过 subjectivity、memory、campaign、pacing 等完整管线，导致“复现”与真实 `run_tick` 行为不同。

v1 的测试策略应明确：

- 单元测试验证纯函数和局部规则
- 集成测试验证 GameSession / EngineSession 管线
- 真实 LLM playtest 验证自然语言可玩性、延迟、fallback、反作弊、内容闭环
- 所有 playtest 报告必须包含原话、事件、world vars、关系快照、关键日志频道和卡点定性

---

## 7. 关键教训与反模式

### 7.1 必须继承的教训
- Tick 延迟是硬伤，必须在架构层面考虑流式、后台化、快通道
- 意图解析极其脆弱，需要大量兜底与重分类
- 内容 authoring 成本极高，必须把 lint/authoring guide 作为一等公民
- `GameSession` 这种大而全的对象后期会成为重构噩梦
- 可选 provider 测试不隔离会持续制造噪音
- 文档容易漂移，必须有“当前状态”与“历史归档”的明确区分
- 结构合法不等于玩家能自然发现路径，内容必须验证可发现性
- UI 必须围绕结构化 DTO 与事件流设计，不能依赖引擎内部字符串输出
- world_book 分层真相是信息政治/误解/宣传系统的原型，不应在 v1 中丢失

### 7.2 建议 v1 避免的模式
- 继续在静态 schema 上叠加“动态”功能
- 让 LLM 直接改写世界状态
- 把过多 orchestration 逻辑塞进单一 `GameSession`
- 内容包完全手写且无工具链支撑
- 把可选 provider 的集成测试混在主线 suite 里

---

## 8. 对 v1 的直接建议

### 8.1 世界模型
- 考虑引入可扩展的实体/概念模型（动态 schema 或轻量 ontology）
- 明确“生成 vs 规则”的边界，决定是否支持玩家行为自动演化新概念

### 8.2 LLM 定位
- 保持“仲裁者/提案者”定位，还是升级为“世界模型演化者”？
- 无论如何，都要设计幻觉与一致性的防护机制

### 8.3 架构
- 在拆分 `GameSession` 前，先提取稳定接缝
- 保持协议层（Command/Event/Snapshot）的独立性
- 设计时就考虑多前端与外部客户端

### 8.4 内容与工具
- 把 `pack-authoring-guide.md` + lint 作为 v1 的标配
- 考虑是否需要可视化编辑器、自动检查、生成辅助

### 8.5 测试与 CI
- 建立清晰的测试 profile（offline deterministic / MiniMax smoke / Ollama optional）
- 引入 CI，锁定基线不退化

### 8.6 文档
- 建立“当前状态”文档，历史文档归档
- 版本号、provider 策略、测试命令必须与实际一致

---

## 9. 总结

Verisaria v0 是一个**成功但有明确边界的原型**。它验证了结构化世界运行时 + 后果三通道 + A5 边界 + FactLedger + 活世界等核心机制的可行性，同时也用真实血泪证明了：

- 静态 schema + 手写内容包难以支撑“真实完整的模拟世界”
- Tick 延迟、意图解析、内容 authoring 是三大硬伤
- `GameSession` 这种大集成对象需要尽早拆分

v0 的设计原则、已验证机制、authoring 经验、测试思路、反作弊红线，都是 v1 可以直接继承的宝贵资产。建议在启动 v1 需求研讨前，仔细阅读本报告与归档的原始设计文档，避免重复踩坑。

---

**归档说明**  
本报告与 tag `archive/v0.5.4-prototype` 共同构成 v0 原型的最终基线。后续 v1 开发应以此为参考，而非在此版本上继续增量修改。
