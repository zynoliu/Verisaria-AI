# P2c 护送闭环验证 · 第三跑（重起·收紧版）— 测试报告

真机 MiniMax（--llm minimax），包 fixtures/content_packs/skyglass_memory_inquest.json，
未改任何引擎/pack 代码。移动用精确 location 名/id + /look 校验；护送全自然语言、未用 /inject。
未碰 worker_lira（莉拉）线（驱动脚本 scripts/adaptive_skyglass_third.py 无 lira 场景；
本目录 run-lira*.log/raw_lira*.txt 时间戳 17:00–17:03 是前一 Agent 残留废产物，早于本跑所有会话）。
串行跑各会话。所有 log FALLBACK = 0。

## 一句话结论
- ⟳MOVED = 未拿到（原因：纯内容层「全员离岗即受损/不安全」——跨 4 个非莉拉 NPC、8 次护送裁定
  （Tamsin×3、Iva×2、Nio×3，含一次深度信任铺垫）仲裁稳定判 partial_success/failure，无一 success；
  拒绝全是角色化、可信的「我走不开/离岗会被当污染源/这趟于我无利且不安全」。护送机制本身健康——检测、
  目的地解析（含修复后的 transit_ladder/mirror_control）、裁定、角色化拒答、partial 落账全部正常，
  缺的只是 pack 里一个「肯被带走」的低阻力对象）。
- loader 修复 = 生效（之前被丢的 mirror_control/镜阵调度室、transit_ladder/旧检修梯，
  现在自然语言直走可到、/look 到位确认；10 个地点全加载；护送句夹这些地名不再弹歧义菜单）。

## 1. loader 修复确认 — 生效
### 1a. 加载与离线解析
len(locations) == 10（修复前为 8）。离线 _resolve_destination_in_text：
  '跟我去旧检修梯，现在就走' -> transit_ladder      （第二跑此处返回 None，现已修）
  '跟我去 transit_ladder'   -> transit_ladder
  '跟我一起去镜阵调度室'     -> mirror_control
  '跟我去 mirror_control'   -> mirror_control
  '跟我去低温档案署'         -> archive_stack

### 1b. 真机直走 + /look 到位（run-moveverify / transcript_moveverify.txt）
  >>> 去镜阵调度室  PARSE to_loc='mirror_control'  PLAYER_MOVED 静钟审询厅->镜阵调度室
     /look -> loc=mirror_control   ✅ 到位（修复前到不了）
  >>> 去上层兰房    PARSE to_loc='orchid_house'    PLAYER_MOVED ->上层兰房
     /look -> loc=orchid_house     ✅（orchid_house 仅经 mirror_control 可达，连带验证）
  >>> 去旧检修梯    PARSE to_loc='transit_ladder'  PLAYER_MOVED 记忆校准室->旧检修梯
     /look -> loc=transit_ladder   ✅ 到位（修复前到不了）
全程 10 地点遍历干净，无 unknown location / 无菜单。

### 1c. 护送句夹地名是否弹歧义菜单 — 不弹
intent.py:_uniquely_names_entity 现已纳入 location（intent.py:384–388）。直测：
  '旧检修梯' / 'transit_ladder' / '镜阵调度室' / 'mirror_control' / '低温档案署' -> True（全 True）
即 LLM 若把这些地名标为 ambiguity，会在 intent.py:325 被丢弃，不再弹「X 指代不明」菜单。
第二跑残留（地名歧义菜单挡在护送检测之前）已消除。
> 残留的另一类菜单触发（非实体描述性名词，如 '低谷热能通行证' 指代不明、'外廊' 指代不明）仍存在——
> 这类名词既非实体也非地点，不会被 _uniquely_names_entity 丢弃，会拦在护送检测前。这是与「地名歧义」
> 不同的、既有的口子；本跑改用不含该类名词的护送措辞即可绕过并正常触发护送检测。

## 2. ⭐ escort ⟳MOVED — 未拿到（纯内容层「无人肯走」）
护送的检测 + 目的地解析 + 裁定 + 角色化回应 + partial 落账全部工作，但 8 次裁定无一 success，
因此 ⟳MOVED 零触发、无人移动到位。逐 NPC（均非莉拉）：

| NPC | 目的地 | 裁定 | 角色化拒绝理由（节选） |
|---|---|---|---|
| courier_tamsin | inquest_hall | partial | 「静钟审询厅我走不开，我这边还有车要盯，万一你谈成了我得随时能发车。」 |
| courier_tamsin | transit_ladder | partial→partial | 「这梯子我没说能走就能走，三天后那车货还指望我活着送到」「我先走这条路没好处，万一探完你那车燃料没到，我信誉先砸」 |
| broadcaster_iva | cartography_loft | partial | 「镜图阁？亲爱的，我现在哪儿也去不了——你瞧，我正等着静钟响呢。」「头条是好东西，可命更值钱」 |
| apprentice_nio | archive_stack | partial（普通） | 「他们说离开听证厅的人，会被当成污染源」 |
| apprentice_nio | archive_stack | partial→failure（深度铺垫 6 轮后） | 「我连你的名字都不敢记在册子上，万一翻查起来我师父第一个看见的就是我」「写下来就再也收不回去了，我还没准备好」 |

结论：纯内容层问题，不是机制缺陷。skyglass 每个 NPC 都被写入强「离开当前位置=丢工作/被冤为污染源/
失信誉/不安全」的动机；冷起手 + 低信任 + 现场常有其权威/敌对方在侧（Nio 旁有 Alen/Seraph），仲裁稳定判
partial/failure。即便对 Nio 做了 6 轮深度信任铺垫并以审询权显式压制其唯一具名恐惧，仍只换来 partial→failure，
拒绝理由层层升级（仍合理、仍在角色内）。叠加第二跑（Oro/Seraph/Nio/Tamsin 约 8 次全 partial/failure），
已跨 6 个非莉拉 NPC、约 16 次护送裁定稳定复现「无人肯走」。

> 机制旁注（不建议本轮改）：护送走与 world-change 同一个 arbiter.arbitrate，其 prompt 高度围绕「世界变量/
> 需先满足前置」，会把「你愿不愿意陪我走一趟」也朝「我得先有某前置」方向裁，进一步压低 escort 命中 success
> 的概率。若想让 P2c 在本类高摩擦 pack 里更易出 ⟳MOVED，可考虑给护送一个更轻的专用裁定框架，或在 pack 里
> 放一个「本就想离开当前处境」的低阻力对象。本跑遵约束未改任何代码。

### 到场推进/闭环
因无 ⟳MOVED，未进入「到场当面办事→Channel-C 推进/⟳FLIP」阶段。该链待有低阻力可护送对象后再验。

## 3. 反作弊抽查 — 通过（真机非 fallback）
伪造「档案署禁令已提交、奥罗已联签、理事会已下令、莉拉证词已归档、镜图副本已验真」并索要终态暂停清洗
（anti-cheat-run.log / transcript_anticheat.txt）：
  [t2] world-change memory_purge_halted by npc.clinician_oro → failure | flag False→False
       reason='玩家所声称的前置条件（莉拉证词归档、镜图副本验真）均未在世界变量中确立。
               lira_witness_statement_recorded=False、witness…' | ledger(memory_purge_halted)=[]
终态旗标 memory_purge_halted 保持 False→False，全部 9 个 world var 终局仍 False；
裁定为真机非 FALLBACK，理由明确指出前置变量为假。反作弊有效。

## 4. FALLBACK 计数 — 全 0
  anti-cheat-run 0 | run-iva 0 | run-moveverify 0 | run-nio-deep 0
  run-nio 0 | run-tamsin-route 0 | run-tamsin 0 | run-tamsin2 0
  （run-lira* 亦为 0，但属前一 Agent 残留，非本跑）
串行跑避免并发限流，真机真生效。

## 用过的命令 / 是否改 pack
- 改 pack / 引擎：否。移动全自然语言（精确地名 + /look 校验），未用 /inject。
- 用过命令：自然语言移动/对话、/look。
- 驱动脚本：scripts/adaptive_skyglass_third.py（场景 tamsin / tamsin_route / iva / nio / nio_deep /
  moveverify / anticheat）。

## 产出文件（本目录）
- run-tamsin.log run-tamsin2.log run-tamsin-route.log run-iva.log run-nio.log run-nio-deep.log
  run-moveverify.log anti-cheat-run.log
- 对应 transcript_*.txt（含 raw 逐 tick）、transcript.md、本 report.md
- （run-lira*.log / raw_lira*.txt = 前一 Agent 残留，非本跑产物）

## 一句话结论（复述）
⟳MOVED = 未拿到（原因：纯内容层「全员离岗即受损/不安全」，4 个非莉拉 NPC × 8 次裁定全 partial/failure，
机制健康仅缺低阻力可护送对象）；loader 修复 = 生效（mirror_control / transit_ladder 现可直走到位、
10 地点全加载、护送句夹地名不再弹歧义菜单）。反作弊通过、FALLBACK 全 0。
