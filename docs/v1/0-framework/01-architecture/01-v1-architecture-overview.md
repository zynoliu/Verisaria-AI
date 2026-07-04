# Verisaria v1 初步架构全景报告（L4 & L3 阶段）

**日期**：2026-07-04  
**版本**：v0.1  
**状态**：基于已完成的 L4 × 2 和 L3 × 2 专题讨论

---

## 1. 目的

本报告将目前已完成的 4 个专题讨论成果进行整合，形成 v1 的**初步高层架构视图**，帮助团队在进入更细粒度设计或实现前，建立共同的整体认知。

---

## 2. v1 核心定位（回顾）

- **更大规模、更多涌现的活世界模拟器**
- **可玩性是首要导向**
- **多视角可配置**（传统玩家 + advisor 模式）
- **内容 authoring 门槛显著降低**（通过 LLM 辅助 + 结构化验证）

---

## 3. 已完成专题及其对架构的贡献

### 3.1 L4 专题（最高优先级）

**内容质量指标体系**（`docs/v1/10-l4/01-content-quality-indicators.md`）
- 建立了 Must（3 项）+ Recommended（4 项）+ Optional（1 项）的分层指标体系。
- 引入**强制 playability proof 门禁**。
- 与 LLM 内容生成形成强绑定，成为内容质量的“最后一道防线”。

**LLM 内容编排功能**（`docs/v1/10-l4/02-llm-content-orchestration-guidelines.md`）
- 明确功能定位为**半自动模式**。
- 规定了“生成 → 验证 → 有限修复（最多 3 次）→ 人工最终确认”的强制流程。
- 禁止全自动发布和无人工确认的低风险豁免。

### 3.2 L3 专题（次优先级）

**GameSession 拆解接缝设计**（`docs/v1/20-l3/01-gamesession-seam-design.md`）
- 将过度膨胀的 `GameSession` 拆分为 5 个独立接缝：
  - Command Adapter
  - Routing Layer
  - Persistence Adapter
  - Snapshot Mapper
  - LLM Orchestrator
- `GameSession` 最终定位为**轻量级生命周期协调器**。

**协议层演化指南**（`docs/v1/20-l3/02-protocol-evolution-guidelines.md`）
- 确立“**核心契约稳定 + 新机制扩展**”的演化原则。
- 提出使用 **Projection / Bridge / Inspector** 模式来支持新能力（advisor 模式、god-view、partial streaming、重放等），而非破坏原有 DTO。

---

## 4. v1 初步高层架构视图

```
用户 / 前端
    │
    ▼
Command Adapter（输入 → Intent）
    │
    ▼
GameSession（轻量协调器）
    ├── Routing Layer（流程路由）
    ├── LLM Orchestrator（LLM 调用编排）
    ├── Persistence Adapter（存档/读档）
    └── Snapshot Mapper（状态快照生成）
            │
            ▼
协议层（Command / Event / Snapshot + Projection/Bridge/Inspector）
    │
    ▼
内容质量指标体系（Must 强制 + Recommended 分层）
    │
    ▼
LLM 内容编排（半自动 + 验证 + 修复 + 人工确认）
```

**四个核心层面**：
- **内容层**：内容质量指标体系
- **生成层**：LLM 内容编排功能
- **运行时层**：GameSession + 5 个接缝
- **协议层**：稳定核心 + 可扩展视图机制

---

## 5. 已锁定决策清单（摘要）

**内容质量**：
- Must 指标强制执行 + 发布前 playability proof 门禁
- LLM 生成必须经过验证 + 有限修复 + 人工确认

**LLM 编排**：
- 仅支持半自动模式
- 禁止全自动发布

**架构**：
- GameSession 拆分为 5 个独立接缝
- 协议层采用 Projection/Bridge/Inspector 扩展模式

（完整清单见 `docs/v1/99-wrapup/99-discussion-wrapup-report.md` 第 4 节）

---

## 6. 结论与后续

目前 v1 的**核心技术方向和风险控制机制**已经通过 L4 和 L3 专题形成了初步框架。下一步可选择：

- 继续 L2 专题（A5 + 分层真相数据模型等）
- 进入实现阶段（指标验证器原型、接缝接口提取等）
- 进一步细化已锁定决策的接口与数据模型

---

**本报告完成**。
