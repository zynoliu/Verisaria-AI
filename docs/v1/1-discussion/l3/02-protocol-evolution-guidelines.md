# Verisaria v1 协议层演化指南（L3）

**状态**：初始草案（L3 Round 1–4 讨论后）
**日期**：2026-07-04
**版本**：v0.1

---

## 1. 核心原则

**核心契约稳定 + 新机制扩展**

- `Command`、`Event`、`Snapshot` 的核心语义和结构保持稳定
- 事件追加不可变原则不变
- A5 授权边界在协议层上的体现不变

---

## 2. 扩展策略

采用 **One raw truth + many views** 模式，通过新增 **Projection / Bridge / Inspector** 实现新能力，而非破坏原有 DTO。

### 2.1 扩展模式说明

| 模式 | 用途 | 示例 |
|------|------|------|
| Projection | 为特定视角生成受限视图 | AdvisorProjection、GodViewProjection |
| Bridge | 在不同系统间传递数据 | PersistentSnapshot、ReplayCursor |
| Inspector | 提供调试/检查能力 | DebugInspector、BoundedReplay |

---

## 3. v1 需求映射

- Advisor 模式 → `AdvisorProjection`
- 长期持久化 → `PersistentSnapshot`
- Partial streaming → `StreamEvent` / `ProgressEvent`
- 外部客户端 / Replay → `ReplayCursor` + `BoundedReplay`
- Debug / God-view → `DebugInspector` / `GodViewProjection`

---

## 4. 版本策略

- 核心契约保持 v1.0 冻结
- 新能力通过次版本或独立命名空间引入
- 现有前端无需修改

---

**版本历史**
- v0.1（2026-07-04）—— L3 Round 1–4 讨论后的初始草案。
