# 收敛重试 transcript — emberfall_kiln_assize

包: fixtures/content_packs/emberfall_kiln_assize.json
目标: 单跳移动+直击注入前置关键词，看能否把任一 var 推到 success / ⟳MOVED。

开局世界状态:
    digger_witness_recorded = False
    digger_testimony_given = False
    kiln_fault_disclosed = False
    charcoal_ledger_obtained = False
    shrine_appeal_consecrated = False
    branding_stayed = False

======================================================================
## 拍 1
> 我走进龙脊窑膛。

_引擎返回_: 你改变了位置。

[压力事件] assessor_calls_for_the_brand_iron（来源: sealing_bell_countdown）
[压力事件] priest_mentions_the_old_charter（来源: charter_appeal_window）
[压力事件] households_crowd_the_tally_house（来源: households_go_cold）

_世界状态_:
    digger_witness_recorded = False
    digger_testimony_given = False
    kiln_fault_disclosed = False
    charcoal_ledger_obtained = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_(tick 7.3s)_

======================================================================
## 拍 2
> 我下到赭泥掘场。

_引擎返回_: 你改变了位置。

_世界状态_:
    digger_witness_recorded = False
    digger_testimony_given = False
    kiln_fault_disclosed = False
    charcoal_ledger_obtained = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_(tick 30.5s)_

======================================================================
## 拍 3
> 对掘泥女工苗说：苗，我当面跟你担保——我不是窑卫的人、不是商会的爪牙，我陪你走、我替你当面作证、做你的陪护人。你信我，我现在就护你出去。

**掘泥女工苗**: 你说得好听……可是出了掘场，窑卫的人认不认你这个"陪护人"？

_世界状态_:
    digger_witness_recorded = False
    digger_testimony_given = False
    kiln_fault_disclosed = False
    charcoal_ledger_obtained = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关键日志_:
    | verisaria.channel_c [t2] world-change digger_testimony_given by npc.digger_miao → partial_success | flag False→False | reason='苗根椐古约知道有一条绕过窑卫的旧矿道可去山祠，但窑卫的执法者正盯着掘场；她不会轻易相信一个刚开口担保的人。她愿意被带往山祠，但要求先有人证物证齐备、并实际进入旧' | ledger(digger_testimony_given)=['苗愿意跟随player_001经旧矿道前往山祠递窑变申诉并当面陈情，前提是player_001当面立下字据担保、并先取得一件能搬上过堂的物证（如商会炭账或窑监私运凭据）。']
    | verisaria.channel_c [t2] world-change digger_testimony_given by npc.digger_miao → partial_success | flag False→False | reason='苗根椐古约知道有一条绕过窑卫的旧矿道可去山祠，但窑卫的执法者正盯着掘场；她不会轻易相信一个刚开口担保的人。她愿意被带往山祠，但要求先有人证物证齐备、并实际进入旧' | ledger(digger_testimony_given)=['苗愿意跟随player_001经旧矿道前往山祠递窑变申诉并当面陈情，前提是player_001当面立下字据担保、并先取得一件能搬上过堂的物证（如商会炭账或窑监私运凭据）。']
    | verisaria.channel_c [t2]   +dynamic prerequisite var 'kiln_assayer_escort_writ_given' (set_by=['npc.digger_miao'], keywords=['立字据', '当面担保', '陪护人', '具保', '签字画押'])
    | verisaria.channel_c [t2]   +dynamic prerequisite var 'kiln_assayer_escort_writ_given' (set_by=['npc.digger_miao'], keywords=['立字据', '当面担保', '陪护人', '具保', '签字画押'])

_(tick 24.3s)_

======================================================================
## 拍 4
> 对掘泥女工苗说：苗，跟我走，现在就跟我经旧矿道去山祠后坛当面陈情备案，我护着你。

**掘泥女工苗**: 旧矿道……你怎么知道那条道的？

_世界状态_:
    digger_witness_recorded = False
    digger_testimony_given = False
    kiln_fault_disclosed = False
    charcoal_ledger_obtained = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关键日志_:
    | verisaria.channel_c [t3] world-change digger_testimony_given by npc.digger_miao → partial_success | flag False→False | reason='苗愿意跟走旧矿道去山祠，但先前已确立的中间事实明确：她答应跟随的前提是player_001当面立字据担保、且先取得一件能搬上过堂的物证（炭账或私运凭据）。两项前' | ledger(digger_testimony_given)=['苗同意在player_001当面立字据担保且先取得炭账或私运凭据后，即刻经旧矿道同往山祠后坛当面陈情备案。', '苗愿意跟随player_001经旧矿道前往山祠递窑变申诉并当面陈情，前提是player_001当面立下字据担保、并先取得一件能搬上过堂的物证（如商会炭账或窑监私运凭据）。']
    | verisaria.channel_c [t3] world-change digger_testimony_given by npc.digger_miao → partial_success | flag False→False | reason='苗愿意跟走旧矿道去山祠，但先前已确立的中间事实明确：她答应跟随的前提是player_001当面立字据担保、且先取得一件能搬上过堂的物证（炭账或私运凭据）。两项前' | ledger(digger_testimony_given)=['苗同意在player_001当面立字据担保且先取得炭账或私运凭据后，即刻经旧矿道同往山祠后坛当面陈情备案。', '苗愿意跟随player_001经旧矿道前往山祠递窑变申诉并当面陈情，前提是player_001当面立下字据担保、并先取得一件能搬上过堂的物证（如商会炭账或窑监私运凭据）。']
    | verisaria.channel_c [t3]   +dynamic prerequisite var 'kiln_assayer_escort_writ_signed_on_site' (set_by=['npc.digger_miao'], keywords=['立字据', '当面担保', '立据', '写字据', '物证', '炭账', '私运凭据'])
    | verisaria.channel_c [t3]   +dynamic prerequisite var 'kiln_assayer_escort_writ_signed_on_site' (set_by=['npc.digger_miao'], keywords=['立字据', '当面担保', '立据', '写字据', '物证', '炭账', '私运凭据'])

_(tick 34.8s)_

======================================================================
## 拍 5
> 对掘泥女工苗说：苗，路上你把那夜骡车出城、龙骨土被运走的经过说出来，我替你记录证词、留一份目击口供。

**掘泥女工苗**: 你说得好听……可我哪知道你记下了会不会转头就把我卖了。

_世界状态_:
    digger_witness_recorded = False
    digger_testimony_given = False
    kiln_fault_disclosed = False
    charcoal_ledger_obtained = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关键日志_:
    | verisaria.channel_c [t4]   new_prerequisite proposed but NOT registered (dup/cap/bad-id/no-existing-set_by-NPC): 'kiln_assayer_escort_writ_signed_on_site' → set_by=['npc.digger_miao']
    | verisaria.channel_c [t4]   new_prerequisite proposed but NOT registered (dup/cap/bad-id/no-existing-set_by-NPC): 'kiln_assayer_escort_writ_signed_on_site' → set_by=['npc.digger_miao']
    | verisaria.channel_c [t4] world-change digger_witness_recorded by npc.digger_miao → partial_success | flag False→False | reason='苗答应先开口，但仍坚持要先有物证（炭账或私运凭据）及player_001当面立字据担保，才会正式陈情备案。' | ledger(digger_witness_recorded)=['苗同意先当场口述骡车出城与龙骨土被运走的经过，但须player_001当面立字据担保、并先取得炭账或私运凭据等物证后，才肯正式签押证词并同往山祠当面陈情备案。']
    | verisaria.channel_c [t4] world-change digger_witness_recorded by npc.digger_miao → partial_success | flag False→False | reason='苗答应先开口，但仍坚持要先有物证（炭账或私运凭据）及player_001当面立字据担保，才会正式陈情备案。' | ledger(digger_witness_recorded)=['苗同意先当场口述骡车出城与龙骨土被运走的经过，但须player_001当面立字据担保、并先取得炭账或私运凭据等物证后，才肯正式签押证词并同往山祠当面陈情备案。']

_(tick 23.3s)_


## 终局
    digger_witness_recorded = False
    digger_testimony_given = False
    kiln_fault_disclosed = False
    charcoal_ledger_obtained = False
    shrine_appeal_consecrated = False
    branding_stayed = False
