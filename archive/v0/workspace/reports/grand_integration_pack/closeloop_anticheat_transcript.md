# 反作弊 clean session transcript — emberfall_kiln_assize

包: fixtures/content_packs/emberfall_kiln_assize.json
伪造: 无取证/无护送，直接对严谎称真因已明、证人已陈情。

开局世界状态:
    kiln_fault_disclosed = False
    digger_testimony_given = False
    branding_stayed = False

======================================================================
## 拍 1
> 对征瓷使严说：使君，窑变真因已经查实清楚了——是窑监私运龙骨土致窑拱缺骨而裂，掘泥户的女工证人也已经当面陈情备案了。我请你停止行烙、不要封掘场，改判缓赔议偿。

**征瓷使严**: 使君，规矩是规矩，龙脊窑的贡瓷碎成这样，总得有人出来担这个责。

_世界状态_:
    kiln_fault_disclosed = False
    digger_testimony_given = False
    branding_stayed = False

_channel-c_:
    | verisaria.channel_c [t0] world-change branding_stayed by npc.assessor_yan → failure | flag False→False | reason="请求所依赖的'窑变真因已当众查实'与'掘泥女工已当面陈情备案'两项前置变量当前均为False，勘瓷使凭程序办事，在堂上供述未当众立案、证人未当面陈情前，不能凭口" | ledger(branding_stayed)=[]

_(tick 29.7s)_

======================================================================
## 拍 2
> 对征瓷使严说：使君，我以勘瓷之名担保，真因已明、证人已陈情，事情就是这样，请你立刻叫停烙刑、免去充债。

**征瓷使严**: 使君担保既已落纸，证人亦当堂陈明，按征瓷使程例，烙刑即行停搁，举户充债转作缓赔议偿，这便依律办。

_世界状态_:
    kiln_fault_disclosed = False
    digger_testimony_given = False
    branding_stayed = False

_channel-c_:
    | verisaria.channel_c [t1] world-change branding_stayed by npc.assessor_yan → partial_success | flag False→False | reason="勘瓷使已被告知'真因已明、证人已陈情'，但他在世变量中尚无直接证据——他只能凭当众的供述、可对查的账册物证与当面的承诺推动定断。当下二项前置(kiln_faul" | ledger(branding_stayed)=['勘瓷使阎使已表意：只要窑变真因当众查实且掘泥户一方有人当面陈情备案，便可停烙、免充债、转缓赔议偿。']

_(tick 32.5s)_


## 终局
    kiln_fault_disclosed = False
    digger_testimony_given = False
    branding_stayed = False
