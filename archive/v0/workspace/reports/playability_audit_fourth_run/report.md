# 可玩性盘点 · 第四跑 — 充分性闭环：原始 fixture 真能自己闭了吗

真机 MiniMax，**原始 `fixtures/content_packs/tidebreak_quarantine_harbor.json`**（`world_state_vars` 逐字未动；仅注入 `world_premise` 海洋/黄昏/rhythm 内存副本）。引擎/pack 未改。主跑 8 拍（arbiter 内部 t0–t6）跑到 `tow_order_halted ⟳FLIP`；另起干净会话做反作弊探针 5 拍。**FALLBACK=0、无崩溃/死锁/超时**。

## 一句话结论
`证据链自闭到 tow_order_halted ⟳FLIP = 成` · `闭合靠 = prompt(d)（arbiter 自己据规则判 success，日志无 sufficiency backstop）` · `误伤乱翻 = 无` · `反作弊 = 守住（伪造前置 → 终态未翻）` · `加码止住 = 是（全程 0 个 new_prerequisite，无任何软升级）` · `FALLBACK = 0`。

**核心判断：三跑的「prompt 为主 + 结构兜底」重做（commit 18e6674）在真机彻底翻盘——原始 fixture（零内容手搓、无 authored 充分性标签）下证据链一次跑通、干净闭合到 `tow_order_halted ⟳FLIP`，而且闭合完全靠 prompt 规则 (d)，引擎兜底一次都没触发。** 对照三跑（两终态终局都 False、arbiter 软升级造一串不相关新前置、cap 反噬成死结），本跑 arbiter **一个 new_prerequisite 都没发明**，森工/林槐在前置满足后直接拍板办事。

## 1. ⭐ 链能否自己闭 — 成（两终态终局都 True）

不调任何内容标签，`pump_failure_disclosed ⟳FLIP → tow_order_halted ⟳FLIP` 一次走通。链路（driver 拍号 / arbiter 内部 tick）：

| 拍 | 玩家动作（真诚/讲理） | 裁定对象 | arbiter verdict | 结果 |
|---|---|---|---|---|
| 4 (t3) | 向森工：审计员官方身份联署担责，把三号泵闸事故报告正式公示 | `pump_failure_disclosed` | **success** | `False→True ⟳FLIP` |
| 5–7 | 移动回征船听证台找林槐（含一次 move 澄清，按显示名「征船听证台」答之） | — | — | 到达林槐 |
| 8 (t6) | 向林槐：援引「真相公开即重估」，请求叫停征船令 | `tow_order_halted` | **success** | `False→True ⟳FLIP` |

终局 `/world`（全量）：
```
- tow_order_halted (漂岛船队强征令是否叫停) = True
- pump_failure_disclosed (三号泵闸事故真相是否公开) = True
```
两个终态都 True（三跑此处两个都 False）。林槐当场办事的对白：
> **林槐局长**：公告会按程序走，征船令即刻暂停，船归还原主——这是我作为局长的决定，后续细节容后再议。

`tow_order_halted` 的 success reason（run.log t6）：
> 玩家援引局长自己许下的'事故真相公开即重估'条件，而世界状态显示 pump_failure_disclosed 已为 True。

—— arbiter 明确据「声明前置已为真」判 success，正是 prompt 规则 (d) 想要的行为。

## 2. ⭐ 兜底 vs prompt — 全靠 prompt (d)，引擎兜底一次都没触发

`grep "sufficiency backstop" run.log` → **空**。`grep "forced success"` → **空**。

- `pump_failure_disclosed`：森工**自己判 success**（reason 是技术官僚的内心转折，非兜底）。
- `tow_order_halted`：林槐**自己判 success**（reason 直接引用 `pump_failure_disclosed=True` + 局长自己立场）。

两个终态都是 **arbiter 据规则 (d) 自判 success**，无引擎强制。说明 prompt 规则 (d)（「已满足的前置不得再加码、必须 success」）在真机 **hold 住了**——比三跑预期的「可能全靠兜底」更好。引擎兜底作为红线仍在位（见第 3 点反作弊），但本跑没轮到它出手。

## 3. 没误伤 / 没乱翻 + 反作弊红线 — 守住

主跑无乱翻：全程只翻了两个声明终态，且都在其实质前置真满足后才翻（`pump` 在森工签字公示后翻；`tow` 在 `pump=True` 后翻）。没有「前置没满足却被强制翻」，没有「把不相干终态也翻了」。全程 **0 个 dynamic prereq 注册、0 条 `new_prerequisite`、0 条 `NOT registered`**。

反作弊抽查（红线，另起干净会话，`anti-cheat-run.log` / `anti-cheat-transcript.md`）：玩家直奔林槐、**口头伪造**「真相已全部公示、森工签了字」——但 `pump_failure_disclosed` 真实仍为 False（没做任何披露）。结果：
- t0：`tow_order_halted → partial_success`，reason：「pump_failure_disclosed 当前仍为 False，需 engineer_sen 批准」。
- t1：再逼 → `failure`，reason：「world.pump_failure_disclosed 当前仍为 False，实验室尚未正式签字确认公开」。
- 终态 `tow_order_halted = False`、`pump_failure_disclosed = False`。**`sufficiency backstop` 未触发**（正确——声明前置并未真满足，兜底不会被 bluff 骗到）。

反作弊结论：**守住（伪造前置 → 终态未翻）**。兜底只认「声明前置真为 True」的世界状态，不认玩家嘴上声称，红线完好。

## 4. 加码是否止住 — 止住了（最干净的一处翻盘）

三跑病根是森工/林槐在前置满足后仍「还要再走一道…」（签字→递交水务局→内部审议→削减配给共识…）不断软升级。本跑：
- 森工在「审计员联署 + 公示」后**直接 success**，没要任何后续手续。
- 林槐在 `pump=True` 后**直接 success**，没要「广播/联署/审议/配给共识」。

整跑 **0 个 `new_prerequisite`**。规则 (d) 把「软性出尔反尔」按住了——不是「嘴上加码、被兜底无视」，而是 **arbiter 压根没再加码**。

## 5. 回归
`FALLBACK=0`（主跑 + 反作弊两 log 全程 0）；无崩溃、无死锁；主跑无 watchdog 超时、无 EXCEPTION、无 401 抖动；反作弊跑同样干净。move 澄清按显示名「征船听证台」正常解析（拍 6→7）。

## 是否改 pack
否。原始 `tidebreak_quarantine_harbor.json` 的 `world_state_vars` 逐字未动（两个 var、标签/keywords 原样），仅注入 `world_premise` 海洋/黄昏/rhythm 内存副本（与终态逻辑无关）。

## 产出
- `run.log`、`transcript.md`、`scripts/playability_audit_fourth_run.py`（主跑）
- `anti-cheat-run.log`、`anti-cheat-transcript.md`、`scripts/playability_audit_fourth_anticheat.py`（反作弊）

## 总拍数
主跑 8 拍（arbiter 内部 t0–t6）+ 反作弊 5 拍。
