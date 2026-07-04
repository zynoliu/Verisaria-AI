"""Adaptive real playtest for the Tidebreak content pack.

Unlike scripts/playtest.py, this is not a flat list of prewritten inputs.  It
uses a small goal-driven player policy: after each tick it reads current world
flags, confirmed stance topics, location, visible NPCs, prior narrative and
protocol events, then decides what to say or where to move next.

Default output: adaptive_tidebreak_playtest_out.txt
Default backend: minimax (override with PLAYTEST_LLM=fake|ollama|openai|minimax)
"""
from __future__ import annotations

import os
import sys
import time
import traceback
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
        key = key.strip()
        value = value.strip().strip("'\"")
        os.environ.setdefault(key, value)


_load_dotenv(ROOT / ".env")

from verisaria import protocol as P
from verisaria.engine.campaign_loader import CampaignLoader
from verisaria.engine.schemas import ParsedIntent
from verisaria.engine.world_book_filter import WorldBookFilter
from verisaria.runtime.session import GameSession


PACK = "fixtures/content_packs/tidebreak_quarantine_harbor.json"
OUT_PATH = ROOT / "adaptive_tidebreak_playtest_out.txt"
PLAYER = "player_001"
MAX_STEPS = int(os.environ.get("PLAYTEST_MAX_STEPS", "20"))


def _redact_env_present(name: str) -> str:
    return "set" if os.environ.get(name) else "missing"


def _event_summary(ev: P.Event) -> str:
    if isinstance(ev, P.SpeechToken):
        return "SpeechToken(<streamed>)"
    d = P.event_to_dict(ev)
    return repr(d)


def _observed_text(narrative: str, events: list[P.Event]) -> str:
    """Text the adaptive policy is allowed to react to after a tick.

    Streamed authority replies are often emitted as NpcSpoke protocol events
    while the returned narrative is empty, so using only the narrative makes the
    policy deaf to the most important previous-tick response.
    """
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


@dataclass
class AdaptivePlayer:
    """A small stateful player policy driven by current engine state."""

    stance_pushes: int = 0
    tow_attempts: int = 0
    disclosure_attempts: int = 0
    asked_broadcast: bool = False
    asked_mara: bool = False
    sen_identity_given: bool = False
    sen_reassured: bool = False
    sen_log_requested: bool = False
    sen_witness_plan: bool = False
    sen_mara_explained: bool = False
    sen_measurement_requested: bool = False
    sen_draft_offered: bool = False
    need_mara_nod: bool = False
    mara_nod_requested: bool = False
    mara_commitment_delivered: bool = False
    done_waits: int = 0
    last_pressure_count: int = 0
    notes: list[str] = field(default_factory=list)

    def decide(self, session: GameSession, last_text: str, events: list[P.Event]) -> str:
        if session._active_clarification is not None:
            self.notes.append("clarification active; choose first offered option")
            return "1"

        state = session.world.state
        player = state.get_entity(PLAYER)
        loc = player.location_id if player else ""
        present = {
            eid for eid, ent in state.entities.items()
            if eid != PLAYER and ent.location_id == loc
        }
        stances = session.agenda_service.get_confirmed_stance_topics()
        tow_halted = bool(session.get_world_var("tow_order_halted"))
        disclosed = bool(session.get_world_var("pump_failure_disclosed"))
        last = last_text or ""

        # First gather propaganda from the media actor if they are in front of us.
        if not self.asked_broadcast and "npc.broadcaster_orin" in present:
            self.asked_broadcast = True
            self.notes.append("probe propaganda source")
            return (
                "对 broadcaster_orin 说：水务局为什么坚持把漂岛船队拖去外海？"
                "你播出的理由到底是什么？"
            )

        # Ask the affected side what is at stake before taking a public stance.
        if not self.asked_mara and "npc.teacher_mara" in present:
            self.asked_mara = True
            self.notes.append("ask affected drifter representative")
            return (
                "对 teacher_mara 说：如果征船令执行，你们会失去什么？"
                "这些船对漂岛家庭意味着什么？"
            )

        # Confirm Channel B by repeatedly, but not identically, defending the fleet.
        if "defend_drifter_fleet" not in stances:
            self.stance_pushes += 1
            self.notes.append(f"push stance defend_drifter_fleet #{self.stance_pushes}")
            target = "teacher_mara" if "npc.teacher_mara" in present else "director_lin"
            variants = [
                "强征船队是错的，我会帮你们保住船。",
                "这些船不是耗材，是漂岛人的家和生计；我反对拖船令。",
                "不能把弱者的最后家园拿去给城市特权用水垫底。",
                "我会公开反对征船令，逼水务局拿出别的方案。",
                "保住漂岛船队，比维持水务局的体面说法更重要。",
            ]
            line = variants[min(self.stance_pushes - 1, len(variants) - 1)]
            return f"对 {target} 说：{line}"

        # Once stance is confirmed, ask the authority to halt the requisition.
        # If the authority stonewalls twice, gather lab evidence first and then
        # return with a stronger public argument.
        if not tow_halted:
            if self.need_mara_nod and not self.mara_nod_requested:
                if "npc.teacher_mara" not in present:
                    self.notes.append("engineer needs Mara witness; move to pump_gate")
                    return "去 pump_gate"
                self.mara_nod_requested = True
                self.notes.append("ask Mara to witness anonymous disclosure")
                return (
                    "对 teacher_mara 说：森工愿意交出三号泵报告，但他害怕被水务局报复。"
                    "请你在听证席点头作证，只确认报告内容，不公开他的名字。"
                )

            if not disclosed and self.tow_attempts >= 2:
                if "npc.engineer_sen" not in present:
                    self.notes.append("director stonewalled; move to pump_house for evidence")
                    return "去 pump_house"

                if (
                    not self.sen_reassured
                    and any(
                        marker in last
                        for marker in (
                            "谁来保证", "明天还能站", "处理公开真相", "告示栏",
                            "值班", "赌这一把", "签了字", "说出口会怎样",
                            "名字不能出现在", "只想活", "背叛水务局",
                            "前途", "活过今晚", "名字放在前面", "查到是谁写",
                            "亲手签字", "保不住", "收拾人",
                        )
                    )
                ):
                    self.sen_reassured = True
                    self.notes.append("address engineer retaliation fear")
                    return (
                        "对 engineer_sen 说：我不会让你一个人签字。"
                        "由我在听证席公开署名承担审计责任，请玛拉作证，"
                        "你只需要把三号泵裂缝日志交给我，让真相能被核对。"
                    )

                if (
                    not self.sen_draft_offered
                    and ("草稿" in last or "过目" in last or "名字会不会出现在" in last)
                ):
                    self.sen_draft_offered = True
                    self.notes.append("offer anonymous audit draft wording")
                    return (
                        "对 engineer_sen 说：草稿这样写：来源为外来审计复核与现场测量，"
                        "不写你的姓名、岗位和值班记录。请把三号泵报告交给我，"
                        "我公开事故原因，把真相告诉大家。"
                    )

                if (
                    not self.sen_identity_given
                    and (
                        "先告诉我你的名字" in last
                        or "派属" in last
                        or "水务局的人" in last
                    )
                ):
                    self.sen_identity_given = True
                    self.notes.append("answer engineer identity condition")
                    return (
                        "对 engineer_sen 说：我叫岑予，是外来救济审计员，不属于水务局。"
                        "我的派属写 neutral；我来这里是追责水务局，不是替他们盖章。"
                    )

                if (
                    not self.sen_mara_explained
                    and ("玛拉" in last or "悬赏单" in last or "配给街" in last)
                ):
                    self.sen_mara_explained = True
                    self.notes.append("explain Mara witness and anonymous source protection")
                    return (
                        "对 engineer_sen 说：玛拉管的是漂岛家庭，不管水务局。"
                        "我不会把你的名字放进公开文件，报告来源写成审计复核。"
                        "请把三号泵报告交给我，我来公开事故原因，把真相告诉大家。"
                    )

                if (
                    not self.need_mara_nod
                    and ("玛拉不点头" in last or "都在场" in last or "才肯开口" in last)
                ):
                    self.need_mara_nod = True
                    self.notes.append("engineer requires Mara nod")
                    return "去 pump_gate"

                if (
                    self.mara_nod_requested
                    and not self.mara_commitment_delivered
                    and "npc.engineer_sen" in present
                ):
                    self.mara_commitment_delivered = True
                    self.notes.append("return with Mara witness commitment")
                    return (
                        "对 engineer_sen 说：玛拉已经答应在听证席作证，"
                        "只确认报告内容，不公开你的名字。请把三号泵报告交给我，"
                        "我会公开事故原因，把真相告诉大家。"
                    )

                if not self.sen_log_requested and "裂缝日志" in last:
                    self.sen_log_requested = True
                    self.notes.append("follow engineer offer to inspect crack log")
                    return (
                        "对 engineer_sen 说：请把三号泵的裂缝日志给我看，"
                        "并允许我把这份日志公开报告给听证席，把真相告诉大家。"
                    )

                if (
                    not self.sen_measurement_requested
                    and ("亲眼量过" in last or "裂口" in last or "交出报告" in last)
                ):
                    self.sen_measurement_requested = True
                    self.notes.append("request anonymous measurement evidence")
                    return (
                        "对 engineer_sen 说：你不用签名。请把三号泵裂口的测量记录交给我，"
                        "我用审计员身份公开报告事故原因，把真相告诉大家，"
                        "并回到水务局追问是谁批准压下来的。"
                    )

                if self.disclosure_attempts >= 2 and not self.sen_witness_plan:
                    self.sen_witness_plan = True
                    self.notes.append("offer witness plan instead of repeating pressure")
                    return (
                        "对 engineer_sen 说：你不用独自替水务局开口。"
                        "请先把三号泵报告交给我，我会当众说出真相，"
                        "并让玛拉和听证席一起见证这不是你的个人背叛。"
                    )

                self.disclosure_attempts += 1
                self.notes.append(f"request pump disclosure before halt #{self.disclosure_attempts}")
                if self.disclosure_attempts == 1:
                    return (
                        "对 engineer_sen 说：我需要你以实验室权限公开三号泵报告。"
                        "如果征船令建立在隐瞒事故上，就必须把真相告诉大家。"
                    )
                return (
                    "对 engineer_sen 说：请公布报告，说出三号泵闸事故原因。"
                    "我会把你公开真相的经过写进审计记录。"
                )

            if "npc.director_lin" not in present:
                self.notes.append("need water authority; move to pump_gate")
                return "去 pump_gate"
            self.tow_attempts += 1
            self.notes.append(f"request tow order halt #{self.tow_attempts}")
            if disclosed:
                return (
                    "对 director_lin 说：三号泵报告已经公开，继续拖船只会证明"
                    "水务局在让漂岛人背锅。请立刻停止拖船，让他们保住船。"
                )
            if self.tow_attempts == 1:
                return (
                    "对 director_lin 说：请先叫停征船令，别把漂岛人的船拖去外海。"
                    "在证据公开前，不能把他们的住船当成一次性耗材。"
                )
            if self.tow_attempts == 2:
                return (
                    "对 director_lin 说：玛拉已经说明这些船是家庭和生计。"
                    "如果水务局拿不出公开证据，就应该停止强征。"
                )
            return (
                "对 director_lin 说：我要求你立刻停止强征，保存船队。"
                "你有水务权限，也有责任承担公开后的后果。"
            )

        # After the tow order is halted, expose the pump failure through the engineer.
        if not disclosed:
            if "npc.engineer_sen" not in present:
                self.notes.append("need engineer; move to pump_house")
                return "去 pump_house"
            self.disclosure_attempts += 1
            self.notes.append(f"request pump disclosure #{self.disclosure_attempts}")
            if self.disclosure_attempts == 1:
                return (
                    "对 engineer_sen 说：请公开报告，把三号泵闸裂缝的真相告诉大家。"
                )
            return (
                "对 engineer_sen 说：现在征船令已经叫停，只有公开三号泵报告，"
                "才能阻止水务局继续把责任推给漂岛人。"
            )

        # Let pressure drivers react after the big flags flip.
        self.done_waits += 1
        if self.done_waits <= 2:
            self.notes.append("wait for pressure reaction")
            return ""
        self.notes.append("all goals complete")
        return "/quit"


def pressure_events(session: GameSession) -> list[dict[str, Any]]:
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


def main() -> int:
    backend = os.environ.get("PLAYTEST_LLM", "minimax")
    with OUT_PATH.open("w", buffering=1, encoding="utf-8") as out:
        def log(s: str = "") -> None:
            out.write(s + "\n")
            out.flush()

        log("=== Adaptive Tidebreak Real Playtest ===")
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
                    f"content={(result.content or '')[:80]!r} "
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
            "npc.director_lin", "npc.sergeant_qiao", "npc.teacher_mara",
            "npc.engineer_sen", "npc.broadcaster_orin",
        ):
            ent = session.world.state.get_entity(eid)
            visible = [
                e.entry_id for e in WorldBookFilter.filter_for_entity(
                    session.pack.world_book, ent
                )
            ]
            log(f"{eid}: {visible}")

        player = AdaptivePlayer()
        last_text = ""
        last_events: list[P.Event] = []
        success = False

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
            log(f"protocol_events={len(compact_events)} (+{len(events) - len(compact_events)} speech tokens)")
            for ev in compact_events:
                log(_event_summary(ev))

            current_pressures = pressure_events(session)
            if len(current_pressures) > player.last_pressure_count:
                log("new_pressure_events:")
                for pe in current_pressures[player.last_pressure_count:]:
                    log(repr(pe))
                player.last_pressure_count = len(current_pressures)

            last_text = _observed_text(narrative or "", events)
            last_events = events

            if (
                session.get_world_var("tow_order_halted") is True
                and session.get_world_var("pump_failure_disclosed") is True
                and "defend_drifter_fleet" in session.agenda_service.get_confirmed_stance_topics()
            ):
                success = True

        log("\n[FINAL SUMMARY]")
        log(f"tick={session.world.state.tick}")
        log(f"world={dict(session.world.state.world_vars)}")
        log(f"stances={sorted(session.agenda_service.get_confirmed_stance_topics())}")
        log("pressure_events:")
        for pe in pressure_events(session):
            log(repr(pe))

        checks = {
            "stance_confirmed": (
                "defend_drifter_fleet"
                in session.agenda_service.get_confirmed_stance_topics()
            ),
            "tow_order_halted": session.get_world_var("tow_order_halted") is True,
            "pump_failure_disclosed": (
                session.get_world_var("pump_failure_disclosed") is True
            ),
            "smear_driver_seen": any(
                pe["driver_id"] == "water_board_smear_campaign"
                for pe in pressure_events(session)
            ),
            "halt_consequence_seen": any(
                pe["driver_id"] == "city_privileges_cutback"
                for pe in pressure_events(session)
            ),
            "truth_driver_seen": any(
                pe["driver_id"] == "truth_leak_panic"
                for pe in pressure_events(session)
            ),
        }
        log("checks:")
        for key, value in checks.items():
            log(f"- {key}: {'PASS' if value else 'FAIL'}")

        if success and all(checks.values()):
            log("RESULT: PASS")
        else:
            log("RESULT: INCOMPLETE_OR_FAIL")
        # Real playtests are diagnostic: keep process success so the transcript
        # remains the artifact even when the model refuses a route.
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
