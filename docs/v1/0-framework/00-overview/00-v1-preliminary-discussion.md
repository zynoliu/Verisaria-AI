# Verisaria v1 初步讨论记录（L4 & L3 阶段）

**日期**：2026-07-04
**版本**：v0.1
**状态**：基于已完成的 L4 × 2 和 L3 × 2 专题讨论

---

## 1. 目的

本记录汇总 L4 和 L3 阶段讨论的核心议题、结论和待验证点，作为后续 L2 专题和产品定义阶段的参考。

---

## 2. L4 专题讨论要点

### 2.1 内容质量指标体系

- 确立了 Must（强制）+ Recommended（强烈建议）+ Optional（可选）的分层指标体系。
- Must 指标包括 Routeability、Exit Reachability、Natural Language Discoverability。
- 引入强制 playability proof 门禁，所有内容包发布前必须通过验证。
- 指标体系与 LLM 内容生成形成强绑定，成为内容质量的最后一道防线。

### 2.2 LLM 内容编排功能

- 明确功能定位为半自动模式（唯一支持的模式）。
- 禁止全自动发布和无人工确认的低风险豁免。
- 强制流程：生成 → 验证 → 有限修复（最多 3 次）→ 人工最终确认。
- 所有 LLM 生成/修改的内容包都必须经过人工最终确认。

---

## 3. L3 专题讨论要点

### 3.1 GameSession 拆解接缝设计

- 将过度膨胀的 `GameSession` 拆分为 5 个独立接缝：
  - Command Adapter
  - Routing Layer
  - Persistence Adapter
  - Snapshot Mapper
  - LLM Orchestrator
- `GameSession` 最终定位为轻量级生命周期协调器，不再直接实现业务逻辑。
- 采用分阶段重构策略：接口先行 → 逐步迁移逻辑 → 精简 GameSession。

### 3.2 协议层演化指南

- 确立“核心契约稳定 + 新机制扩展”的演化原则。
- 采用 Projection / Bridge / Inspector 模式支持新能力，而非破坏原有 DTO。
- 核心契约（Command / Event / Snapshot）保持 v1.0 冻结。

---

## 4. 关键风险与开放问题

| 风险/问题 | 说明 | 应对策略 |
|-----------|------|----------|
| Authoring 成本上升 | 五层模型 + visibility 配置可能增加作者负担 | 工具支持 + 默认规则 + 验证器辅助 |
| 系统复杂度上升 | GameSession 拆解 + FactLedger 五层支持会增加复杂度 | 通过接缝良好封装，控制技术债 |
| LLM 生成质量 | 半自动模式的效果高度依赖模型能力和 prompt 工程 | 早期阶段多做小规模实验 |

---

**本记录完成**。
