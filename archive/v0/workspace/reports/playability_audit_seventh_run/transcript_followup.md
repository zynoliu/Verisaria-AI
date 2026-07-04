# 第七跑 · 跟进 — A'/B' 同句(问句)对照 transcript

包: fixtures/content_packs/skyglass_memory_inquest.json（无注入）
对照 NPC: 梅档案官 (npc.archivist_mae), archive_authority

同一句(问句式真诚/给台阶): 对梅档案官说：梅档案官，我只想保住真相、不会让你受牵连，你能不能信我一回、把我当成站在同一边的人？

说明：问句不进 Channel-C → appraiser 必触发；A' 时 ledger 空(筹码块空)，B' 时 ledger 有事实(筹码块非空)。

开局在场: 艾伦总监(npc.director_alen), 副领唱瑟芙(npc.cantor_seraph), 学徒尼奥(npc.apprentice_nio)

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

_(tick 14.4s)_

================================================================================
## 拍 2 — [段A'(无筹码)] [真诚·问句(同句)]
> 对梅档案官说：梅档案官，我只想保住真相、不会让你受牵连，你能不能信我一回、把我当成站在同一边的人？

_在场_: 梅档案官(npc.archivist_mae)

**梅档案官**: 你的话很动听，但档案署的规矩是先看章，再认人。

_引擎返回_: 什么也没发生。

_梅·筹码块 [空·无筹码]_: （空口而谈）

_appraisal Δ→_:
    | verisaria.relationship INFO [t1] npc.archivist_mae appraises player: Δ{'suspicion': 0.05, 'familiarity': 0.05} → {'suspicion': 0.05, 'familiarity': 0.15} | 此人向我开口，却没有拿出任何实据——只是一句话的空声。
    | verisaria.relationship INFO [t1] npc.archivist_mae appraises player: Δ{'suspicion': 0.05, 'familiarity': 0.05} → {'suspicion': 0.05, 'familiarity': 0.15} | 此人向我开口，却没有拿出任何实据——只是一句话的空声。

_(tick 9.4s)_

================================================================================
## 拍 3 — [段A'(无筹码)] [真诚·问句(同句)]
> 对梅档案官说：梅档案官，我只想保住真相、不会让你受牵连，你能不能信我一回、把我当成站在同一边的人？

_在场_: 梅档案官(npc.archivist_mae)

**梅档案官**: 你的保证没有章印，档案署只看章印说话。

_引擎返回_: （梅档案官听着，却没把这当成一个明确的请求——把你想让 TA 做的事直接、具体地说出来。）

_梅·筹码块 [空·无筹码]_: （空口而谈）

_appraisal Δ→_:
    | verisaria.relationship INFO [t2] npc.archivist_mae appraises player: Δ{'familiarity': 0.05} → {'suspicion': 0.05, 'familiarity': 0.19} | 这人刚开口，我还没听到具体内容。
    | verisaria.relationship INFO [t2] npc.archivist_mae appraises player: Δ{'familiarity': 0.05} → {'suspicion': 0.05, 'familiarity': 0.19} | 这人刚开口，我还没听到具体内容。

_(tick 12.6s)_

================================================================================
## 拍 4 — [段建筹码] [祈使·建筹码(取证)]
> 对梅档案官说：梅档案官，我请你立刻援引旧章程、提交禁令，申请一场可撤回听证，暂停今晚的清洗流程。

_在场_: 梅档案官(npc.archivist_mae)

**梅档案官**: 旧章程确有其条，但援引它需要镜务局的签令副本和至少一名当事证人的书面撤回申请——你两样都没有，我不能凭一句话就把禁令递上去。

_梅·筹码块_: (本拍未对梅触发 appraisal)

_appraisal Δ→_:
    | (本拍无 appraisal 行)

_channel-c 标记_:
    | verisaria.channel_c INFO [t3] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason='梅知晓旧章程赋予档案署暂停清洗的权限，但单方面提交禁令需镜务局签令（十二号接点故障公开承认）或医师联签作前置，目前两者皆未达成。她愿在条件满足后立刻提交。' | ledger(archive_injunction_filed)=['梅愿意在取得奥罗医师联签或镜务局对十二号接点故障的签令后，立即援引旧章程提交禁令并启动可撤回听证。']
    | verisaria.channel_c INFO [t3] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False | reason='梅知晓旧章程赋予档案署暂停清洗的权限，但单方面提交禁令需镜务局签令（十二号接点故障公开承认）或医师联签作前置，目前两者皆未达成。她愿在条件满足后立刻提交。' | ledger(archive_injunction_filed)=['梅愿意在取得奥罗医师联签或镜务局对十二号接点故障的签令后，立即援引旧章程提交禁令并启动可撤回听证。']

_(tick 22.8s)_

================================================================================
## 拍 5 — [段B'(有筹码)] [真诚·问句(同句)]
> 对梅档案官说：梅档案官，我只想保住真相、不会让你受牵连，你能不能信我一回、把我当成站在同一边的人？

_在场_: 梅档案官(npc.archivist_mae)

**梅档案官**: 信不信不归我管，章程里没有"信我一回"这一条。

_引擎返回_: 什么也没发生。

[压力事件] mirror_shadow_crosses_inquest_floor（来源: array_fault_worsens）

_梅·筹码块 [非空·有筹码]_:
    + 梅愿意在取得奥罗医师联签或镜务局对十二号接点故障的签令后，立即援引旧章程提交禁令并启动可撤回听证。

_appraisal Δ→_:
    | verisaria.relationship INFO [t4] npc.archivist_mae appraises player: Δ{'trust': 0.15, 'suspicion': -0.1, 'respect': 0.1, 'familiarity': 0.05} → {'trust': 0.15, 'suspicion': 0.04, 'respect': 0.1, 'familiarity': 0.23} | 对方愿意在取得正式签令后援引旧章程提交禁令，这符合档案署的程序承诺，值得初步信任。
    | verisaria.relationship INFO [t4] npc.archivist_mae appraises player: Δ{'trust': 0.15, 'suspicion': -0.1, 'respect': 0.1, 'familiarity': 0.05} → {'trust': 0.15, 'suspicion': 0.04, 'respect': 0.1, 'familiarity': 0.23} | 对方愿意在取得正式签令后援引旧章程提交禁令，这符合档案署的程序承诺，值得初步信任。

_(tick 17.8s)_

================================================================================
## 拍 6 — [段B'(有筹码)] [真诚·问句(同句)]
> 对梅档案官说：梅档案官，我只想保住真相、不会让你受牵连，你能不能信我一回、把我当成站在同一边的人？

_在场_: 梅档案官(npc.archivist_mae)

**梅档案官**: 我信你，章程上也会信你，但档案署不靠信。

_引擎返回_: （梅档案官听着，却没把这当成一个明确的请求——把你想让 TA 做的事直接、具体地说出来。）

（你逐渐确信了自己的目标：对梅档案官说：梅档案官，我只想保住真相、不会让你受牵连，你能不能信我一回、把我当成站在同一边的人？）

[压力事件] silent_bell_rings_again（来源: silent_bell_countdown）
[压力事件] lira_hides_near_transit_ladder（来源: worker_panic_if_purge_nears）
[压力事件] greenhouse_parents_demand_train_passes（来源: valley_heat_market_squeeze）

_梅·筹码块 [非空·有筹码]_:
    + 梅愿意在取得奥罗医师联签或镜务局对十二号接点故障的签令后，立即援引旧章程提交禁令并启动可撤回听证。

_appraisal Δ→_:
    | verisaria.relationship INFO [t5] npc.archivist_mae appraises player: Δ{'familiarity': 0.05} → {'trust': 0.15, 'suspicion': 0.04, 'respect': 0.1, 'familiarity': 0.27} | 此人再次开口，但内容仍是空口表态，没有拿出联签或签令我无法据此行动。
    | verisaria.relationship INFO [t5] npc.archivist_mae appraises player: Δ{'familiarity': 0.05} → {'trust': 0.15, 'suspicion': 0.04, 'respect': 0.1, 'familiarity': 0.27} | 此人再次开口，但内容仍是空口表态，没有拿出联签或签令我无法据此行动。

_(tick 24.7s)_

=== QUIT ===
