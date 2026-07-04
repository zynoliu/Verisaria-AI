# Verisaria v1 分层真相世界模型草案（L2）

**状态**：初始草案（L2 Round 1–5 讨论后）  
**日期**：2026-07-04  
**版本**：v0.1

---

## 1. 核心定位

**A5 + 分层真相** 升级为 v1 **核心世界模型**，而非仅作为 `world_book` 的附加特性。

所有需要访问控制的知识/事实都通过统一的分层系统表达，成为 WorldState 的一等公民，与 `world_vars`、`fact_ledger`、`memory` 并列。

---

## 2. 五层模型（更新版）

| 层级 | 名称 | 描述 | 默认可见主体 | 备注 |
|------|------|------|--------------|------|
| **L-1** | Unknown | 客观存在但尚未被任何角色发现的知识 | 无（需被发现后进入其他层） | 需通过探索/事件“发现”后提升 |
| **L0** | Canonical | 世界公认的客观事实 | 所有角色 | - |
| **L1** | Faction | 阵营内部共识/宣传版本 | 同一 faction 成员 | 自由 NPC 通常没有 L1 |
| **L2** | Forbidden | 被刻意隐藏的知识 | 特定权限角色 | - |
| **L3** | Personal | 个人私有记忆/认知偏差 | 仅该角色自身 | 有记忆能力的 NPC 均有 L3；无记忆 NPC 可无 L3 |

---

## 3. 存储与查询策略（待技术设计阶段细化）

**当前阶段仅明确原则**：

- 采用**查询时过滤（query-time filtering）**作为主要策略。
- 所有知识记录需支持按 `layer` 和 `visibility` 进行动态过滤。
- 具体存储方案（关系型表、文档型数据库、向量数据库、混合架构等）及索引策略，**留待技术设计阶段评估**。

**本阶段不固化**：
- 表结构
- 存储引擎选型
- 查询优化细节
- 物理隔离 vs 逻辑隔离方案

这些问题将在后续技术架构设计中结合性能、可扩展性、一致性要求进行决策。

---

## 4. 访问控制规则

### 4.1 基本可见性

- **Player**：L0 + 所属 faction 的 L1 + 自己的 L3
- **NPC**：L0 + 所属 faction 的 L1 + 自己的 L3（严格 A5）
- **Advisor**：L0 + 玩家所属 faction 的 L1 + 玩家的 L3
- **God-view / Debug**：全部层级（必须通过独立 Inspector 获取）

### 4.2 实现方式

- `WorldState.get_knowledge(actor)` 根据 actor 的 faction、permissions 动态过滤
- `SnapshotMapper` 接收 `VisibilityContext` 参数
- LLM Prompt 构建阶段调用知识过滤接口

---

## 5. 对现有组件的影响

| 组件 | 影响 | 应对措施 |
|------|------|----------|
| **Protocol Snapshot** | 需要支持 VisibilityContext 过滤 | 新增 `Snapshot.v1.layered` 变体或扩展字段 |
| **LLM Prompt** | 只能注入可见层知识 | LLM Orchestrator 在 prompt 构建时调用过滤接口 |
| **FactLedger** | `partial_success` 默认进入 L0，可被标记为 L2 | FactLedger 记录增加 `layer` 字段 |
| **Memory Compaction** | Personal（L3）与公开知识压缩策略不同 | Memory 系统感知知识层级 |
| **Persistence** | 需要支持知识层索引和查询优化 | 增加 `knowledge_visibility` 索引 |

---

## 6. Evolution Notes

- 未来可支持“同一事实在不同层有不同版本”的多版本模型。
- 可扩展支持“临时可见层”（如任务/声望解锁 L2）。
- 谣言传播系统可基于 L1 → L0 的升级机制实现。
- 审计日志可记录“某角色在某时刻看到了某条 L2 知识”，用于误解/背叛剧情。

---

**版本历史**
- v0.1（2026-07-04）—— L2 Round 1–5 讨论后的初始草案。
