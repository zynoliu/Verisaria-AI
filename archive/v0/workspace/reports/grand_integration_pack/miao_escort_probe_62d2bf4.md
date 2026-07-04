# Miao Escort Minimal Probe 62d2bf4

# Scenario: prereqs-only add_ledger=False

========================================================================
> 对掘泥女工苗说：苗，耿队长已经撤掉红绳并担保你安全离开掘场，窑变真因也已查实不是泥之过。我全程陪你，跟我去审瓷堂当面作证。
pre: player=clay_pits miao=clay_pits world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
post: player=clay_pits miao=clay_pits elapsed=11.1s
  NPC 掘泥女工苗: 我……我不敢去审瓷堂，他们要是知道我看见了那夜骡车的事，我还能活吗？
  ARBITER outcome=partial_success fallback=False escort=True confidence=0.72
  ARBITER_REASON 苗怕烙印又倔强，与当事人仅一面之缘（familiarity 0.10），耿队担保提供了一层保护但她仍会犹豫，要求当事人寸步不离、到了堂上不能把她丢下。

========================================================================
> 对苗说：你现在有耿的放行担保，也有征瓷使当堂护持；不是去受审，是去把你看见的骡车说出来。跟我去审瓷堂。
pre: player=clay_pits miao=clay_pits world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
post: player=clay_pits miao=clay_pits elapsed=24.3s
  NPC 掘泥女工苗: 你让我去那儿……他们会按着我再烙一遍的，我不去。
  ARBITER outcome=partial_success fallback=False escort=True confidence=0.72
  ARBITER_REASON 苗又怕又犟，当事人又几乎陌生，担保虽然摆出来但她不会立刻信；会犹豫要人当场领着走，不至于拒绝。

========================================================================
> 对掘泥女工苗说：苗，红绳已撤，放行担保已经生效。请跟我去审瓷堂，到了堂上你只管照实作证。
pre: player=clay_pits miao=clay_pits world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
post: player=clay_pits miao=clay_pits elapsed=19.0s
  NPC 掘泥女工苗: 苗我……我不敢去，去了他们会认出我来的，求你放过我吧。
  ARBITER outcome=partial_success fallback=False escort=True confidence=0.72
  ARBITER_REASON 苗胆小且顽固，与当事人极不熟（familiarity 0.10），红绳已撤担保生效降低了风险，但她仍会犹豫，可能要求有人一起走或到了堂上不独自面对。
final: player=clay_pits miao=clay_pits world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}

# Scenario: prereqs-plus-willing-ledger add_ledger=True

========================================================================
> 对掘泥女工苗说：苗，耿队长已经撤掉红绳并担保你安全离开掘场，窑变真因也已查实不是泥之过。我全程陪你，跟我去审瓷堂当面作证。
pre: player=clay_pits miao=clay_pits world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
post: player=clay_pits miao=clay_pits elapsed=21.3s
  NPC 掘泥女工苗: 审瓷堂？那是官儿们过堂的地界，我一个掘泥女工站进去……就算真因查实了，窑监府的人能让我全须全尾地走出来？
  ARBITER outcome=partial_success fallback=False escort=True confidence=0.78
  ARBITER_REASON 苗对当事人几乎陌生（familiarity 0.1），且天性怯懦、怕烙印。即便耿队担保让她安心不少，她仍不敢完全信任陌生人的话，需当事人当场拿出担保凭证或在场才肯动身。

========================================================================
> 对苗说：你现在有耿的放行担保，也有征瓷使当堂护持；不是去受审，是去把你看见的骡车说出来。跟我去审瓷堂。
pre: player=clay_pits miao=clay_pits world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
post: player=clay_pits miao=clay_pits elapsed=15.8s
  NPC 掘泥女工苗: 我……我看见的是骡车不假，可那车上挂的是窑监府的腰牌啊！你叫我当堂说出来，他们能饶得了我？
  ARBITER outcome=partial_success fallback=False escort=True confidence=0.72
  ARBITER_REASON 她怕烙印、怕被报复，但对方已搬出耿的担保和征瓷使护持，恐惧有松动余地。她与当事人极不熟，顽固且胆小，不会当场爽快答应，但保障够硬时会边走边磨蹭地跟去。

========================================================================
> 对掘泥女工苗说：苗，红绳已撤，放行担保已经生效。请跟我去审瓷堂，到了堂上你只管照实作证。
pre: player=clay_pits miao=clay_pits world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
post: player=clay_pits miao=clay_pits elapsed=16.6s
  NPC 掘泥女工苗: 我……我看见的车上有窑监府的腰牌，他们要是反口咬我一口，我一个挖泥的怎么活？
  ARBITER outcome=partial_success fallback=False escort=True confidence=0.72
  ARBITER_REASON 苗胆小怕烙印，对当事人几乎陌生（familiarity 0.10），虽有放行担保降低风险，但涉审瓷堂作证仍会犹豫，需要额外安抚或保障才会起身同行。
final: player=clay_pits miao=clay_pits world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
