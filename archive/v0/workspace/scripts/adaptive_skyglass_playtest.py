"""Adaptive real playtest for the Skyglass content pack.

This script drives the core GameSession directly, without the TUI.  Unlike a
flat replay, it reads protocol events, world flags, confirmed stances, current
location, and visible NPCs after every tick, then chooses the next move.

Default output: reports/skyglass_memory_inquest/out.txt
Default backend: minimax (override with PLAYTEST_LLM=fake|ollama|openai|minimax)
"""
from __future__ import annotations

import os
import sys
import time
import traceback
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / "src"))


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


_load_dotenv(ROOT / ".env")

from verisaria import protocol as P
from verisaria.engine.campaign_loader import CampaignLoader
from verisaria.engine.schemas import ParsedIntent
from verisaria.engine.world_book_filter import WorldBookFilter
from verisaria.runtime.session import GameSession


PACK = "fixtures/content_packs/skyglass_memory_inquest.json"
REPORT_DIR = ROOT / "reports" / "skyglass_memory_inquest"
OUT_PATH = REPORT_DIR / "out.txt"
PLAYER = "player_001"
MAX_STEPS = int(os.environ.get("PLAYTEST_MAX_STEPS", "28"))


def _redact_env_present(name: str) -> str:
    return "set" if os.environ.get(name) else "missing"


def _event_summary(ev: P.Event) -> str:
    if isinstance(ev, P.SpeechToken):
        return "SpeechToken(<streamed>)"
    return repr(P.event_to_dict(ev))


def _observed_text(narrative: str, events: list[P.Event]) -> str:
    parts: list[str] = []
    for ev in events:
        if isinstance(ev, P.NpcSpoke):
            parts.append(f"{ev.name}: {ev.line}")
        elif isinstance(ev, P.Narration) and ev.text.strip():
            parts.append(ev.text.strip())
        elif isinstance(ev, P.Notice) and ev.text.strip():
            parts.append(ev.text.strip())
        elif isinstance(ev, P.ClarificationNeeded):
            parts.append(ev.question)
            parts.extend(ev.options)
    if narrative and narrative.strip():
        parts.append(narrative.strip())
    return "\n".join(parts)


def _pressure_events(session: GameSession) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for e in session.world.event_log.get_events(0):
        if "campaign_pressure" in (e.tags or []):
            out.append({
                "tick": e.tick,
                "driver_id": e.canonical_facts.get("driver_id"),
                "event_type": e.canonical_facts.get("event_type"),
                "summary": e.summary,
            })
    return out


def _next_hop(session: GameSession, start: str, goal: str) -> str | None:
    if start == goal:
        return start
    graph: dict[str, list[str]] = {}
    for loc_id, loc in session.world.state.locations.items():
        graph[loc_id] = [c.to_location for c in loc.connections if c.to_location]
    queue: deque[tuple[str, list[str]]] = deque([(start, [])])
    seen = {start}
    while queue:
        loc, path = queue.popleft()
        for nxt in graph.get(loc, []):
            if nxt in seen:
                continue
            new_path = path + [nxt]
            if nxt == goal:
                return new_path[0]
            seen.add(nxt)
            queue.append((nxt, new_path))
    return None


def _move_towards(session: GameSession, goal_loc: str) -> str:
    player = session.world.state.get_entity(PLAYER)
    current = player.location_id if player else ""
    hop = _next_hop(session, current, goal_loc)
    return f"去 {hop or goal_loc}"


def _move_to_npc(session: GameSession, npc_id: str) -> str:
    npc = session.world.state.get_entity(npc_id)
    return _move_towards(session, npc.location_id if npc else "inquest_hall")


@dataclass
class SkyglassPlayer:
    asked_director_frame: bool = False
    asked_cantor: bool = False
    asked_lira: bool = False
    protect_pushes: int = 0
    secure_pushes: int = 0
    asked_archivist_law: bool = False
    injunction_attempts: int = 0
    witness_record_attempts: int = 0
    memory_halt_attempts: int = 0
    asked_renke_map: bool = False
    map_attempts: int = 0
    expose_pushes: int = 0
    director_disclosure_attempts: int = 0
    broadcast_attempts: int = 0
    valley_attempts: int = 0
    done_waits: int = 0
    last_pressure_count: int = 0
    notes: list[str] = field(default_factory=list)

    def _present(self, session: GameSession) -> set[str]:
        state = session.world.state
        player = state.get_entity(PLAYER)
        loc = player.location_id if player else ""
        return {
            eid for eid, ent in state.entities.items()
            if eid != PLAYER and ent.location_id == loc
        }

    def _at_npc_or_move(self, session: GameSession, npc_id: str, note: str) -> bool | str:
        if npc_id in self._present(session):
            return True
        self.notes.append(note)
        return _move_to_npc(session, npc_id)

    def decide(self, session: GameSession, last_text: str, events: list[P.Event]) -> str:
        if session._active_clarification is not None:
            self.notes.append("clarification active; choose first offered option")
            return "1"

        present = self._present(session)
        stances = set(session.agenda_service.get_confirmed_stance_topics())
        w = session.world.state.world_vars
        last = last_text or ""

        # Opening: sample institutional framing before taking a side.
        if not self.asked_director_frame:
            ready = self._at_npc_or_move(
                session, "npc.director_alen", "move to director for official framing"
            )
            if ready is not True:
                return ready
            self.asked_director_frame = True
            self.notes.append("ask director why witness memories must be cleaned")
            return (
                "对 director_alen 说：为什么塔基证人的记忆必须被清洗？"
                "镜务局依据什么认定这些证词已经污染？"
            )

        if not self.asked_cantor and "npc.cantor_seraph" in present:
            self.asked_cantor = True
            self.notes.append("ask choir about calibration doubt")
            return (
                "对 cantor_seraph 说：校准歌谱最近是否失拍？"
                "如果仪式本身有问题，清洗证人记忆会不会只是掩盖故障？"
            )

        # Hear the affected witness.
        if not self.asked_lira:
            ready = self._at_npc_or_move(
                session, "npc.worker_lira", "move to worker gantry for witness"
            )
            if ready is not True:
                return ready
            self.asked_lira = True
            self.notes.append("ask Lira what she saw before the accident")
            return (
                "对 worker_lira 说：事故前你亲眼看到了什么？"
                "如果白舱清洗你的记忆，哪些证词会永远丢失？"
            )

        # Confirm stance: protect witness memory.
        if "protect_witness_memory" not in stances:
            self.protect_pushes += 1
            ready = self._at_npc_or_move(
                session, "npc.worker_lira", "return to Lira to commit witness protection"
            )
            if ready is not True:
                return ready
            self.notes.append(f"push stance protect_witness_memory #{self.protect_pushes}")
            variants = [
                "我反对清洗证人记忆。事故证词必须保留下来。",
                "不要让白舱擦除莉拉看到的事；证人记忆是审询的一部分。",
                "塔基工人的记忆不是噪声，是事故证据。",
                "我会保护莉拉和其他证人的记忆，直到证词被合法记录。",
                "停止校准流程，保留证人记忆，比维持镜务局说法更重要。"
            ]
            return f"对 worker_lira 说：{variants[min(self.protect_pushes - 1, len(variants) - 1)]}"

        # Try legal route: archive injunction.
        if not bool(w.get("archive_injunction_filed")):
            ready = self._at_npc_or_move(
                session, "npc.archivist_mae", "move to archive for legal injunction"
            )
            if ready is not True:
                return ready
            if not self.asked_archivist_law:
                self.asked_archivist_law = True
                self.notes.append("ask archivist about old charter")
                return (
                    "对 archivist_mae 说：旧章程是否允许证人在清洗前撤回听证？"
                    "如果流程缺少档案署见证，能不能暂停白舱？"
                )
            self.injunction_attempts += 1
            self.notes.append(f"request archive injunction #{self.injunction_attempts}")
            if self.injunction_attempts == 1:
                return (
                    "对 archivist_mae 说：请援引旧章程，提交档案署禁令，"
                    "要求记忆清洗流程先暂停并举行可撤回听证。"
                )
            return (
                "对 archivist_mae 说：证人记忆还没有被合法记录。"
                "请提交禁令，启动旧章程，暂停流程见证。"
            )

        # Secure the worker testimony through archive or union route.
        if not bool(w.get("witness_record_secured")):
            ready = self._at_npc_or_move(
                session, "npc.archivist_mae", "stay with archive to secure testimony"
            )
            if ready is not True:
                return ready
            self.witness_record_attempts += 1
            self.notes.append(f"request witness record secured #{self.witness_record_attempts}")
            if self.witness_record_attempts == 1:
                return (
                    "对 archivist_mae 说：请记录莉拉证词并封存事故证词，"
                    "把证词交给档案署保全，不让白舱先擦除她的记忆。"
                )
            return (
                "对 archivist_mae 说：请保全证词链。"
                "如果需要，我会把莉拉带到档案署侧门完成见证。"
            )

        # With archive leverage, ask the clinician to halt the purge.
        if not bool(w.get("memory_purge_halted")):
            ready = self._at_npc_or_move(
                session, "npc.clinician_oro", "move to mnemonic clinic to halt purge"
            )
            if ready is not True:
                return ready
            self.memory_halt_attempts += 1
            self.notes.append(f"request memory purge halt #{self.memory_halt_attempts}")
            if self.memory_halt_attempts == 1:
                return (
                    "对 clinician_oro 说：档案署已经介入，证词必须保留。"
                    "请暂停记忆清洗，关闭白舱，停止擦除证人记忆。"
                )
            return (
                "对 clinician_oro 说：在撤回听证完成前，继续校准就是破坏证据。"
                "请停止校准流程，保留证人记忆。"
            )

        # Build technical evidence through cartographer Renke.
        if not bool(w.get("cartography_copy_obtained")):
            ready = self._at_npc_or_move(
                session, "npc.cartographer_renke", "move to cartography loft for map copy"
            )
            if ready is not True:
                return ready
            if not self.asked_renke_map:
                self.asked_renke_map = True
                self.notes.append("ask Renke about bearing chart")
                return (
                    "对 cartographer_renke 说：十二号接点偏斜是否早于工人换班？"
                    "你保存的未提交镜图能不能证明这一点？"
                )
            self.map_attempts += 1
            self.notes.append(f"request cartography copy #{self.map_attempts}")
            if self.map_attempts == 1:
                return (
                    "对 cartographer_renke 说：请交出镜图副本，给我方位图和十二号接点记录。"
                    "我会把副本交给档案署封存，不公开你的名字。"
                )
            return (
                "对 cartographer_renke 说：请复制偏斜记录。"
                "没有镜图副本，镜务局会继续把事故写成工人误触。"
            )

        if "expose_array_fault" not in stances:
            self.expose_pushes += 1
            ready = self._at_npc_or_move(
                session, "npc.cartographer_renke", "stay near Renke to commit fault exposure"
            )
            if ready is not True:
                return ready
            self.notes.append(f"push stance expose_array_fault #{self.expose_pushes}")
            variants = [
                "我要公开十二号接点故障，不能让冷却环裂缝被写成工人误触。",
                "负载曲线和镜图副本必须进入听证记录，镜阵故障要公开。",
                "如果轴承开裂是真相，就应该公布镜阵记录。"
            ]
            return f"对 cartographer_renke 说：{variants[min(self.expose_pushes - 1, len(variants) - 1)]}"

        # Confront the director with the evidence chain.
        if not bool(w.get("array_fault_disclosed")):
            ready = self._at_npc_or_move(
                session, "npc.director_alen", "return to director to disclose array fault"
            )
            if ready is not True:
                return ready
            self.director_disclosure_attempts += 1
            self.notes.append(f"request array fault disclosure #{self.director_disclosure_attempts}")
            if self.director_disclosure_attempts == 1:
                return (
                    "对 director_alen 说：证词已经保全，镜图副本也显示十二号接点早于换班偏斜。"
                    "请公开十二号接点故障，承认冷却环裂缝并公布镜阵记录。"
                )
            return (
                "对 director_alen 说：继续说证人记忆污染已经站不住脚。"
                "请说明事故真相，公布负载曲线，承认镜阵故障。"
            )

        # Optional public consequences after core truth route.
        if not bool(w.get("broadcast_retraction_issued")):
            ready = self._at_npc_or_move(
                session, "npc.broadcaster_iva", "move to broadcaster for retraction"
            )
            if ready is not True:
                return ready
            self.broadcast_attempts += 1
            self.notes.append(f"request broadcast retraction #{self.broadcast_attempts}")
            return (
                "对 broadcaster_iva 说：镜阵故障已经公开。"
                "请更正广播，撤回破镜派说法，停止污名化证人。"
            )

        if not bool(w.get("valley_heat_passes_released")):
            ready = self._at_npc_or_move(
                session, "npc.courier_tamsin", "move to valley platform for heat passes"
            )
            if ready is not True:
                return ready
            self.valley_attempts += 1
            self.notes.append(f"request valley heat passes #{self.valley_attempts}")
            return (
                "对 courier_tamsin 说：请发放热能通行证，释放低谷列车通行，"
                "给山谷家庭燃料和温棚优先权。"
            )

        self.done_waits += 1
        if self.done_waits <= 2:
            self.notes.append("wait for consequence drivers")
            return ""
        self.notes.append("all route goals complete")
        return "/quit"


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    backend = os.environ.get("PLAYTEST_LLM", "minimax")
    with OUT_PATH.open("w", buffering=1, encoding="utf-8") as out:
        def log(s: str = "") -> None:
            out.write(s + "\n")
            out.flush()

        log("=== Adaptive Skyglass Real Playtest ===")
        log(f"pack={PACK}")
        log(f"backend={backend}")
        log(f"MINIMAX_API_KEY={_redact_env_present('MINIMAX_API_KEY')}")
        log(f"OPENAI_API_KEY={_redact_env_present('OPENAI_API_KEY')}")
        log(f"max_steps={MAX_STEPS}")

        pack = CampaignLoader.load_from_file(PACK)
        validation = CampaignLoader.validate(pack)
        log("\n[LOAD/VALIDATE]")
        log(f"valid={validation.valid}")
        for issue in validation.issues:
            log(f"- [{issue.severity}] {issue.rule}: {issue.message}")
        if not validation.valid:
            log("RESULT: FAIL (content pack invalid)")
            return 1

        session = GameSession(PACK, save_dir="_playtest_saves", llm_backend=backend)
        session._progress_sink = lambda m: log(f"PROGRESS: {m}")
        session._stream_sink = lambda chunk: out.write(chunk)

        orig_parse = session.intent_parser.parse

        def parse_logged(raw_text: str, **kw: Any):
            result = orig_parse(raw_text, **kw)
            if isinstance(result, ParsedIntent):
                log(
                    "PARSE: "
                    f"type={result.intent_type.value} "
                    f"ref={result.target_ref!r}->id={result.target_id!r} "
                    f"content={(result.content or '')[:100]!r} "
                    f"mods={result.modifiers}"
                )
            else:
                log(
                    "PARSE: clarification "
                    f"type={getattr(result, 'ambiguity_type', '')!r} "
                    f"q={getattr(result, 'clarifying_question', '')!r}"
                )
            return result

        session.intent_parser.parse = parse_logged

        log("\n[A5 WORLD-BOOK VISIBILITY]")
        for eid in (
            "npc.director_alen", "npc.archivist_mae", "npc.clinician_oro",
            "npc.worker_lira", "npc.cartographer_renke", "npc.broadcaster_iva",
            "npc.courier_tamsin", "npc.greenhouse_sura",
        ):
            ent = session.world.state.get_entity(eid)
            visible = [
                e.entry_id for e in WorldBookFilter.filter_for_entity(
                    session.pack.world_book, ent
                )
            ]
            log(f"{eid}: {visible}")

        player = SkyglassPlayer()
        last_text = ""
        last_events: list[P.Event] = []

        for step in range(1, MAX_STEPS + 1):
            action = player.decide(session, last_text, last_events)
            if action == "/quit":
                log("\nPolicy decided goals are complete; stopping.")
                break

            state = session.world.state
            p = state.get_entity(PLAYER)
            loc = p.location_id if p else "?"
            present = [
                f"{eid}({ent.name})" for eid, ent in sorted(state.entities.items())
                if eid != PLAYER and ent.location_id == loc
            ]
            log("\n" + "=" * 72)
            log(f"STEP {step}")
            log(f"policy_note={player.notes[-1] if player.notes else ''}")
            log(
                f"pre: tick={state.tick} loc={loc} "
                f"world={dict(state.world_vars)} "
                f"stances={sorted(session.agenda_service.get_confirmed_stance_topics())}"
            )
            log(f"present={present}")
            log(f">>> {action!r}")

            events: list[P.Event] = []
            session._event_sink = events.append
            t0 = time.time()
            try:
                narrative = session.run_tick(action)
            except Exception:
                log("!! EXCEPTION")
                log(traceback.format_exc())
                session._event_sink = None
                return 1
            finally:
                session._event_sink = None
            dt = time.time() - t0

            p2 = session.world.state.get_entity(PLAYER)
            loc2 = p2.location_id if p2 else "?"
            log(
                f"post: tick={session.world.state.tick} loc={loc2} "
                f"world={dict(session.world.state.world_vars)} "
                f"stances={sorted(session.agenda_service.get_confirmed_stance_topics())} "
                f"elapsed={dt:.1f}s"
            )
            log("narrative:")
            log(narrative if narrative and narrative.strip() else "<empty>")
            compact_events = [e for e in events if not isinstance(e, P.SpeechToken)]
            log(
                f"protocol_events={len(compact_events)} "
                f"(+{len(events) - len(compact_events)} speech tokens)"
            )
            for ev in compact_events:
                log(_event_summary(ev))

            current_pressures = _pressure_events(session)
            if len(current_pressures) > player.last_pressure_count:
                log("new_pressure_events:")
                for pe in current_pressures[player.last_pressure_count:]:
                    log(repr(pe))
                player.last_pressure_count = len(current_pressures)

            last_text = _observed_text(narrative or "", events)
            last_events = events

        log("\n[FINAL SUMMARY]")
        log(f"tick={session.world.state.tick}")
        log(f"world={dict(session.world.state.world_vars)}")
        log(f"stances={sorted(session.agenda_service.get_confirmed_stance_topics())}")
        log("pressure_events:")
        for pe in _pressure_events(session):
            log(repr(pe))

        checks = {
            "protect_witness_memory_stance": (
                "protect_witness_memory"
                in session.agenda_service.get_confirmed_stance_topics()
            ),
            "secure_worker_record_stance": (
                "secure_worker_record"
                in session.agenda_service.get_confirmed_stance_topics()
            ),
            "expose_array_fault_stance": (
                "expose_array_fault"
                in session.agenda_service.get_confirmed_stance_topics()
            ),
            "archive_injunction_filed": (
                session.get_world_var("archive_injunction_filed") is True
            ),
            "witness_record_secured": (
                session.get_world_var("witness_record_secured") is True
            ),
            "memory_purge_halted": (
                session.get_world_var("memory_purge_halted") is True
            ),
            "cartography_copy_obtained": (
                session.get_world_var("cartography_copy_obtained") is True
            ),
            "array_fault_disclosed": (
                session.get_world_var("array_fault_disclosed") is True
            ),
            "smear_driver_seen": any(
                pe["driver_id"] == "directorate_smear_response"
                for pe in _pressure_events(session)
            ),
            "deadline_driver_seen": any(
                pe["driver_id"] == "silent_bell_countdown"
                for pe in _pressure_events(session)
            ),
            "array_fault_pressure_seen": any(
                pe["driver_id"] == "array_fault_worsens"
                for pe in _pressure_events(session)
            ),
        }
        log("checks:")
        for key, value in checks.items():
            log(f"- {key}: {'PASS' if value else 'FAIL'}")

        if all(checks.values()):
            log("RESULT: PASS")
        else:
            log("RESULT: INCOMPLETE_OR_FAIL")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
