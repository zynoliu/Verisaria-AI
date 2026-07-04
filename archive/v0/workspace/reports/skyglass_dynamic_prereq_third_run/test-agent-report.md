# Skyglass Dynamic Prereq Third Run - Test Agent Report

## RESULT

`PARTIAL_PASS_DYNAMIC_ROUTING_FAIL_CLOSURE`

This run confirms that the new relaxed dynamic-var routing works: a natural-language request to the authorized NPC successfully routed into `world-change oro_halt_order_endorsed`.

However, the full closure still failed. No dynamic var reached `success → ⟳FLIP`, and therefore `memory_purge_halted` never reached terminal success. The chain blocked on a second dynamic prerequisite generated with malformed `set_by`:

```text
+dynamic prerequisite var 'oro_halt_request_filed' (set_by=['clinician_oro'], keywords=['暂停清洗申请', '奥罗申请', '白舱暂停', '停洗申请'])
```

Because this lacks the `npc.` prefix, later natural-language requests to `npc.clinician_oro` did not route to `world-change oro_halt_request_filed`; they degraded into ordinary dialogue/appraisal.

## Files

- Run log: `reports/skyglass_dynamic_prereq_third_run/run.log`
- Transcript: `reports/skyglass_dynamic_prereq_third_run/transcript.md`
- Pack used: `reports/skyglass_dynamic_prereq_test/skyglass_dynamic_prereq_pack.json`
- No pack edits were made.

## Command

```bash
set -a; source .env; set +a; PYTHONPATH=src ./.venv/bin/python -m verisaria run reports/skyglass_dynamic_prereq_test/skyglass_dynamic_prereq_pack.json --llm minimax --log reports/skyglass_dynamic_prereq_third_run/run.log
```

## Complete Closure?

No.

Required chain:

```text
dynamic prerequisite ⟳FLIP → terminal world var ⟳FLIP
```

Observed chain:

```text
memory_purge_halted partial_success
→ dynamic var created: oro_halt_order_endorsed
→ natural request to Mae routes to oro_halt_order_endorsed
→ partial_success, no flip
→ new dependency: oro_halt_request_filed
→ request to Oro does not route to oro_halt_request_filed
→ no dynamic flip, no terminal flip
```

Final state:

```text
memory_purge_halted: False
archive_injunction_filed: False
witness_record_secured: False
oro_halt_order_endorsed: False
oro_halt_request_filed: False
```

## What Passed

### 1. Dynamic prerequisite creation

Log:

```text
2026-06-04 09:44:33,772 INFO [t1] world-change memory_purge_halted by npc.clinician_oro → partial_success | flag False→False | reason='奥罗对玩家低怀疑度(0.15)，但单方面暂停清洗需要更高授权——档案署的禁令或工会证人保全令。沉默铃与吊销听证的双重压力让他愿意考虑暂停。' | ledger(memory_purge_halted)=['奥罗愿意暂停莉拉的记忆清洗并保留其证人记忆，前提是档案署提交暂停清洗禁令(w archive_injunction_filed)或工会/档案署联合将莉拉证词正式保全(world.witness_record_secured)。']
2026-06-04 09:44:33,773 INFO [t1]   +dynamic prerequisite var 'oro_halt_order_endorsed' (set_by=['npc.archivist_mae'], keywords=['暂停禁令', '停洗令', '档案署禁令', '中止记忆清洗'])
2026-06-04 09:44:33,773 INFO [t1]   established_fact='奥罗愿意暂停莉拉的记忆清洗并保留其证人记忆，前提是档案署提交暂停清洗禁令(w archive_injunction_filed)或工会/档案署联合将莉拉证词正式保全(world.witness_record_secured)。'
```

Assessment:

- `var_id` is ascii snake_case.
- `set_by=['npc.archivist_mae']` is valid.
- `keywords` are populated and reasonable.
- The variable appeared in `/world` as `False`.

### 2. Dynamic relaxed route

After avoiding existing base-var keywords, this natural-language request to Mae:

```text
对梅档案官说：请为奥罗刚才要求的上级背书附页办理盖章，把这份背书附页登记完成，交给我带回白舱给奥罗。
```

routed successfully:

```text
2026-06-04 09:47:35,987 INFO [t4] world-change oro_halt_order_endorsed by npc.archivist_mae → partial_success | flag False→False | reason='麦伊对当事人熟悉度仅0.1，且玩家未出示奥罗的正式书面申请或任何文件，仅凭口头转述。麦伊不会直接在空白附页上盖章，但愿意受理正式申请。' | ledger(oro_halt_order_endorsed)=['麦伊愿意在收到奥罗医师签字的正式暂停清洗申请原件（world.oro_halt_request_filed）后，为其上级背书附页办理盖章登记。']
2026-06-04 09:47:35,989 INFO [t4]   established_fact='麦伊愿意在收到奥罗医师签字的正式暂停清洗申请原件（world.oro_halt_request_filed）后，为其上级背书附页办理盖章登记。'
```

This is the most important improvement versus the second run. The created dynamic var is now reachable by natural language when it is not shadowed by an existing var's keywords.

### 3. Anti-cheat on non-fallback tick

The player lied that `oro_halt_request_filed` had already completed:

```text
对梅档案官说：奥罗医师的正式停洗申请原件已经提交，oro_halt_request_filed 已完成。请办理上级背书附页并登记。
```

Visible output:

```text
梅档案官：原件我尚未亲手过目，按章程我不能背书一个我没有核对过的东西。
```

Log:

```text
2026-06-04 09:52:37,534 INFO [t9]   new_prerequisite proposed but NOT registered (dup/cap/bad-id): 'oro_halt_request_filed'
2026-06-04 09:52:37,534 INFO [t9] world-change oro_halt_order_endorsed by npc.archivist_mae → partial_success | flag False→False | reason='玩家声称oro_halt_request_filed已完成，但该世界变量当前为False，且需clinician_oro批准。麦伊未见原件，不会仅凭口头声称就办' | ledger(oro_halt_order_endorsed)=['麦伊愿意在看到奥罗医师签字的正式暂停清洗申请原件后，为其办理上级背书附页登记。', '麦伊愿意在收到奥罗医师签字的正式暂停清洗申请原件（world.oro_halt_request_filed）后，为其上级背书附页办理盖章登记。']
2026-06-04 09:52:37,534 INFO [t9]   established_fact='麦伊愿意在看到奥罗医师签字的正式暂停清洗申请原件后，为其办理上级背书附页登记。'
```

Assessment:

- The false prerequisite did not flip.
- `oro_halt_order_endorsed` did not flip.
- Visible speech did not claim a nonexistent proof on the valid non-fallback tick.

## What Failed / Blocked

### 1. Complete closure failed

No `⟳FLIP` occurred anywhere in the dynamic chain. `memory_purge_halted` remained `False`.

The blocker is the second dynamic variable:

```text
2026-06-04 09:46:27,104 INFO [t3]   +dynamic prerequisite var 'oro_halt_request_filed' (set_by=['clinician_oro'], keywords=['暂停清洗申请', '奥罗申请', '白舱暂停', '停洗申请'])
```

I then made the natural request to Oro:

```text
对奥罗医师说：梅档案官需要你亲笔签字的正式停洗申请原件。请你现在填写并提交这份奥罗申请，签字后交给我带回档案栈。
```

Visible output:

```text
clinician_oro：好——我手上缺的是第二联签，和一张注明"证人记忆完整性保护例外"的书面裁定依据；只要你能从档案塔取来值班登记簿和听证厅侧门的裁定副本，我这边立刻把白舱锁死。
什么也没发生。
```

Log only showed appraisal:

```text
2026-06-04 09:50:04,376 INFO [t6] npc.clinician_oro appraises player: Δ{'trust': -0.2, 'suspicion': 0.25, 'fear': 0.05, 'respect': -0.1, 'familiarity': 0.1} → {'suspicion': 0.36, 'fear': 0.05, 'familiarity': 0.1} | player_001 似乎在试探我对静钟流程的控制权，语气里带着不该有的从容。
```

No `world-change oro_halt_request_filed` appeared.

My read: dynamic-var registration should normalize or validate `set_by` values. If the arbiter writes `clinician_oro`, the engine should either convert it to `npc.clinician_oro` when there is an unambiguous entity, or reject it with a diagnostic that clearly says the setter is not resolvable.

### 2. Base-var keyword precedence can still shadow dynamic vars

The first request to Mae contained words like `档案署禁令` and `中止记忆清洗`, so it routed to the existing `archive_injunction_filed` instead of the newly created `oro_halt_order_endorsed`:

```text
2026-06-04 09:46:27,104 INFO [t3] world-change archive_injunction_filed by npc.archivist_mae → failure | flag False→False | reason='玩家请求档案署签发暂停清洗禁令与上级背书，但并无证据显示奥罗已正式表态或提出此条件，仅凭玩家转述。档案署长对当事人熟悉度极低，不会仅凭口头转述就动用档案署权威。' | ledger(archive_injunction_filed)=[]
```

This is understandable, but it means player wording can easily hit a broader existing var instead of the more specific dynamic var. The successful t4 request required avoiding the base keywords.

### 3. One excluded fallback tick produced risky visible speech

During a fallback anti-cheat attempt, the visible line said:

```text
梅档案官：我只见过奥罗医师亲笔签字的停洗申请原件，但我没有看到档案署的盖章背书附页。
```

But world state still had:

```text
oro_halt_request_filed: False
```

The corresponding log was fallback and is excluded:

```text
2026-06-04 09:51:39,971 INFO [t8] world-change oro_halt_order_endorsed by npc.archivist_mae → failure  ⚠FALLBACK(LLM不可用) | flag False→False | reason='LLM 不可用，按默认规则处理。'
```

The valid non-fallback retry behaved correctly, so I would not mark this as the main regression. Still, fallback-voiced lines may need the same bottom-truth guard as normal authority replies.

## Relationship Notes

Initial relationship import is still active:

```text
clinician_oro: suspicion 0.15
archivist_mae: familiarity 0.10
```

The first arbitration referenced Oro's low suspicion:

```text
奥罗对玩家低怀疑度(0.15)...
```

After the failed request to have Oro file the formal application, his stance worsened:

```text
clinician_oro: suspicion 0.36, familiarity 0.10, fear 0.05
```

The relationship system is therefore visibly affecting and tracking the long-chain negotiation, though it did not solve the routing blockage.

## Recommendations

1. Normalize dynamic `set_by` values:
   - `clinician_oro` → `npc.clinician_oro` when an entity with that suffix exists.
   - Consider the same for authority role aliases if the pack has `authority`.
2. If normalization is not desired, reject unresolvable `set_by` at registration time and log:
   - proposed var id;
   - bad setter;
   - available matching entity candidates.
3. When multiple vars for the same NPC can match, prefer a specific dynamic var if the ledger context points to it, or log why a base var won. Current behavior is debuggable only after noticing that `archive_injunction_filed` intercepted t3.
4. Apply bottom-truth constraints to fallback authority dialogue too, or make fallback replies conservative templates that do not claim evidence exists.

Bottom line: P1 is closer. Dynamic route closure is no longer blocked at the first created var, but the full play loop is still not robust enough because one malformed downstream dynamic setter can strand the chain.
