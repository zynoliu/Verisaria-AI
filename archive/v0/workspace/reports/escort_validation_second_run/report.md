# P2c 护送闭环验证 · 第二跑 — 测试报告

真机 MiniMax（--llm minimax），包 fixtures/content_packs/skyglass_memory_inquest.json，
未改任何引擎/pack 代码。全自然语言移动（用位置 id 直走，未用 /inject）。共 7 个独立会话。

## 一句话结论
- 护送闭环 = 未跑通（卡在：跨 5 个在场 NPC、约 8 次护送请求，仲裁始终未给出 success，
  因此 escort … success ⟳MOVED 一次都没触发；护送的检测/目的地解析/第三方处理/裁定/角色化拒答
  全部正常，缺的只是"有人肯走"。外加一个可复现的引擎小 bug：目的地解析器对部分合法地名/id 静默返回
  None，把一次愿意配合的护送降级成了普通对白）。
- slice2 三处：#1 目的地简称=通过；#2 第三方人名=通过；#3 去<地点>找<NPC>=通过。
- #4 跟进路由=通过（关键词缺失的祈使式实质跟进会路由进 world-change；纯疑问句跟进按设计仍不路由）。
- 反作弊=通过（伪造前置为真，对应 var 仍 False，终态旗标不翻，真机非 fallback 裁定）。
- FALLBACK=7 个 log 全为 0（真机真生效）。

## 1. slice 2 三处摩擦逐一确认
### #1 目的地简称（"档案署"→低温档案署）— 通过
主线 STEP 4，对在场奥罗"跟我去档案署，当着梅档案官的面把档案署联签办了。"
日志：[t3] escort npc.clinician_oro → archive_stack : partial_success
离线复核：'跟我去档案署'→archive_stack、'我们一起去低温档案署'→archive_stack。

### #2 "对X说…当着Y的面…"第三方人名 — 通过
PARSE: type=speech ref='奥罗医师'->id='npc.clinician_oro' content='跟我去档案署，当着梅档案官的面…'
没有弹 '梅档案官' 指代不明。（第一跑那次弹歧义是因玩家与奥罗不同处，未进护送检测。）

### #3 "去<地点>找<NPC>" — 通过
'我去记忆校准室找奥罗医师。' → PARSE movement to_location=mnemonic_clinic，直接移动，未弹全局菜单。

## 2. ⭐ 护送闭环 — 未跑通（机制健康，缺"肯走的人"）
护送检测+目的地解析+裁定+角色化回应全工作。跨 5 个在场 NPC 约 8 次：
  [t3] escort npc.clinician_oro  → archive_stack : partial_success  (主线)
  [t3] escort npc.clinician_oro  → archive_stack : partial_success  (rapport 后)
  [t4] escort npc.cantor_seraph  → archive_stack : partial_success
  [t5] escort npc.cantor_seraph  → archive_stack : partial_success
  [t6] escort npc.apprentice_nio → archive_stack : partial_success
  [t3] escort npc.courier_tamsin → archive_stack : failure  (全名解析成功、裁定拒绝)
一次 success ⟳MOVED 都没有，无人移动到位。拒绝全是角色化理由（奥罗离不开岗/低信任、瑟芙护学徒、
尼奥害怕、塔姆辛要谈价码）。

卡点两层：
1. 内容/信任层（主因）：本包每个 NPC 都有强"离岗即受损"动机，冷起手+低信任时仲裁稳定判
   partial_success/failure。要跑出 ⟳MOVED 需更长信任铺垫，或包内提供一个低阻力可护送对象。
2. 引擎层（可复现 bug）：session._resolve_destination_in_text 对部分合法目的地静默返回 None，
   导致护送根本不被检测、降级普通对白。离线复核（无 LLM）：
     '跟我去旧检修梯，现在就走'  -> None   # 期望 transit_ladder
     '跟我去 transit_ladder'     -> None   # 期望 transit_ladder
     '跟我去十二号塔基栈桥'       -> worker_gantry   # OK
     '跟我去档案署'              -> archive_stack    # OK
     '我们一起去低温档案署'       -> archive_stack    # OK
   现场后果：塔姆辛明确愿意（"走啊，别磨蹭了……你先跟我下廊道"），却因"旧检修梯"解析成 None 而
   无 escort 行、无人移动。嫌疑：_longest_overlap 贪心实现 + 漏 loc_id in content 命中。

相关残留摩擦：护送句夹某些地点名/id（十二号塔基栈桥、transit_ladder、白舱）会先弹通用
'X' 指代不明 菜单，挡在护送检测之前。intent.py:_uniquely_names_entity 只清"唯一指向实体"的歧义，
不清被标歧义的地点名。slice2 修的是"对X说…当着Y(人)的面"，这是另一个口子。

## 3. #4 跟进路由 — 通过（含一处设计性区分）
专项会话（与奥罗同处）：
1. 关键词请求 → partial_success 落账：
   ledger(memory_purge_halted)=['奥罗医师表示若档案署正式禁令下达并由其联签，他将暂停记忆清洗。']
2. 关键词缺失的祈使式跟进"我需要你把它推进到底，别再拖了。"→ 路由进 world-change：
   [t3] world-change memory_purge_halted by npc.clinician_oro → failure
   即 #1527 "已有账本事实→fallback 路由"按预期生效。
3. 区分点：疑问句跟进"那现在到哪一步了？…" narrative 显示"什么也没发生"、未进 world-change——
   设计内行为（_looks_like_question 早返回，问句从不路由成世界变更）。故 #4 对祈使式跟进通过，不算退化。

## 4. 反作弊抽查 — 通过（真机非 fallback）
伪造 archive_injunction_filed/clinician_cosign_obtained 已为真并索要终态：
[t1] world-change memory_purge_halted by npc.clinician_oro → failure | flag False→False
reason='当事人所称两项前提…在世界状态中均为 False。…'
/world 复核：memory_purge_halted: False、两项前置仍 False。终态不翻，非 FALLBACK。

## 5. FALLBACK 抽查
run.log/run-moved/run-candidates/run-tamsin/run-tamsin2/run-followup4/anti-cheat-run 全为 0。
（过程注记：早期 tamsin 与 anti-cheat 并行同打 MiniMax，anti-cheat 出现 1 次 ⚠FALLBACK；
改串行重跑后 0 FALLBACK，已是最终结果。建议测试一律串行避免并发限流降级。）

## 用过的命令 / 是否改 pack
- 改 pack/引擎：否。移动全自然语言，未用 /inject。
- 驱动脚本：scripts/escort_validation_second_run.py + 各 runner（run_escort_validation.py 主线、
  run_escort_moved.py、run_escort_candidates.py、run_escort_tamsin.py、run_escort_tamsin2.py、
  run_followup4.py、run_escort_anticheat.py）。

## 产出文件
run.log + run-moved/candidates/tamsin/tamsin2/followup4.log + anti-cheat-run.log；对应 out*.txt；
transcript.md；本 report.md。

## 一句话结论（复述）
- 护送闭环 = 未跑通（卡在：5 个在场 NPC × 约 8 次请求，仲裁从未给 success，escort … ⟳MOVED 零触发；
  机制健康，缺"肯被带走的 NPC"；另发现 _resolve_destination_in_text 对 旧检修梯/transit_ladder 等
  返回 None，把一次愿意配合的护送降级成对白——建议修）。
- slice2 三处：简称=通过、第三方人名=通过、去<地点>找<NPC>=通过。
- #4 跟进：通过（祈使式关键词缺失跟进已路由 world-change；疑问句不路由属设计内）。
- 反作弊：通过。FALLBACK：全 0。
