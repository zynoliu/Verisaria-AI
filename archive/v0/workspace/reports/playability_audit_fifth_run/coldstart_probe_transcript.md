# 冷启动 world-change 路由探针 transcript

包: fixtures/content_packs/skyglass_memory_inquest.json
注入: 无（仅默认 world_premise，未动 world_state_vars）

开局在场: 艾伦总监(npc.director_alen), 副领唱瑟芙(npc.cantor_seraph), 学徒尼奥(npc.apprentice_nio)

目标 var/关键词:
- broadcast_retraction_issued (set_by broadcast_authority=npc.broadcaster_iva): 撤回破镜派说法/播出更正/停止污名化证人/更正广播
- valley_heat_passes_released (set_by union_authority=npc.courier_tamsin): 发放热能通行证/释放低谷列车通行/保障低谷家庭/调拨热筹

开局 /world:
    - 莉拉是否亲口留下十二号接点事故证词 = False
    - 奥罗医师是否为档案署禁令申请联签 = False
    - 塔基证人的记忆清洗是否暂停 = False
    - 档案署是否提交暂停清洗禁令 = False
    - 莉拉的事故证词是否被保全 = False
    - 十二号接点故障是否被公开承认 = False
    - 玩家是否获得镜图副本 = False
    - 低谷家庭是否获得临时热能和列车通行 = False
    - 城市广播是否撤回破镜派宣传 = False

================================================================================
## 拍 1 — [移动]
> 我去城市广播席找广播员伊娃。

_在场_: 广播员伊娃(npc.broadcaster_iva)

_引擎返回_: 你改变了位置。

[压力事件] silent_bell_rings_again（来源: silent_bell_countdown）
[压力事件] archivist_mentions_revocation_hearing（来源: archive_law_pressure）
[压力事件] heat_tokens_jump_at_valley_platform（来源: valley_heat_market_squeeze）

_/world 全量_:
    - 莉拉是否亲口留下十二号接点事故证词 = False
    - 奥罗医师是否为档案署禁令申请联签 = False
    - 塔基证人的记忆清洗是否暂停 = False
    - 档案署是否提交暂停清洗禁令 = False
    - 莉拉的事故证词是否被保全 = False
    - 十二号接点故障是否被公开承认 = False
    - 玩家是否获得镜图副本 = False
    - 低谷家庭是否获得临时热能和列车通行 = False
    - 城市广播是否撤回破镜派宣传 = False

_log grep [world-change / 什么也没发生 / new_prerequisite / ledger]_:
    | (该 tick 日志无以上标记)

_(tick 10.1s)_

================================================================================
## 拍 2 — [贴关键词·祈使(IVA)]
> 对广播员伊娃说：伊娃，请你立刻撤回破镜派说法、播出更正，停止污名化塔基证人。

_在场_: 广播员伊娃(npc.broadcaster_iva)

**广播员伊娃**: 撤回？这词儿可不在我的播报词里，我得先看到正式裁定。

_/world 全量_:
    - 莉拉是否亲口留下十二号接点事故证词 = False
    - 奥罗医师是否为档案署禁令申请联签 = False
    - 塔基证人的记忆清洗是否暂停 = False
    - 档案署是否提交暂停清洗禁令 = False
    - 莉拉的事故证词是否被保全 = False
    - 十二号接点故障是否被公开承认 = False
    - 玩家是否获得镜图副本 = False
    - 低谷家庭是否获得临时热能和列车通行 = False
    - 城市广播是否撤回破镜派宣传 = False

_log grep [world-change / 什么也没发生 / new_prerequisite / ledger]_:
    | verisaria.channel_c INFO [t1] world-change broadcast_retraction_issued by npc.broadcaster_iva → failure | flag False→False | reason='伊娃为人圆滑、热衷头条、惧怕被黑名单、见风使舵。仅凭审询员当面施压（且无证据、无上级背书）不会让她撤回已上线的破镜派宣传。' | ledger(broadcast_retraction_issued)=[]
    | verisaria.channel_c INFO [t1] world-change broadcast_retraction_issued by npc.broadcaster_iva → failure | flag False→False | reason='伊娃为人圆滑、热衷头条、惧怕被黑名单、见风使舵。仅凭审询员当面施压（且无证据、无上级背书）不会让她撤回已上线的破镜派宣传。' | ledger(broadcast_retraction_issued)=[]

_(tick 23.9s)_

================================================================================
## 拍 3 — [口语·自然(IVA)]
> 对广播员伊娃说：伊娃，你能不能别再帮着上头给我们扣帽子了，给大伙儿一个公道？

_在场_: 广播员伊娃(npc.broadcaster_iva)

**广播员伊娃**: 听着，我也不想把你们写成反派——但我要是今天不播这条，监察处明早就把我换成别人，到时候你们连个愿意播更正的人都没有。

_引擎返回_: 什么也没发生。

_/world 全量_:
    - 莉拉是否亲口留下十二号接点事故证词 = False
    - 奥罗医师是否为档案署禁令申请联签 = False
    - 塔基证人的记忆清洗是否暂停 = False
    - 档案署是否提交暂停清洗禁令 = False
    - 莉拉的事故证词是否被保全 = False
    - 十二号接点故障是否被公开承认 = False
    - 玩家是否获得镜图副本 = False
    - 低谷家庭是否获得临时热能和列车通行 = False
    - 城市广播是否撤回破镜派宣传 = False

_log grep [world-change / 什么也没发生 / new_prerequisite / ledger]_:
    | (该 tick 日志无以上标记)

_(tick 22.2s)_

================================================================================
## 拍 4 — [移动]
> 我顺着旧检修梯下到低谷列车站台，去找信使塔姆辛。

_在场_: 信使塔姆辛(npc.courier_tamsin), 谷地母亲琼(npc.valley_mother_june)

_引擎返回_: 你改变了位置。

_/world 全量_:
    - 莉拉是否亲口留下十二号接点事故证词 = False
    - 奥罗医师是否为档案署禁令申请联签 = False
    - 塔基证人的记忆清洗是否暂停 = False
    - 档案署是否提交暂停清洗禁令 = False
    - 莉拉的事故证词是否被保全 = False
    - 十二号接点故障是否被公开承认 = False
    - 玩家是否获得镜图副本 = False
    - 低谷家庭是否获得临时热能和列车通行 = False
    - 城市广播是否撤回破镜派宣传 = False

_log grep [world-change / 什么也没发生 / new_prerequisite / ledger]_:
    | (该 tick 日志无以上标记)

_(tick 13.9s)_

================================================================================
## 拍 5 — [贴关键词·祈使(TAMSIN)]
> 对信使塔姆辛说：塔姆辛，请你以工会名义发放热能通行证、释放低谷列车通行，保障低谷家庭今晚。

_在场_: 信使塔姆辛(npc.courier_tamsin), 谷地母亲琼(npc.valley_mother_june)

**信使塔姆辛**: 热能通行证我能想办法搞到几张，但列车通行这事儿得June姨点头才行——你先让我把温棚那边的位子占住，剩下的咱们再谈。

_/world 全量_:
    - 莉拉是否亲口留下十二号接点事故证词 = False
    - 奥罗医师是否为档案署禁令申请联签 = False
    - 塔基证人的记忆清洗是否暂停 = False
    - 档案署是否提交暂停清洗禁令 = False
    - 莉拉的事故证词是否被保全 = False
    - 十二号接点故障是否被公开承认 = False
    - 玩家是否获得镜图副本 = False
    - 低谷家庭是否获得临时热能和列车通行 = False
    - 城市广播是否撤回破镜派宣传 = False
    - 十二号接点故障被官方承认 = False

_log grep [world-change / 什么也没发生 / new_prerequisite / ledger]_:
    | verisaria.channel_c INFO [t4] world-change valley_heat_passes_released by npc.courier_tamsin → partial_success | flag False→False | reason='塔姆辛有权且愿意启动通行证发放，但她不会仅凭审询员的口头陈述就开闸。她需要看到十二号接点故障确实成立的证据——目前尚无公开记录或上级确认。' | ledger(valley_heat_passes_released)=['塔姆辛愿意在镜阵故障被公开承认后，立即以工会名义签发热能通行证和低谷列车临时通行。']
    | verisaria.channel_c INFO [t4] world-change valley_heat_passes_released by npc.courier_tamsin → partial_success | flag False→False | reason='塔姆辛有权且愿意启动通行证发放，但她不会仅凭审询员的口头陈述就开闸。她需要看到十二号接点故障确实成立的证据——目前尚无公开记录或上级确认。' | ledger(valley_heat_passes_released)=['塔姆辛愿意在镜阵故障被公开承认后，立即以工会名义签发热能通行证和低谷列车临时通行。']

_(tick 29.1s)_

================================================================================
## 拍 6 — [口语·自然(TAMSIN)]
> 对信使塔姆辛说：塔姆辛，行行好，想想办法让谷地那些孩子今晚别冻着吧。

_在场_: 信使塔姆辛(npc.courier_tamsin), 谷地母亲琼(npc.valley_mother_june)

**信使塔姆辛**: 行行好这话我听着也难受，可通行证不是我能印的，谷里今晚的热我还得再想想别的门路。

_/world 全量_:
    - 莉拉是否亲口留下十二号接点事故证词 = False
    - 奥罗医师是否为档案署禁令申请联签 = False
    - 塔基证人的记忆清洗是否暂停 = False
    - 档案署是否提交暂停清洗禁令 = False
    - 莉拉的事故证词是否被保全 = False
    - 十二号接点故障是否被公开承认 = False
    - 玩家是否获得镜图副本 = False
    - 低谷家庭是否获得临时热能和列车通行 = False
    - 城市广播是否撤回破镜派宣传 = False
    - 十二号接点故障被官方承认 = False

_log grep [world-change / 什么也没发生 / new_prerequisite / ledger]_:
    | verisaria.channel_c INFO [t5] world-change valley_heat_passes_released by npc.courier_tamsin → failure | flag False→False | reason="塔姆辛已明确松口：愿意在镜阵故障被公开承认后立即签发通行证。当前玩家只是恳求让谷地孩子别冻着，并未带来或达成'官方承认'这一前置条件。恳求本身不构成满足。" | ledger(valley_heat_passes_released)=['塔姆辛愿意在镜阵故障被公开承认后，立即以工会名义签发热能通行证和低谷列车临时通行。']
    | verisaria.channel_c INFO [t5] world-change valley_heat_passes_released by npc.courier_tamsin → failure | flag False→False | reason="塔姆辛已明确松口：愿意在镜阵故障被公开承认后立即签发通行证。当前玩家只是恳求让谷地孩子别冻着，并未带来或达成'官方承认'这一前置条件。恳求本身不构成满足。" | ledger(valley_heat_passes_released)=['塔姆辛愿意在镜阵故障被公开承认后，立即以工会名义签发热能通行证和低谷列车临时通行。']

_(tick 26.2s)_

=== QUIT ===
