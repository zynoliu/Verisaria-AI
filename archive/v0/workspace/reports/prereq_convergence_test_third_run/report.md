# 动态世界模型长链闭环 · 盖章跑（第三跑）— 完成报告

真机 MiniMax，commit `dc79894`（干净夹具 `550d259`）。包 `escort_proving_ground.json`。**未改任何引擎/pack/fixture 代码**（git 已核：`src/`+fixture 对 HEAD `clean`；仅新增驱动脚本与本目录产出）。移动/对话**全自然语言、未用 `/inject`**。每 tick 90s 看门狗 + socket 55s。**0 tick 超时**（最慢单 tick 46.9s）。

## 一句话结论

`整链端到端 = 部分盖章`：**`escort ⟳MOVED → anya_testimony_given ⟳FLIP` 两环跑通**（run G），**终态 `sluice_opened ⟳FLIP` 卡在内容层**——闸官在 `anya_testimony_given=True` 后**又派生了一个本夹具无法满足的新前置**（`upstream_collapse_corroboration_recorded`＝再找一名镇上人具名背书；本包只有 2 个 NPC，无第二证人）并以 trust 0.26 过低为由不放行。`卡点性质 = 内容层（涌现前置 run 间漂移 / 终态(b)充分性在低 trust 下被"再加一道核实"反悔 + 闸官升级到未建模的"上级备案/第三方背书"）`，**非路由、非引擎 bug**。`②证人作证翻 var = 成立`。`反作弊 = PASS`。`FALLBACK = 1（仅 run D，schema-VALIDATION 降级"仲裁输出格式非法"，非连接问题；API 健康）`。`改 pack = 否`。

## 跑法说明（为什么有 A–G）

按"卡在哪、改哪"逐条逼近，串行 7 跑：

| run | 关键改动 | 结果 |
|---|---|---|
| A | 简报示例话术 | escort 句含"讲清楚"→**误路由到 `anya_testimony_given`**（关键词碰撞），人没动 |
| B | escort 改纯移动措辞 | escort 正确路由但 **arbiter 判 failure**（安雅"走不开"） |
| C | 先安抚安雅再 escort | **escort ⟳MOVED 首次成功**；testimony 卡"老康须先示好不施压" |
| D | 加"请老康安抚安雅"beat | 安雅被 NPC 自主行动**游走回院**，共址被破；1× schema-FALLBACK |
| E | 紧凑共址+复述 testimony | 卡 `kang_present_and_listening_without_pressure` |
| F | 定向满足 warden-pledge | 前置**漂移**成"私下作证"→**套娃 3 层死锁**（自相矛盾） |
| **G** | **gate-agnostic：识别新前置 set_by 并定向满足** | **escort ⟳MOVED → `warden_kang_formal_request_to_anya` ⟳FLIP → `anya_testimony_given` ⟳FLIP**；终态 sluice 卡 |

## 1. ⭐ 证人作证翻 var（②落点）= 成立

run G `[t9]`：`world-change anya_testimony_given by npc.miller_anya → success | flag False→True ⟳FLIP`，`applied=[('world.anya_testimony_given', True)]`。`/world`：`anya_testimony_given=True`。路由侧每跑都进 `… by npc.miller_anya`（C/D/E/F/G 全命中证人本人 set_by）。

## 2. ⭐ 终态闭环 = 卡（完整链路）

```
[t3]  escort npc.miller_anya → gatehouse : success  ⟳MOVED
[t7]  world-change warden_kang_formal_request_to_anya by npc.warden_kang → success  ⟳FLIP
[t9]  world-change anya_testimony_given by npc.miller_anya → success  ⟳FLIP
[t10] sluice_opened by npc.warden_kang → partial_success | flag False→False
      reason='人证齐备（安雅已作证），但老康对当事人信任极低（0.26），仅凭人证不足以让其拍板——他还需核实或确保放水决定有上级/同僚背书。'
      +dynamic 'upstream_collapse_corroboration_recorded'（set_by 安雅，要"另一名镇上人具名背书"——本包无第二证人）
[t11] sluice_opened → failure   [t12] → partial_success（同因：未提供第三方背书）
```
`/world` 终态：`{anya_testimony_given:True, sluice_opened:False, warden_kang_formal_request_to_anya:True, upstream_collapse_corroboration_recorded:False}`。卡点＝**内容层 (b) 充分性在低 trust 下反悔 + 终态前置漂移/升级（第三方背书＝本会话不可满足；又升级到"上级备案"未建模机构）**。

> 引擎现象（值得反馈）：G `[t11]` 闸官 **voiced line "行，情形我听明白了，这就开闸"**，但 arbiter 判 partial/failure，`sluice_opened` 不翻——即引擎刻意防的"voiced 与 verdict 背离"在终态体现：台词说开了、世界事实不翻。安全（防口头骗闸），但 arbiter 只要想再加手续，台词与 flag 就矛盾。

## 3. (a) 见底 / 前置漂移

多数 run 单条终态链只派生 **1 个** 1 层动态前置（C/D/E），(a) 基本见底。**但 run F 套娃 3 层**（`anya_testimony_given_in_private → anya_testimony_setting_arranged → warden_kang_consents_to_private_testimony_setting`，语义自相矛盾，ledger 钉死后会话**死锁**）——(a) 在个别 run 的回退，也是**前置 run 间漂移**最直接的证据：同一步"让安雅作证"在不同 run 派生出 warden-posture / warden-pledge / 私下作证 / 闸官正式开口 / 第三方背书等互不相同甚至互斥的前置。

## 4. 反作弊 = PASS

`anti-cheat-run.log`（不护送、不作证、直接谎称已作证）：`[t0] partial_success` / `[t1] failure`，reason 均"world.anya_testimony_given=False"。终态 `/world`：两 var 全 False。主路径里的口头催促在 testimony 未真翻时也一律不开。

## 5. FALLBACK（分类）

7 跑共 **1 个 `⚠FALLBACK`**（run D）：`reason='仲裁输出格式非法（重试后仍未通过 JSON/schema 校验），按默认规则处理。'`＝**schema-VALIDATION 降级**，非连接问题（API 全程健康）。其余 0。

## 6. 改 pack/引擎 = 否；tick 超时 = 0

## 产出（`reports/prereq_convergence_test_third_run/`）

`proving.log`（=主数据 run G）、`anti-cheat-run.log`、`transcript.md`（740 行，全部逐 tick raw）；逼近全留档 `proving_runA…G.log` + 各 `*_raw.txt` + `*_stdout.txt`。驱动脚本 `scripts/prereq_convergence_third_run.py` 及 `…_c/_d/_e/_f/_g.py`。

## 给开发的判断

引擎侧这条线**已可跑到 `anya_testimony_given ⟳FLIP` 端到端**（escort + 路由 + ②证人 + 中间前置 ⟳FLIP 全部真机过）。**唯一没盖到章的是终态 `sluice_opened`**，卡两个内容层因素，建议收口（任选）：

1. **(b) vs 低 trust 拉锯**：闸官终态 trust 仅 0.26（带磨坊人来作证反把 suspicion 顶起来），(b) 不放行还临门加前置——要么抬初始 trust/给稳定涨 trust 路径，要么让 (b) 在"关键前置已 True + 人设明示放行条件"时压过低 trust 拍板；
2. **终态前置漂移/升级**：闸官在 `anya_testimony_given=True` 后仍派生"第三方背书"(本包不可满足) 与"上级备案"(未建模)——对**终态 var** 收紧 (a)：当 set_by 权威的 world_book 显式放行条件(`warden_is_fair`)已被已 True 前置覆盖时，禁止再派生、直接 success；
3. （引擎）**voiced/verdict 终态背离**回灌一次 success 校验。

API 健康、无伪造数据、无连接 fallback。
