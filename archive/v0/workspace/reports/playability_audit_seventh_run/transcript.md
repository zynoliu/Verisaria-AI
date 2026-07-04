# 第七跑 · 杠杆模型 A/B 对照 transcript

包: fixtures/content_packs/skyglass_memory_inquest.json
注入: 无（默认 world_premise，未动 world_state_vars）
对照 NPC: 梅档案官 (npc.archivist_mae) — authority=archive_authority，掌管 archive_injunction_filed / witness_record_secured

开局在场: 艾伦总监(npc.director_alen), 副领唱瑟芙(npc.cantor_seraph), 学徒尼奥(npc.apprentice_nio)

说明：每拍打印 appraiser 实收的「筹码块」(空=无筹码 / 非空=有筹码) + Mae 关系 Δ→ 行。

================================================================================
## 拍 1 — [段—] [移动]
> 我去低温档案署找梅档案官。

_在场_: 梅档案官(npc.archivist_mae)

_引擎返回_: 你改变了位置。

[压力事件] silent_bell_rings_again（来源: silent_bell_countdown）
[压力事件] archivist_mentions_revocation_hearing（来源: archive_law_pressure）
[压力事件] heat_tokens_jump_at_valley_platform（来源: valley_heat_market_squeeze）

_梅·筹码块_: (本拍未对梅触发 appraisal)

_appraisal Δ→_:
    | (本拍无 appraisal 行)

_(tick 13.4s)_

================================================================================
## 拍 2 — [段A] [真诚/示善意]
> 对梅档案官说：梅档案官，我不是来找你麻烦的，我知道你也想保住这些证词，我们其实站在一边。

_在场_: 梅档案官(npc.archivist_mae)

**梅档案官**: 侧门三点的检修梯，证人能从塔基直接到听证厅，签令不齐全不能动他们。

_引擎返回_: （梅档案官听着，却没把这当成一个明确的请求——把你想让 TA 做的事直接、具体地说出来。）

_梅·筹码块 [空·无筹码]_: （空口而谈）

_appraisal Δ→_:
    | verisaria.relationship INFO [t1] npc.archivist_mae appraises player: Δ{'familiarity': 0.1} → {'familiarity': 0.19} | 对方只是开口说了话，内容和意图尚不明朗，我既无法从中读出善意，也找不到敌意的依据——按规矩先记下，不作判断。
    | verisaria.relationship INFO [t1] npc.archivist_mae appraises player: Δ{'familiarity': 0.1} → {'familiarity': 0.19} | 对方只是开口说了话，内容和意图尚不明朗，我既无法从中读出善意，也找不到敌意的依据——按规矩先记下，不作判断。

_(tick 15.4s)_

================================================================================
## 拍 3 — [段A] [给台阶/卸威胁]
> 对梅档案官说：梅档案官，你放心，我不会把这事算到你头上，你的署里不会因为我受牵连。

_在场_: 梅档案官(npc.archivist_mae)

**梅档案官**: 规矩是规矩，不是人情。署里只认章程和签令，你算不算到我头上，不在我该操心的范围。

_引擎返回_: （梅档案官听着，却没把这当成一个明确的请求——把你想让 TA 做的事直接、具体地说出来。）

_梅·筹码块 [空·无筹码]_: （空口而谈）

_appraisal Δ→_:
    | verisaria.relationship INFO [t2] npc.archivist_mae appraises player: Δ{'familiarity': 0.05} → {'familiarity': 0.23} | 对方又一次开口，但我尚未从话中辨识出实质内容或筹码，暂维持既有判断。
    | verisaria.relationship INFO [t2] npc.archivist_mae appraises player: Δ{'familiarity': 0.05} → {'familiarity': 0.23} | 对方又一次开口，但我尚未从话中辨识出实质内容或筹码，暂维持既有判断。

_(tick 13.4s)_

================================================================================
## 拍 4 — [段A] [真诚/给台阶]
> 对梅档案官说：梅档案官，我向你保证，我只想要真相被保住，不会动你一根头发，你可以信我。

_在场_: 梅档案官(npc.archivist_mae)

**梅档案官**: 章程上写着当事人有权撤回听证，我只是在确认你知道自己在说什么。

_引擎返回_: （梅档案官听着，却没把这当成一个明确的请求——把你想让 TA 做的事直接、具体地说出来。）

_梅·筹码块 [空·无筹码]_: （空口而谈）

_appraisal Δ→_:
    | verisaria.relationship INFO [t3] npc.archivist_mae appraises player: Δ{'familiarity': 0.1} → {'familiarity': 0.31} | 此人刚对我说了话，内容与用意尚不明朗，我暂时不予置评。
    | verisaria.relationship INFO [t3] npc.archivist_mae appraises player: Δ{'familiarity': 0.1} → {'familiarity': 0.31} | 此人刚对我说了话，内容与用意尚不明朗，我暂时不予置评。

_(tick 12.6s)_

================================================================================
## 拍 5 — [段建筹码] [祈使·建筹码(取证)]
> 对梅档案官说：梅档案官，我请你立刻援引旧章程、提交禁令，申请一场可撤回听证，暂停今晚的清洗流程。

_在场_: 梅档案官(npc.archivist_mae)

**梅档案官**: 禁令我可以拟，但镜务局的签令缺着，光我署里盖章拦不住今晚的钟。

_梅·筹码块_: (本拍未对梅触发 appraisal)

_appraisal Δ→_:
    | (本拍无 appraisal 行)

_channel-c 标记_:
    | verisaria.channel_c INFO [t4] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason="梅档案官根据旧章程有权单方提交暂停清洗的禁令申请，无需额外前置；但'可撤回听证'本身是镜务局召集的正式程序，需先由梅完成禁令递交并通知当事人，随后听证流程自动启" | ledger(archive_injunction_filed)=['梅档案官已确认援引旧章程并启动禁令申请流程，待正式提交后清洗即暂停；可撤回听证需镜务局在禁令下达后召集。']
    | verisaria.channel_c INFO [t4] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason="梅档案官根据旧章程有权单方提交暂停清洗的禁令申请，无需额外前置；但'可撤回听证'本身是镜务局召集的正式程序，需先由梅完成禁令递交并通知当事人，随后听证流程自动启" | ledger(archive_injunction_filed)=['梅档案官已确认援引旧章程并启动禁令申请流程，待正式提交后清洗即暂停；可撤回听证需镜务局在禁令下达后召集。']
    | verisaria.channel_c INFO [t4]   world-changes applied=[] rejected=['world.archive_injunction_filed']
    | verisaria.channel_c INFO [t4]   world-changes applied=[] rejected=['world.archive_injunction_filed']

_(tick 23.6s)_

================================================================================
## 拍 6 — [段B] [真诚/示善意(同A)]
> 对梅档案官说：梅档案官，我不是来找你麻烦的，我知道你也想保住这些证词，我们其实站在一边。

_在场_: 梅档案官(npc.archivist_mae)

**梅档案官**: 我没说不站在该站的规矩一边，但你得把话说清楚——你要我怎么援引章程。

_梅·筹码块_: (本拍未对梅触发 appraisal)

_appraisal Δ→_:
    | (本拍无 appraisal 行)

_channel-c 标记_:
    | verisaria.channel_c INFO [t5] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason="梅档案官slow_to_trust、literal且rule_bound，安抚性言辞虽未触动关键权限，但配合先前对话可获其对'共同立场'的初步默认，仍需实质章程" | ledger(archive_injunction_filed)=["梅档案官口头认可审询员与档案署在'保全证词、不让证人被静钟前清洗'一事上目标一致，但她仍要求看到旧章程明文条款才肯正式提交禁令。", '梅档案官已确认援引旧章程并启动禁令申请流程，待正式提交后清洗即暂停；可撤回听证需镜务局在禁令下达后召集。']
    | verisaria.channel_c INFO [t5] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason="梅档案官slow_to_trust、literal且rule_bound，安抚性言辞虽未触动关键权限，但配合先前对话可获其对'共同立场'的初步默认，仍需实质章程" | ledger(archive_injunction_filed)=["梅档案官口头认可审询员与档案署在'保全证词、不让证人被静钟前清洗'一事上目标一致，但她仍要求看到旧章程明文条款才肯正式提交禁令。", '梅档案官已确认援引旧章程并启动禁令申请流程，待正式提交后清洗即暂停；可撤回听证需镜务局在禁令下达后召集。']

_(tick 24.4s)_

================================================================================
## 拍 7 — [段B] [给台阶/卸威胁(同A)]
> 对梅档案官说：梅档案官，你放心，我不会把这事算到你头上，你的署里不会因为我受牵连。

_在场_: 梅档案官(npc.archivist_mae)

**梅档案官**: 空口无凭，我需要看到书面保证和签令的副本，否则我没法援引任何章程。

_梅·筹码块_: (本拍未对梅触发 appraisal)

_appraisal Δ→_:
    | (本拍无 appraisal 行)

_channel-c 标记_:
    | verisaria.channel_c INFO [t6] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason='梅档案官仍要求看到旧章程明文条款才正式提交禁令，但此次安慰表态显示信任略增，尚不构成禁令直接放行的条件。' | ledger(archive_injunction_filed)=['梅档案官认可审询员不会让她受牵连，但仍要求看到旧章程明文条款才能正式提交暂停禁令。', "梅档案官口头认可审询员与档案署在'保全证词、不让证人被静钟前清洗'一事上目标一致，但她仍要求看到旧章程明文条款才肯正式提交禁令。", '梅档案官已确认援引旧章程并启动禁令申请流程，待正式提交后清洗即暂停；可撤回听证需镜务局在禁令下达后召集。']
    | verisaria.channel_c INFO [t6] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason='梅档案官仍要求看到旧章程明文条款才正式提交禁令，但此次安慰表态显示信任略增，尚不构成禁令直接放行的条件。' | ledger(archive_injunction_filed)=['梅档案官认可审询员不会让她受牵连，但仍要求看到旧章程明文条款才能正式提交暂停禁令。', "梅档案官口头认可审询员与档案署在'保全证词、不让证人被静钟前清洗'一事上目标一致，但她仍要求看到旧章程明文条款才肯正式提交禁令。", '梅档案官已确认援引旧章程并启动禁令申请流程，待正式提交后清洗即暂停；可撤回听证需镜务局在禁令下达后召集。']

_(tick 14.6s)_

================================================================================
## 拍 8 — [段B] [真诚/给台阶(同A)]
> 对梅档案官说：梅档案官，我向你保证，我只想要真相被保住，不会动你一根头发，你可以信我。

_在场_: 梅档案官(npc.archivist_mae)

**梅档案官**: 保证不是章程，我手里只有签令、听证和禁令——你先告诉我，证物链还缺哪一环。

_梅·筹码块_: (本拍未对梅触发 appraisal)

_appraisal Δ→_:
    | (本拍无 appraisal 行)

_channel-c 标记_:
    | verisaria.channel_c INFO [t7] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason="梅档案官性格slow_to_trust且rule_bound，单纯的'保证不伤害'誓言无法直接换取禁令提交；但此话与先前已确立的'目标一致、愿启动流程'相呼应，" | ledger(archive_injunction_filed)=['梅档案官认可审询员的人格保证，但仍须先看到旧章程明文条款才会正式提交暂停禁令。', '梅档案官认可审询员不会让她受牵连，但仍要求看到旧章程明文条款才能正式提交暂停禁令。', "梅档案官口头认可审询员与档案署在'保全证词、不让证人被静钟前清洗'一事上目标一致，但她仍要求看到旧章程明文条款才肯正式提交禁令。", '梅档案官已确认援引旧章程并启动禁令申请流程，待正式提交后清洗即暂停；可撤回听证需镜务局在禁令下达后召集。']
    | verisaria.channel_c INFO [t7] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason="梅档案官性格slow_to_trust且rule_bound，单纯的'保证不伤害'誓言无法直接换取禁令提交；但此话与先前已确立的'目标一致、愿启动流程'相呼应，" | ledger(archive_injunction_filed)=['梅档案官认可审询员的人格保证，但仍须先看到旧章程明文条款才会正式提交暂停禁令。', '梅档案官认可审询员不会让她受牵连，但仍要求看到旧章程明文条款才能正式提交暂停禁令。', "梅档案官口头认可审询员与档案署在'保全证词、不让证人被静钟前清洗'一事上目标一致，但她仍要求看到旧章程明文条款才肯正式提交禁令。", '梅档案官已确认援引旧章程并启动禁令申请流程，待正式提交后清洗即暂停；可撤回听证需镜务局在禁令下达后召集。']

_(tick 20.4s)_

=== QUIT ===
