# 窑监路由隔离 probe (charcoal 预置 True)


## A·只含kiln关键词(不夹炭账)
> 对窑监阔说：阔窑监，断口缺的是龙骨土、非泥之过。请你当众承认私运龙骨土、公开窑变真因，我只论窑务、容你将功折罪、不深究你个人。
    | (无 world-change —— 未路由, 当对白)
    => kiln_fault_disclosed=False  routed_to_kiln=False

## B·开头夹炭账关键词
> 对窑监阔说：阔窑监，官炭私运账已在我手、画押俱全。请你当众承认私运龙骨土、公开窑变真因，我只论窑务、容你将功折罪。
    | (无 world-change —— 未路由, 当对白)
    => kiln_fault_disclosed=False  routed_to_kiln=False

## C·纯祈使最短
> 对窑监阔说：阔窑监，请你公开窑变真因、承认私运龙骨土致窑拱缺骨而裂。
    | verisaria.channel_c [t0] world-change kiln_fault_disclosed by npc.warden_kuo → failure | flag False→False | reason='阔为人guilty且guarded，面对当面指控但无可对查账册物证压在面前时，仅凭口头指认不会认账。无炭账佐证、无证人当面陈情，阔合理地保持戒备并把责任推回掘泥' | ledger(kiln_fault_disclosed)=[]
    => kiln_fault_disclosed=False  routed_to_kiln=True
