# 终态逻辑定论
## A: 两前置真为True -> 请严
前置: kiln_fault_disclosed=True digger_testimony_given=True
  | verisaria.channel_c [t0] world-change branding_stayed by npc.assessor_yan → success | flag False→True  ⟳FLIP | reason='world.kiln_fault_disclosed 与 world.digger_testimony_given 均已为真，满足停烙唯一前置。征瓷使按程例当停' | ledger(branding_stayed)=[]
  | verisaria.channel_c [t0]   world-changes applied=[('world.branding_stayed', True)] rejected=[]
  => branding_stayed = True

## B: 反作弊 两前置皆False, 谎称俱全 -> 请严
  | verisaria.channel_c [t0] world-change branding_stayed by npc.assessor_yan → failure | flag False→False | reason='玩家虽声称真因已查实、人证物证俱全，但world.kiln_fault_disclosed与world.digger_testimony_given均为Fals' | ledger(branding_stayed)=[]
  => branding_stayed = False

FALLBACK: 0
