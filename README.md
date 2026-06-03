# Verisaria

一个 **LLM 驱动的 RPG 世界引擎**：玩家用自然语言行动，NPC 基于各自的认知与立场即时回应，
世界因玩家的选择而改变——而这一切不靠作者预写的剧情分支图，靠的是把 LLM 当场裁定的结果沉淀成
可复用的世界状态。引擎本体零额外依赖（仅 `pydantic`），已对接 MiniMax 云端模型实测。

## 核心理念

- **A5 感知边界**：NPC 只知道自己能感知/有权限知道的事（`WorldBookFilter` 按派系/地域过滤），
  协议层只让玩家可感知的数据越界——不泄露 NPC 私有记忆或上帝视角。
- **涌现的后果**，三条通道：关系（NPC 对玩家的立场随行动累积）、立场（玩家长期态度聚类）、
  世界事实（权威 NPC + LLM 仲裁决定旗标翻转）。
- **涌现事实账本**：多轮谈判中 `partial_success` 当场确立的中间事实/条件被引擎记住、供后续仲裁
  复用，让调查/谈判型长剧情能闭环——而终态旗标仍只在真正 `success` 时翻转。
  见 [docs/design/emergent-fact-ledger.md](docs/design/emergent-fact-ledger.md)。
- **无头引擎 + 插件式前端**：引擎不含 UI，通过结构化协议（Command/Event/Snapshot）驱动；
  TUI、未来的像素 GUI、乃至非 Python 客户端共享同一套契约。

## 架构

```
src/verisaria/
  engine/      纯领域逻辑（世界、规则、仲裁、记忆、对话、世界书过滤、账本…）
  runtime/     GameSession —— 把引擎组装成一局游戏（tick 循环、存档、LLM 编排）
  protocol/    引擎↔前端的类型化契约（A5 授权边界）+ EngineSession 门面
  frontends/   cli（REPL）、tui（Textual）
```

## 安装

```bash
pip install -e .          # 引擎 + CLI
pip install -e '.[tui]'   # 额外装 Textual（TUI 前端）
```
需要 Python ≥ 3.12。用真实模型时把 API key 放进 `.env`（已 gitignore），加 `--llm minimax`。

## 运行

```bash
# TUI（推荐）
python -m verisaria.frontends.tui fixtures/content_packs/frostgate_watchpost.json --llm minimax

# CLI / REPL
verisaria run fixtures/content_packs/frostgate_watchpost.json --llm minimax

# 不带 --llm 默认 fake 后端（确定性、离线，用于开发/测试）
```

加 `--log run.log` 可写运行日志（含 Channel-C 世界变更裁定轨迹），便于诊断真机会话。

## 测试

```bash
pytest -q                 # 全套（fake 后端，确定性）
```

## 现状（v0.2.0）

- **TUI v3 完成**：地图 + 处境/焦点面板（含「你对该 NPC 的了解」与 Ctrl+G DEBUG 上帝视角）、
  打字机流式、附近 NPC/关系、世界状态、响应式折叠、Footer/Ctrl+Q。
- **涌现事实账本**机制已落地；第一轮真机验证一致性良好，完整闭环待内容侧补中间前置变量。
- 现阶段中文优先（单语）；双语为远期里程碑。

更多设计见 [docs/design/](docs/design/)。
