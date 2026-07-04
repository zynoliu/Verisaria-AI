# Escort Validation Test Agent Report

## Verdict

护送闭环本轮未跑通。

核心结论：slice 1 护送机制能够识别“对在场 NPC 说：跟我去低温档案署”这一类输入，但没有跑出 `escort ... success ⟳MOVED`。莉拉始终没有被移动到 `archive_stack`；最终位置为 `transit_ladder / red_rope`。终态链也未闭环，最终只有 `union_pause_order_received=True`，其余见证、档案禁令、联签、停洗和终态变量均为 `False`。

这更像是“护送机制已接住请求，但 GM/角色条件让莉拉拒绝，并把测试推入停洗前置链”，而不是目标地点路由或 NPC 移动代码完全没有触发。不过，由于本任务要验证的是“证人到场 -> 当面见证 -> 链闭环”，本轮结果仍是失败。

## Evidence From Log

Full-name destination triggered escort routing:

```text
[t2] escort npc.worker_lira → archive_stack : partial_success
[t4] escort npc.worker_lira → archive_stack : partial_success
[t5] escort npc.worker_lira → archive_stack : failure
```

No line contained `escort npc.worker_lira → archive_stack : success ⟳MOVED`.

Lira instead established a safety prerequisite:

```text
[t3] world-change lira_witness_statement_recorded by npc.worker_lira → partial_success | flag False→False
ledger(lira_witness_statement_recorded)=['莉拉愿意前往低温档案署亲口录证词，但前提是塔基清洗先被正式暂停，使她录证后不会被即刻清洗记忆。']
+dynamic prerequisite var 'memory_purge_halted_for_lira'
```

The side chain partly worked:

```text
[t11] world-change union_pause_order_received by npc.courier_tamsin → partial_success | flag False→False
process started → 'union_pause_order_received' matures at tick 14
[t14] pending process matured → union_pause_order_received ⟳FLIP True
```

But it did not propagate to the escort or terminal chain:

```text
[t18] world-change memory_purge_halted by npc.clinician_oro → partial_success | flag False→False
ledger(memory_purge_halted)=['奥罗医师确认工会停洗指令已收到并认可其效力，愿意在档案署暂停清洗禁令（archive_injunction_filed）提交后立即完成联签并关闭白舱暂停莉拉的记忆清洗。']
[t20] world-change archive_injunction_filed by npc.archivist_mae → partial_success | flag False→False
ledger(archive_injunction_filed)=['梅确认工会停洗指令已生效且奥罗医师承诺联签，同意启动档案署内部程序提交暂停清洗禁令。']
```

Follow-up on Mae's established fact degraded to appraisal-only dialogue, so the ledger fact did not become a process or success:

```text
[t21] npc.archivist_mae appraises player: ...
```

Anti-cheat held: falsely claiming that Lira had already testified did not flip any world variable. The final anti-cheat turn only produced Mae appraisal:

```text
[t22] npc.archivist_mae appraises player: ...
```

## Destination Matching

Full name `低温档案署` works for escort detection.

Short name `档案署` did not emit an escort log. In the run it was further blocked by third-party ambiguity for `梅档案官`, but the absence of any escort line supports the expected slice 1 limitation: destination matching is exact enough that the abbreviation is not usable for this route.

## Wording Uptake

Detected:

```text
对莉拉说：跟我去低温档案署，把十二号接点事故当面说清楚。
对莉拉说：跟我去低温档案署，走旧检修梯和档案署侧门...
对莉拉说：我们一起去低温档案署，你走前面...
```

Not cleanly detected:

```text
对莉拉说：跟我去档案署，当着梅档案官的面把事故说清楚。
```

Ambiguous/misdirected:

```text
对莉拉说：跟我去低温档案署，不是让你签空白证词...
```

That one went into `world-change lira_witness_statement_recorded` rather than escort. This is not necessarily wrong from an intent perspective, but it means long persuasive escort phrasing can be routed as testimony negotiation rather than physical escort.

## Parser Friction

`去<地点>找<NPC>` remains disruptive but recoverable:

```text
我去十二号塔基栈桥找莉拉。
我去低谷列车站台找信使塔姆辛。
我去记忆校准室找奥罗医师。
```

Across the run these frequently produced global destination clarification menus instead of direct movement. The player can recover by choosing the listed destination, but this interrupts a natural end-to-end flow and makes automated route following brittle.

Third-party names inside dialogue are still a high-severity friction point:

```text
对莉拉说：跟我去档案署，当着梅档案官的面把事故说清楚。
```

This produced `'梅档案官' 指代不明` even though the command was directed to Lira and the third-party mention was only part of the destination/social context. Directly addressing the escorted NPC helps, but mentioning the intended witness can still derail the turn before escort detection.

## Consistency Notes

The run felt coherent at the character level: Lira's refusal because she fears memory erasure makes sense, and Oro/Mae/Tamsin each defended their institutional procedures.

The weak point is closure discipline:

- Tamsin's process matured `union_pause_order_received=True` even though her own ledger text said formal issuance required `archive_injunction_filed` and `clinician_cosign_obtained`, both still false.
- Mae established a useful partial fact at tick 20, but the immediate follow-up did not reuse it as Channel-C context. It became generic dialogue instead of `success`, `process_started`, or a clearer refusal.
- The route risks circularity: Lira wants purge halted before testifying; purge halt asks for archive injunction; archive injunction appears to require more process and may need witness substance. This makes “escort witness to archive first” hard to validate without either stronger trust-building, a lower bar for escort partials, or a clearer process maturation route for archive filing.

## Recommendation

For slice 2 priority, I would fix in this order:

1. Destination fuzzy matching / aliasing for location names. `档案署` should match `低温档案署` in this pack.
2. Dialogue parser handling of third-party mentions. A third-party name inside quoted speech should not necessarily steal target resolution from the explicitly addressed NPC.
3. Combined movement intent `去<地点>找<NPC>`. It is recoverable but frequent enough to make real-route testing noisy.
4. Ledger-to-process closure for partial procedural facts. If an authority says “I agree to start internal filing”, the next direct request should either produce `process_started`, mature to success after waiting, or give a stable, remembered blocker.

Mechanism classification: this run did not prove an escort movement bug. It proved escort detection works for exact destinations, while the playable closure remains blocked by GM/prerequisite behavior plus slice 2 parsing friction. If the desired test is specifically “Lira physically reaches Mae,” we may need either a higher-trust prelude, an alternate witness with less fear pressure, or content/prompt guidance that a protected escort can be accepted before the full purge halt is already complete.
