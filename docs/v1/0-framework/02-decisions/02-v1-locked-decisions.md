# Verisaria v1 已锁定决策清单（L4 & L3 阶段）

**日期**：2026-07-04  
**版本**：v0.1  
**来源**：L4 × 2 + L3 × 2 专题讨论

---

## 1. 目的

本清单将目前已完成的 4 个专题中**已达成共识并锁定的决策**进行汇总，方便后续设计、实现、review 时快速引用，避免重复讨论。

---

## 2. 内容质量指标体系（L4）

**已锁定决策**：

1. 建立 **Must（强制）** 指标 3 项：
   - Routeability
   - Exit Reachability
   - Natural Language Discoverability

2. 建立 **Recommended（强烈建议）** 指标 4 项：
   - NPC 职掌 / 第三方人名清晰度
   - 状态收敛一致性
   - Faction-gated truth verifiability
   - Advisor-mode discoverability

3. 建立 **Optional（可选）** 指标 1 项：
   - 覆盖率 / 深度

4. 引入**强制 playability proof 门禁**：
   - 内容包发布前必须通过验证（可配置 warn/block）

5. 支持作者自定义验证规则。

6. 与 LLM 内容生成形成**强绑定**（见下节）。

**来源**：`docs/v1/1-discussion/l4/01-content-quality-indicators.md`

---

## 3. LLM 内容编排功能（L4）

**已锁定决策**：

1. 功能定位为**半自动模式**（唯一支持的模式）。

2. **禁止**以下模式：
   - 纯辅助工具模式（LLM 只生成草稿）
   - 接近全自动模式（LLM 生成 → 指标通过 → 可直接发布）

3. **强制流程**：
   - 生成后必须运行内容质量指标验证
   - 验证失败触发修复循环（最多 3 次）
   - 最终必须由人工确认后才能发布

4. **无低风险豁免**：所有 LLM 生成/修改的内容包都必须经过人工最终确认。

5. **审计日志**：每次生成必须记录 prompt 版本、验证结果、修复次数、人工确认状态。

6. **高风险内容**（faction-gated truth、复杂护送链、长链充分性）触发更严格验证。

7. 作者**不能关闭** Must 指标的自动修复，但可选择“仅报告模式”。

**来源**：`docs/v1/1-discussion/l4/02-llm-content-orchestration-guidelines.md`

---

## 4. GameSession 拆解（L3）

**已锁定决策**：

1. 将 `GameSession` 拆分为 **5 个核心接缝**：
   - Command Adapter
   - Routing Layer
   - Persistence Adapter
   - Snapshot Mapper
   - LLM Orchestrator

2. `GameSession` 最终定位为**轻量级生命周期协调器**：
   - 负责顶层生命周期管理
   - 持有各接缝引用
   - 不再直接实现业务逻辑

3. 采用**分阶段重构**策略：
   - 阶段一：接口先行 + 简单委托
   - 阶段二：逐步迁移逻辑
   - 阶段三：精简 GameSession

4. 向后兼容策略：保留现有门面方法，外部调用方影响最小。

**来源**：`docs/v1/1-discussion/l3/01-gamesession-seam-design.md`

---

## 5. 协议层演化（L3）

**已锁定决策**：

1. **核心不变**（严格保护）：
   - `Command`、`Event`、`Snapshot` 的核心语义和结构稳定性
   - 事件追加不可变原则
   - A5 授权边界在协议层上的体现

2. **扩展策略**：采用 **One raw truth + many views** 模式，通过新增 **Projection / Bridge / Inspector** 实现新能力，而非破坏原有 DTO。

3. **v1 需求映射**：
   - Advisor 模式 → `AdvisorProjection`
   - 长期持久化 → `PersistentSnapshot`
   - Partial streaming → `StreamEvent` / `ProgressEvent`
   - 外部客户端 / Replay → `ReplayCursor` + `BoundedReplay`
   - Debug / God-view → `DebugInspector` / `GodViewProjection`

4. **版本策略**：
   - 核心契约保持 v1.0 冻结
   - 新能力通过次版本或独立命名空间引入
   - 现有前端无需修改

**来源**：`docs/v1/1-discussion/l3/02-protocol-evolution-guidelines.md`

---

## 6. 总结

以上决策已通过 L4 和 L3 专题讨论达成共识，可直接用于后续设计和实现阶段。

如需调整，需重新发起专题讨论。

---

**清单完成**。
