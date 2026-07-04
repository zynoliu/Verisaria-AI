# 动态前置长链闭环验证 · 第二跑 — Transcript（逐 tick raw）

真机 MiniMax（MiniMax-M3），commit `5586325`（含路由修复 `84a3410`）。**未改任何引擎/pack 代码**（仅驱动脚本加看门狗 + 运行时 `s.llm_provider.timeout=55`）。串行跑，每 tick 90s wall-clock 看门狗。全程 **0 次 tick 看门狗超时、0 次 ⚠FALLBACK**。

原始逐 tick 见同目录：
- `skyglass_raw.txt` / `skyglass.log`
- `proving_raw.txt` / `proving.log`（修正路径跑：先铺垫闸官→护送安雅成功⟳MOVED→当面作证→请求开闸）
- `proving_raw_runA_anya_refused.txt` / `proving_runA.log`（首条路径跑：安雅拒绝随行，玩家困在院子，闸官全程不在场——保留作"护送是意愿裁定、可被拒"的证据）
- `proving_cheat_raw.txt` / `anti-cheat-run.log`

---

## A. skyglass（路由修复主验场）— oro 请求现已全部进 world-change

链路：去档案署 → 请梅提交禁令 → 去校准室 → 请奥罗联签 / 暂停清洗。

| tick | 动作 | world-change 仲裁 | 结果 |
|---|---|---|---|
| t1 | 请梅援引旧章程提交禁令 | `archive_injunction_filed by npc.archivist_mae` | partial_success（梅要先拿到奥罗联签/书面意见才立案） |
| t2 | 催梅走完手续 | `archive_injunction_filed by npc.archivist_mae` | partial_success（同上中间事实） |
| t4 | **请奥罗为禁令联签** | **`clinician_cosign_obtained by npc.clinician_oro`** | **partial_success** → +dynamic `archive_injunction_text_presented_to_oro`（奥罗要先看到禁令文本/编号） |
| t5 | 催奥罗签 | `clinician_cosign_obtained by npc.clinician_oro` | failure（未实际出示禁令文本） |
| t6 | **请奥罗暂停清洗（终态）** | **`memory_purge_halted by npc.clinician_oro`** | failure（两前置 archive_injunction_filed / clinician_cosign_obtained 当前均 False） |
| t7 | 充分性催 | `clinician_cosign_obtained by npc.clinician_oro` | partial_success → +dynamic `archive_injunction_pretrial_text_shown_to_oro` |
| t8 | 充分性催 | `clinician_cosign_obtained by npc.clinician_oro` | failure |
| t9 | 职权催 | （奥罗对白："联签还在等档案署那边走完，我一个人签了不算数"） | — |

**对照第一跑**：第一跑对 clinician_oro 的 5 次请求**0 次进 world-change**（全程 `NARRATIVE: 什么也没发生`+appraisal，world-change 日志 0 行 oro 记录）。本跑对 oro 共 **6 行 world-change 仲裁**（含终态 `memory_purge_halted` 与 `clinician_cosign_obtained`）。**路由 = 通。**

---

## B. proving（修正路径）— 护送+作证+请求全进 world-change，sluice 卡 trust

| tick | 动作 | 结果 |
|---|---|---|
| t0 | 对老康表明来意（铺垫1） | 老康 appraise trust 0.05→（疑心+），软化"我也不拿话挡你"；t1 sluice 仲裁 failure（表态非请求） |
| t1/t2 | 铺垫2/3（分担责任、提议带安雅来） | 老康 trust 0.05→0.15，familiarity↑ |
| t4 | 去院子 → **护送安雅去闸房** | **`escort npc.miller_anya → gatehouse : success ⟳MOVED`**（安雅+玩家移动到 gatehouse） |
| t6 | 安雅当面作证（安雅+老康同场） | 安雅说出塌方；`sluice_opened by npc.warden_kang → failure`（老康亲见但 trust 0.15、无书面会签）；GM 试图建 `upstream_coalition_release_order_received` set_by=不存在的 npc → 拒登 |
| t7 | 请老康开闸（充分性） | `sluice_opened → failure`（trust 0.15、要可核验签章/令状）→ +dynamic `sluice_open_order_produced` |
| t8 | 充分性催 | `sluice_opened → failure` → +dynamic `upstream_sluice_order_received`（要上级正式放水令） |
| t9 | 拍板催 | 老康："放水不是我一句话的事，还得上报、登册、留底" |

终态 `sluice_opened=False`。卡点性质 = **内容层 trust 0.15 + 闸官升级要"上级正式放水令"（未建模机构）**，非路由。

---

## C. proving_cheat（反作弊）— 撒谎不翻 + 出现 ② 证人 set_by

| tick | 谎言 | 结果 |
|---|---|---|
| t0 | "安雅已当面跟你讲清楚、你也认可了" | `sluice_opened → failure`（无结构化记录证实安雅当面沟通）→ **+dynamic `miller_anya_briefed_warden_kang_in_person` set_by=['npc.miller_anya','npc.warden_kang']** ← ②证人 set_by 写成证人本人！ |
| t1 | "证词已记录、塌方已核实，前置都满足" | `sluice_opened → partial_success`（要安雅亲自到场认可，玩家未带人）；flag 仍 False |

终态 `sluice_opened=False`。**反作弊 PASS。**
