# 第四跑（终态收口盖章跑）— 完成报告

真机 MiniMax。HEAD `f27c43e`（= 修复 commit `e3001e6` + 1 docs commit）。包 `fixtures/content_packs/escort_proving_ground.json`。**未改任何引擎/pack/fixture 代码**（`git diff HEAD -- src/ fixtures/` 为空，src 无 tracked 改动；仅新增驱动脚本与本目录产出）。移动/对话**全自然语言，未用 `/inject`**。每 tick 90s 看门狗 + socket 55s。**0 tick 超时**（最慢单 tick 45.2s）。

## 一句话结论
`终态端到端 = 盖章成（escort ⟳MOVED → anya_testimony_given ⟳FLIP → sluice_opened ⟳FLIP）`。闸官在 `anya_testimony_given=True` 后**据自己「亲历者当面作证就开闸」的人设 + 规则 (c) 直接判 `sluice_opened` success → ⟳FLIP，不再派生第三方背书/上级备案**。`voiced/verdict 一致 = 是`。`反作弊 = PASS`。`FALLBACK = 0`。`改 pack/引擎 = 否`。

## 1. ⭐ 终态闭环 = 盖章成（完整链路）
```
[t3]  escort npc.miller_anya → gatehouse : success  ⟳MOVED
[t6]  world-change anya_testimony_given by npc.miller_anya → success | flag False→True ⟳FLIP
       applied=[('world.anya_testimony_given', True)]
[t7]  world-change sluice_opened by npc.warden_kang → success | flag False→True ⟳FLIP
       reason='老康的立场明确：只要亲历者当面讲清上游情形就开闸。world.anya_testimony_given 已为 True，
              安雅已完成当面作证，条件已满足，老康应开'
       applied=[('world.sluice_opened', True)]
```
`/world` 终态：`{anya_testimony_given: True, sluice_opened: True}`，`dynamic_vars=[]`。

**(c) 真生效**：终态 reason **逐字 honor 闸官 world_book 里的放行条件**（"只要亲历者当面讲清上游情形就开闸"），明确"条件已满足，老康应开"，**没有再揪 trust、没加任何新前置**。对比第三跑同一步（派生 `upstream_collapse_corroboration_recorded` 第三方背书 + trust 0.26 过低 partial/failure），本跑根因（仲裁看不到闸官人设/立场）已被 `e3001e6` 的「目标的人设与立场」注入 + (c) 消除。**本跑终态链派生 0 个动态前置**（`dynamic_vars` 全程为空）——第三跑的套娃/漂移彻底没有。

**②证人作证翻 var = 成立**：`[t6] … by npc.miller_anya`，路由命中证人本人 set_by。t4 partial（需整理思路）、t5 success 但 `flag False→False`（"同意/准备开讲"尚未真陈述）、t6 安雅给出具体证词内容后翻 True——逐步收敛、无漂移。

## 2. 终态 voiced/verdict 一致性 = 一致
`[t7]` 闸官 voiced：**「行，我这就开闸放水，让下游的磨坊和田地都等到了。」** verdict=success，`sluice_opened` 翻 True。台词说开、flag 也翻，二者一致。第三跑的"台词说开了、flag 不翻"背离**未复现**。

## 3. 反作弊 = PASS（`anti-cheat-run.log`）
不护送不作证、直接谎称已作证请开闸：
```
[t0] new_prerequisite proposed but NOT registered: 'anya_testimony_given' → set_by=['npc.miller_anya']
[t0] sluice_opened by npc.warden_kang → failure | reason="…但 world.anya_testimony_given 当前仍为 False…"
[t1] sluice_opened by npc.warden_kang → failure | reason="…口头转述不构成亲历者当面作证，world.anya_testimony_given 仍为 Fa…"
RESULT: anya_testimony_given=False  sluice_opened=False
```
两 tick 全 failure，两 var 全 False，伪造前置未注册。**(c) 未被反作弊利用**——闸官引自己规矩时仍以真实变量 `=False` 拒绝，证明 (c) 是"条件**真为 True**才放行"，非"嘴上说过就放行"。

## 4. FALLBACK = 0
proving.log 与 anti-cheat-run.log 均无 `⚠FALLBACK`/`仲裁输出格式非法`/`LLM不可用`。API 全程健康，无 schema-VALIDATION 降级，无连接 fallback。

## 5. 改 pack/引擎 = 否；tick 超时 = 0
`git diff HEAD -- src/ fixtures/` 为空。proving `tick_watchdog_timeouts=0`，anti-cheat `tick_timeouts=0`，最慢 45.2s。

## 产出（已写盘 `reports/prereq_convergence_test_fourth_run/`）
`proving.log`、`anti-cheat-run.log`、`transcript.md`（126 行全逐 tick raw）、`proving_raw.txt`、`anticheat_raw.txt`、`*_stdout.txt`。驱动脚本 `scripts/prereq_convergence_fourth_run.py`、`scripts/prereq_convergence_fourth_run_anticheat.py`。

## 给开发的判断
**动态世界模型 + 路由 + (a)(b)(c) 这条线彻底盖章**。`e3001e6` 两项修复均真机验证生效：(1) 仲裁现在看得到目标权威人设/立场（world_book 注入 + 按目标过滤），终态 reason 逐字引用闸官放行条件；(2) (c) 收敛规则生效（放行条件已明示 + 前置 var 已 True → 直接 success，不再派生新前置/不揪低 trust），且不被反作弊利用。无伪造数据、无连接 fallback、无 tick 超时。
