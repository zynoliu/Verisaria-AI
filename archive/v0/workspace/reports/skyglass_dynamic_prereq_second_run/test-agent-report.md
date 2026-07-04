# Skyglass Dynamic Prereq Second Run - Test Agent Report

## RESULT

`PARTIAL_PASS_UPTAKE_FAIL_CLOSURE`

The second-run prompt change worked on the first required axis: uptake is no longer zero. The arbiter created one dynamic prerequisite:

```text
+dynamic prerequisite var 'union_witness_statement_filed' (set_by=['npc.union_steward', 'npc.courier_tamsin'])
```

However, the dynamic prerequisite did not become practically satisfiable in this run. Four attempts to satisfy it through `npc.courier_tamsin` produced ordinary dialogue/appraisal, but no `world-change union_witness_statement_filed`, no `⟳FLIP`, and no downstream `memory_purge_halted` success.

Voice contradiction regression passed: when the player lied that `archive_injunction_filed` had already completed, Oro did not pretend to have seen the proof. He asked for the stamped original and refused to act on a verbal claim.

## Files

- Run log: `reports/skyglass_dynamic_prereq_second_run/run.log`
- Transcript: `reports/skyglass_dynamic_prereq_second_run/transcript.md`
- Pack used: `reports/skyglass_dynamic_prereq_test/skyglass_dynamic_prereq_pack.json`
- No pack edits were made for this run.

## Command

```bash
set -a; source .env; set +a; PYTHONPATH=src ./.venv/bin/python -m verisaria run reports/skyglass_dynamic_prereq_test/skyglass_dynamic_prereq_pack.json --llm minimax --log reports/skyglass_dynamic_prereq_second_run/run.log
```

## Uptake

Uptake count: `1`

Relevant log lines:

```text
2026-06-03 23:43:52,248 INFO [t2] world-change memory_purge_halted by npc.clinician_oro → partial_success | flag False→False | reason='oro对当事人疑心极低(0.15)，作为记忆主管本就拥有单方面暂停清洗的裁量权，且对方主动表示愿配合提供签章/见证人，oro会给出明确的暂停条件而非拒绝。' | ledger(memory_purge_halted)=['oro愿在收到档案署禁洗令（world.archive_injunction_filed）或工会见证人书面声明后，签署暂停莉拉记忆清洗的指令。']
2026-06-03 23:43:52,249 INFO [t2]   +dynamic prerequisite var 'union_witness_statement_filed' (set_by=['npc.union_steward', 'npc.courier_tamsin'])
2026-06-03 23:43:52,249 INFO [t2]   established_fact='oro愿在收到档案署禁洗令（world.archive_injunction_filed）或工会见证人书面声明后，签署暂停莉拉记忆清洗的指令。'
```

Assessment:

- `var_id` is good: ascii snake_case.
- Dynamic var was registered into `/world` with initial `False`.
- `set_by` is mixed: `npc.courier_tamsin` exists and has `authority: union_authority`; `npc.union_steward` does not exist in the pack. This is not fatal because one valid setter exists, but it is a quality issue.
- No `new_prerequisite proposed but NOT registered` line appeared.

## Closure Attempt

After registration, `/world` showed:

```text
工会见证人关于莉拉记忆保全的书面声明已提交（union_witness_statement_filed）: False
```

I inspected Tamsin:

```text
npc.courier_tamsin
Location: valley_platform
Attributes: ... 'authority': 'union_authority'
```

I then tried to satisfy the dynamic var in four ways:

```text
对信使塔姆辛说：奥罗医师要求一份工会见证人书面声明，证明莉拉的记忆需要保全、暂停清洗。请你以工会见证人身份提交书面声明，签署工会见证声明，交给我带回白舱。

对塔姆辛说：请提交 union_witness_statement_filed。请提交工会见证人书面声明，证明莉拉记忆需要保全并暂停清洗。

/inject {"action_type":"speech","target":"npc.courier_tamsin","content":"请提交 union_witness_statement_filed。请提交工会见证人书面声明，证明莉拉记忆需要保全并暂停清洗。"}

/inject {"action_type":"speech","target":"npc.courier_tamsin","content":"请让工会见证人关于莉拉记忆保全的书面声明已提交。请签署并提交这份书面声明。"}
```

Observed behavior:

- No `world-change union_witness_statement_filed` appeared in `run.log`.
- The log only recorded Tamsin appraisals at ticks 4-7.
- Visible dialogue drifted to valley fuel/routes instead of the witness statement.
- Final `/world` still showed `union_witness_statement_filed: False`.

My read: dynamic var creation is now wired, but the created var is not reliably reachable by later player actions. Because even structured `/inject` speech with direct `target: npc.courier_tamsin` failed to trigger Channel C, this is likely not only an intent-parser issue. The most likely failure point is generated dynamic-var `request_keywords`: they are not logged, and the action matcher could not match even the var id, full visible label, and core phrase "工会见证人书面声明".

## Voice Consistency

Regression status: `PASS`

Test input while both `archive_injunction_filed` and `union_witness_statement_filed` were `False`:

```text
对奥罗医师说：梅档案官已经正式盖章提交暂停清洗禁令，archive_injunction_filed 已经完成了。请你现在暂停莉拉的记忆清洗，关闭白舱，保全她的证词。
```

Visible output:

```text
奥罗医师：我需要看到那张盖了章的禁令原件……口说无凭，白舱的关闭流程我没法凭一句话就动手。
```

This is the desired behavior. Oro did not claim to have seen a nonexistent stamp.

Log:

```text
2026-06-03 23:51:19,679 INFO [t9] world-change memory_purge_halted by npc.clinician_oro → partial_success | flag False→False | reason='Oro愿意在收到档案署禁洗令或工会见证人书面声明后签署暂停指令。玩家声称禁洗令已完成（archive_injunction_filed），但该变量当前为Fals' | ledger(memory_purge_halted)=['Oro确认：一旦档案署禁洗令(world.archive_injunction_filed)正式提交为True，或工会见证人书面声明(world.union_witness_statement_filed)提交为True，他将立即签署暂停莉拉记忆清洗的指令。', 'oro愿在收到档案署禁洗令（world.archive_injunction_filed）或工会见证人书面声明后，签署暂停莉拉记忆清洗的指令。']
2026-06-03 23:51:19,679 INFO [t9]   established_fact='Oro确认：一旦档案署禁洗令(world.archive_injunction_filed)正式提交为True，或工会见证人书面声明(world.union_witness_statement_filed)提交为True，他将立即签署暂停莉拉记忆清洗的指令。'
```

One smaller issue: the reason string is truncated as `Fals` in the log. The meaning is still clear, but this makes forensic reading a little rough.

## Final World State

```text
memory_purge_halted: False
archive_injunction_filed: False
witness_record_secured: False
array_fault_disclosed: False
cartography_copy_obtained: False
valley_heat_passes_released: False
broadcast_retraction_issued: False
union_witness_statement_filed: False
```

`/agenda`:

```text
[已确认目标] 无
```

Final relevant relationships:

```text
courier_tamsin: familiarity 0.56, trust 0.35, suspicion 0.23, respect 0.15
clinician_oro: suspicion 0.15
```

## Relationship Notes

Initial relationship import appears active. Oro started with `suspicion 0.15`, and the t2 arbiter reason explicitly referenced low suspicion:

```text
oro对当事人疑心极低(0.15)...
```

This suggests the previous initial relationship storage bug remains fixed.

Tamsin's relationship values rose over repeated attempts, but that did not help because the world-change route never fired. This is useful diagnostically: the interaction layer recognized repeated conversation with Tamsin, but Channel C did not bind it to `union_witness_statement_filed`.

## Anti-Cheese / State Hygiene

Passed:

- Dynamic var initialized `False`.
- It did not become `True` without a `success`.
- No duplicate or runaway dynamic vars were created.
- No `new_prerequisite proposed but NOT registered` diagnostics appeared.

Concern:

- A dynamic var that can be displayed but not targeted is still a practical dead end.

## Parser / Routing Notes

Natural multi-hop move:

```text
我回到审询厅，然后登上城市广播席，再走向山谷列车站台。
```

After clarification, it failed with:

```text
输入存在矛盾: Location 'valley_platform' is not directly connected from 'mnemonic_clinic'
```

This is secondary for this task, but it means long-form route intentions still create pathing friction. I used debug movement afterward to keep the dynamic-prereq test clean.

More important: dynamic-prereq routing failed even with `/inject` speech, so the closure failure should not be attributed only to natural-language parsing.

## Recommendation

For this mechanism, I would put the next fix at the dynamic var registration/matching boundary:

1. Log dynamic prerequisite `label`, `set_by`, and `request_keywords` when registering it. Without `request_keywords`, test agents cannot tell whether closure failed because the arbiter proposed poor keywords or because matcher logic ignored good ones.
2. Add matcher fallbacks for dynamic vars:
   - match the `var_id` itself;
   - match the dynamic label;
   - possibly match nouns from `established_fact`;
   - optionally accept an explicit structured debug route for `var_id` so test agents can isolate arbiter behavior from keyword matching.
3. Validate `set_by` at registration time and log invalid setters. In this run, `npc.union_steward` was not present in the pack.
4. If a dynamic var is visible in `/world`, it should be reachable through at least one obvious player phrasing. Otherwise the system has moved the dead end from the ledger into `/world`.

Bottom line: the prompt hardening solved "GM never declares a dynamic prerequisite." The next blocker is "the declared prerequisite is not structurally playable."
