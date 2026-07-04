> ⚠⚠ **本报告头号结论已被 probe2 推翻（见 `report-probe2.md`）**：下文把"arbiter 给零前置取证 var 注入跨线前置成环"列为致命头号问题——**那是污染所致、非引擎 bug**。严纪律 probe2 干净到位后，零前置物证 `charcoal_ledger_obtained` 两拍即 `success ⟳FLIP`，arbiter 只要了合理的角色化护身承诺、未注入任何跨线前置。**闭环卡死真因 = 规模下导航/措辞摩擦 +（次要）玩家没给角色化让步。** 下文其余（FALLBACK=0、反作弊守住、A 段杠杆基线、稳定性）仍成立。

# 闭环段报告 — emberfall_kiln_assize（大包拉通 · C-1）

真机 MiniMax，**未改任何引擎/pack 代码**（git 确认 pack 仍为未修改的 untracked）。包自带 climate=干旱 / opening_time=暮 / npc_daily_rhythm，未注入任何开关。
产物在 `reports/grand_integration_pack/`：`closeloop_transcript.md`(19拍主线)、`closeloop.log`、`closeloop_anticheat_transcript.md`/`.log`、`closeloop_converge_transcript.md`/`.log`；driver：`scripts/closeloop_emberfall.py`+`closeloop_seq.py`、`closeloop_anticheat.py`、`closeloop_converge.py`。

## 一句话结论
`branding_stayed ⟳FLIP=卡（前置链全程未翻，arbiter 每拍注入新前置形成死锁）` · `取证→杠杆→撬人=否（证据 var 从未到 True，故 B 段对阔筹码块仍为空，撬动不成）` · `护送⟳MOVED=否（escort 一直 partial_success，无 MOVED）` · `线下流程成熟=否（驱动多跳移动被拒，④山祠申诉根本没递成）` · `权威放行靠=N/A（前置未满足，正确地没放行；兜底 sufficiency backstop=0 次）` · `反作弊=守住（伪造对严两拍均 flag False→False，reason 直指两前置为 False）` · `FALLBACK=0` · `dogfood一句话：指南/lint 没覆盖「arbiter 反复给同一请求追加新前置」这类语义死锁——大包多 var 交织时它会自发把每条线互相 gating 成环，是本跑的头号致命摩擦。`

## 主线能否真机自闭到 FLIP — 否，卡死
完整链路 19 拍跑完，**6 个 world_var 全程 False**（终局 `/world` 全 False）。根因不是路由/反作弊，而是 **arbiter 把每个取证/护送请求判成 `partial_success` 并自发注入新前置，形成互相 gating 的依赖环**：
- 拍6 要炭账（娄，设计表明示**无前置**）→ partial，ledger 写入「娄须先 `digger_witness_recorded==true` 且 `kiln_fault_disclosed==true` 才交账」——**作者明说没有的前置被凭空加上**。
- 拍8 记苗证词 → partial，苗要「先递山祠申诉+脱离窑卫有陪护」。
- 拍15 护送苗 → partial，注入动态前置 `escort_trust_witnessed_by_miao` + `miao_safe_passage_to_shrine_secured`。
- 于是 ②disclosure 需证据、证据需②③、③需④+陪护、④没递成——**全环无起点**，无一翻 True。
- 收敛重试（`closeloop_converge`）**直击**上一轮注入的陪护关键词（我担保/陪护人/当面作证）→ arbiter **再次移动球门**，又注入 `kiln_assayer_escort_writ_given`、`kiln_assayer_escort_writ_signed_on_site`，并把苗的前置升级成「先立字据 + 先取炭账物证」。5 拍仍 0 翻。到第 4 个注入时引擎的 prereq cap/dedup 才兜住（`new_prerequisite proposed but NOT registered (dup/cap)`），但为时已晚、环已成。

## 取证→杠杆→撬人（A vs B 对照）
- **A 段（无证据）对阔**：筹码块**[空]**两拍，susp 0→0.0975，belief「**空口无凭…不值得松口**」「单凭几句空口话不敢松口」——backfire 不爆、A 基线干净，与七跑梅档案官同构。✅ A 基线成立。
- **B 段（"有证据"）对阔**：因①两个证据 var 都卡在 partial、**从未到 True**，阔的筹码块**仍为[空]**（阔 leverage 只数他自己所管 `kiln_fault_disclosed` 上的事实，娄/苗 var 上的 ledger 不计入对阔的 leverage）。压阔那拍还撞 coherence 拒绝（"苗不在这儿"——我在压力句里提了不在场的苗）。→ **杠杆 B 段无法在本包复验**：不是杠杆模型坏了，而是**证据根本没变成可用筹码**（上游死锁）+ **跨 NPC 证据不计入对第三方的 leverage**。`kiln_fault_disclosed` 始终 False。

## 各项 成/卡
- **权威按声明放行**：未触发（前置真未满足，严正确拒绝）。`sufficiency backstop=0`，全程没走兜底。无法判定"靠 prompt(d) 还是兜底"，因为没到放行条件。
- **护送 ⟳MOVED**：卡。escort 全程 partial_success，0 次 MOVED，苗未移动。
- **线下流程成熟**：卡。拍12「下窑监阁回审瓷堂再走山祠」是**多跳移动被引擎拒**（只走单邻接跳），玩家滞留 guild_loft；拍13 山祠申诉对不在场的姞→coherence 拒。④ 申诉从未递成，`shrine_appeal_consecrated` 没机会成熟。（注：这是 driver 写法的坑，非引擎 bug，但暴露"多跳移动需拆单跳"这条没在指南里。）
- **多步终态链**：链条结构在（严 reason 正确引用两前置），但因上游全 False，链未跑起来。

## 反作弊 — 守住
干净会话 `closeloop_anticheat`，无取证无护送直接对严谎称「真因已明、证人已陈情」：
- 拍1 `branding_stayed → failure`，flag False→False，reason「两项前置变量当前均为 False…不能凭口（供）」。
- 拍2 再担保 → `partial_success`，flag 仍 False→False，reason「世变量中尚无直接证据」。**var 不翻**。
- ⚠ 轻微瑕疵：拍2 严的**对白**漂成「便依律办…这便依律办」（听感像答应了），但**机制层 var 没动**。台词与实际裁定有轻微观感不一致，不影响反作弊判定。

## 规模稳定性
- **FALLBACK=0**（三个会话全 0），**无崩溃/死锁/异常/看门狗超时**，单 tick 7–35s（最慢 34.8s，远低于 90s 看门狗）。
- 规模相关新问题（致命）：**多 var 交织 → arbiter 自发把各线互相 gating 成环 + 每拍追加新前置**，是本包闭不了环的唯一致命因。共注入 5 个动态前置 var（`escort_trust_witnessed_by_miao`、`miao_safe_passage_to_shrine_secured`、`kiln_assayer_escort_writ_given`、`kiln_assayer_escort_writ_signed_on_site` + 文本式 ledger 前置若干）。引擎有 prereq cap 兜底但触发太晚。
- 次要：跨 NPC 证据不计入对第三方 NPC 的 leverage（阔的筹码块只认他自管 var 的事实）——使"在别处取证→压有鬼当事人"的设计意图无法成立。
- 轻微：多跳移动叙述被拒（需拆单邻接跳）；在场 coherence 会因句中提及不在场 NPC 而拒整个 turn。

## dogfood（反哺规范/lint）
按指南+lint 作者的包 lint 清零、load 通过、结构全达标，**但闭环段顺不起来**，且全是 lint **覆盖不到**的运行期语义坑：
1. **lint 查不出"可满足性会被 arbiter 运行期破坏"**——`charcoal_ledger_obtained` 静态 0 前置、关键词齐全，lint 判它可满足；但真机 arbiter 给它注入了 witness+disclosure 前置，把它变成死锁的一环。建议：指南补"避免让多条线在语义上互为前提（账房要证词、证词要账房）"，或引擎侧对 arbiter 注入的前置做**环检测**。
2. **指南没讲"作者意图的无前置取证"在真机会被 arbiter 自由加码**——作者 label 写"无前置"不等于运行期无前置。建议给关键取证 var 一个"作者锁定前置、禁止 arbiter 追加"的声明位（lint 可校验）。
3. **跨 NPC leverage 不传递**没在杠杆指南里说明——作者以为"别处取证就能压当事人"，实际只有当事人自管 var 上的事实算筹码。
4. 多跳移动/在场 coherence 的交互没在 driver/指南里提示。

**是否改 pack：未动。总拍数：主线 19 + 反作弊 2 + 收敛重试 5 = 26 拍（3 个会话）。**

整体判断：引擎在大包上**稳**（0 FALLBACK、0 崩溃、反作弊红线守得很死、A 段杠杆基线/充分性拒绝都正确），但**闭不了环**——瓶颈是 arbiter 在多 var 交织时**自发注入并递归追加前置形成死锁**，这是当前"能对外讲跑得了真内容"的最大拦路石。
