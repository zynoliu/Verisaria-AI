# Verisaria v1 GameSession 接缝设计草案（L3）

**状态**：初始草案（L3 Round 1–4 讨论后）
**日期**：2026-07-04
**版本**：v0.1

---

## 1. 问题背景

当前 `GameSession` 承担了过多职责，导致代码膨胀、职责不清、难以测试和扩展。

---

## 2. 拆解目标

将 `GameSession` 拆分为 5 个独立接缝，使其成为轻量级生命周期协调器。

### 2.1 五个核心接缝

| 接缝 | 职责 | 输入 | 输出 |
|------|------|------|------|
| Command Adapter | 将原始输入解析为 Intent | 玩家输入 / 外部事件 | Intent 对象 |
| Routing Layer | 根据 Intent 路由到对应处理流程 | Intent | 流程执行结果 |
| Persistence Adapter | 存档/读档、世界状态持久化 | WorldState / Snapshot | 持久化记录 |
| Snapshot Mapper | 生成当前状态快照 | WorldState + VisibilityContext | Snapshot DTO |
| LLM Orchestrator | 编排 LLM 调用、prompt 构建、响应解析 | Prompt 上下文 | LLM 响应 + 验证结果 |

---

## 3. GameSession 新定位

- 仅负责顶层生命周期管理（start、pause、resume、end）
- 持有各接缝引用
- 不直接实现业务逻辑

---

## 4. 重构策略

采用分阶段重构：
1. 阶段一：接口先行 + 简单委托
2. 阶段二：逐步迁移逻辑
3. 阶段三：精简 GameSession 至协调器角色

---

## 5. 向后兼容

保留现有门面方法，外部调用方影响最小。

---

**版本历史**
- v0.1（2026-07-04）—— L3 Round 1–4 讨论后的初始草案。
