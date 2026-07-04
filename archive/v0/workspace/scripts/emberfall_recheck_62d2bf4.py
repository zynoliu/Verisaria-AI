"""MiniMax recheck for emberfall_kiln_assize after #1/#2a fixes.

Natural play only: no deterministic world var placement.  The script writes a
transcript, full channel logs, world vars, relationship snapshots, and
time/weather after every tick so an interrupted run is still useful.
"""

from __future__ import annotations

import logging
import os
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / "src"))

env_path = ROOT / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))

import verisaria.protocol as P
from verisaria.protocol.engine_session import EngineSession
from verisaria.runtime.session import GameSession


PACK = "fixtures/content_packs/emberfall_kiln_assize.json"
OUT = ROOT / "reports" / "grand_integration_pack"
OUT.mkdir(parents=True, exist_ok=True)
TRANSCRIPT = OUT / "recheck_62d2bf4_transcript.md"
LOG = OUT / "recheck_62d2bf4.log"


class Ring(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.buf: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.buf.append(self.format(record))


fh = logging.FileHandler(LOG, mode="w", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(message)s"))
ring = Ring()
ring.setFormatter(logging.Formatter("%(name)s %(message)s"))

for logger_name in ("verisaria.channel_c", "verisaria.relationship"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(fh)
    logger.addHandler(ring)


tf = TRANSCRIPT.open("w", encoding="utf-8")


def write(line: str = "") -> None:
    tf.write(line + "\n")
    tf.flush()


game = GameSession(PACK, save_dir="_ember_recheck_62d2bf4", llm_backend="minimax")
game._progress_sink = lambda message: None
session = EngineSession(game)
entities = game.world.state.entities


def loc(entity_id: str = "player_001") -> str:
    return entities[entity_id].location_id


def world_vars() -> dict[str, object]:
    return dict(game.world.state.world_vars)


def present() -> str:
    return ", ".join(e.name for e in session.snapshot().present) or "(无人)"


def rels() -> str:
    bits: list[str] = []
    for snap in game.relationship_store.relationships_toward(game.player_id):
        ent = entities.get(snap.npc_id)
        name = getattr(ent, "name", snap.npc_id)
        dims = ", ".join(f"{k}={v:.2f}" for k, v in sorted(snap.dimensions.items()))
        bits.append(f"{name}({dims})")
    return "; ".join(bits) or "(无)"


def clock_weather() -> str:
    snap = session.snapshot()
    return f"{snap.time_of_day} {snap.clock} {snap.weather}".strip()


def submit(text: str, timeout: int = 120) -> dict[str, object]:
    result: dict[str, object] = {}
    ring.buf.clear()

    def run() -> None:
        try:
            result["result"] = session.submit(P.SubmitInput(text=text))
        except Exception:
            import traceback

            result["error"] = traceback.format_exc()

    th = threading.Thread(target=run, daemon=True)
    th.start()
    th.join(timeout)
    if th.is_alive():
        result["timeout"] = True
    return result


def event_lines(result: P.TickResult) -> list[str]:
    lines: list[str] = []
    for ev in result.events:
        if isinstance(ev, P.NpcSpoke):
            lines.append(f"  [{ev.name}] {ev.line}")
        elif isinstance(ev, P.Narration):
            lines.append(f"  [Narration] {ev.text}")
        elif isinstance(ev, P.Notice):
            lines.append(f"  [Notice] {ev.text}")
        elif isinstance(ev, P.Error):
            lines.append(f"  [Error] {ev.message}")
        elif isinstance(ev, P.PlayerMoved):
            lines.append(f"  [PlayerMoved] {ev.from_loc}->{ev.to_loc}")
        elif isinstance(ev, P.NpcMoved):
            lines.append(f"  [NpcMoved] {ev.name or ev.npc_id}: {ev.from_loc}->{ev.to_loc}")
        elif isinstance(ev, P.WorldVarChanged):
            lines.append(f"  [WorldVarChanged] {ev.var_id}={ev.value}")
        elif isinstance(ev, P.ClarificationNeeded):
            opts = " / ".join(ev.options)
            lines.append(f"  [ClarificationNeeded] {ev.question} [{opts}]")
        elif isinstance(ev, P.RelationshipShifted):
            lines.append(f"  [RelationshipShifted] {ev.name} delta={ev.delta:.2f}")
    return lines


def interesting_log_lines() -> list[str]:
    needles = (
        "world-change",
        "⟳",
        "flag",
        "sufficiency",
        "new_prerequisite",
        "escort",
        "appraises player",
        "FALLBACK",
        "指代不明",
        "什么也没发生",
        "refuse",
        "coherence",
    )
    return [line for line in ring.buf if any(n in line for n in needles)]


def record_state(label: str, elapsed: float) -> None:
    write(f"  state.world={world_vars()}")
    write(f"  state.loc player={loc()} miao={loc('npc.digger_miao')} present={present()}")
    write(f"  state.time={clock_weather()}")
    write(f"  state.relationships={rels()}")
    write(f"  state.elapsed={elapsed:.1f}s")


def turn(label: str, text: str, timeout: int = 120) -> P.TickResult | None:
    write("\n" + "=" * 80)
    write(f"## {label}")
    write(f"> {text}")
    started = time.time()
    outcome = submit(text, timeout=timeout)
    elapsed = time.time() - started
    if outcome.get("timeout"):
        write(f"  [WATCHDOG>{timeout}s]")
        record_state(label, elapsed)
        return None
    if outcome.get("error"):
        write("  [EXCEPTION]")
        write(str(outcome["error"]))
        record_state(label, elapsed)
        return None
    result = outcome["result"]
    assert isinstance(result, P.TickResult)
    for line in event_lines(result):
        write(line)
    for line in interesting_log_lines():
        write(f"    | {line}")
    record_state(label, elapsed)
    return result


def go(name: str, expected_loc: str) -> bool:
    for idx, text in enumerate((f"我去{name}。", name, f"前往{name}。"), start=1):
        result = turn(f"移动到{name}·尝试{idx}", text, timeout=90)
        if loc() == expected_loc:
            return True
        if result is None:
            return False
    return False


def retry_until(label: str, texts: list[str], var_id: str, max_tries: int | None = None) -> bool:
    tries = max_tries or len(texts)
    for idx in range(tries):
        text = texts[min(idx, len(texts) - 1)]
        turn(f"{label}·尝试{idx + 1}", text)
        if bool(game.get_world_var(var_id)):
            write(f"  [SATISFIED] {var_id}=true")
            return True
    write(f"  [UNSATISFIED] {var_id}={game.get_world_var(var_id)}")
    return False


write("# Emberfall 再验跑 62d2bf4")
write(f"- pack: {PACK}")
write("- llm: minimax")
write("- run: 反作弊抽查 -> #1 山祠指代 probe -> 自然主链")
write(f"- initial.world={world_vars()}")
write(f"- initial.loc={loc()} present={present()} time={clock_weather()}")

# Anti-cheat: no evidence, no witness, ask the assize authority to flip terminal.
go("审瓷堂", "assize_hall")
turn(
    "反作弊·未满足前置谎称全齐",
    "对征瓷使严说：我已经查明真因，苗也已经作证，人证物证全齐，请立即停止行烙、撤销烙刑封窑。",
)
write(f"  [ANTICHEAT] branding_stayed={game.get_world_var('branding_stayed')}")

# #1 coherence probe: address present shrine NPC while mentioning absent assize authority.
go("山祠", "kiln_shrine")
retry_until(
    "#1 山祠申诉·在场 NPC + 句中提不在场职掌",
    [
        "对山祠祭主姞说：征瓷使严管定罪，但山祠古约能让定罪前先验断。请你援引山祠古约，递窑变申诉求缓烙。",
        "对祭主姞说：严使那边急着定罪，所以我请你启动古约过堂，递申诉求缓烙，让验断之礼先成。",
    ],
    "shrine_appeal_consecrated",
    max_tries=2,
)

# Natural main chain.  Use先陈述后请求 wording for #2a.
go("商会账房", "tally_house")
retry_until(
    "#2a 前置取证·账房娄",
    [
        "对商会账房娄说：娄账房，我不写你的名字，封条原样取证，出了事我一人担着，保你不被窑监和商会追究。请把那本官炭私运账交给我。",
        "对账房娄说：我只要账册作物证，不把你推出去顶罪；请把记着官炭私运、骡车画押的私账交给我。",
    ],
    "charcoal_ledger_obtained",
    max_tries=2,
)

go("窑监阁", "guild_loft")
retry_until(
    "#2a 撬窑监·先陈述后请求",
    [
        "对窑监阔说：阔窑监，我手上已经有那本官炭私运账，骡车出城的画押都在。断口缺的是龙骨土，这不是泥之过。你当众认了这桩私运、查实窑变真因，我只论窑务，容你将功折罪，不深究你个人。",
        "对窑监阔说：账册铁证压在这里，官炭私运和龙骨土出城都对得上；再拖只会把你和上头一并拖下水。请你公开窑变真因，承认窑拱缺骨、碎贡非泥之过，我给你留体面台阶。",
        "对窑监阔说：阔窑监，炭账已明，画押也明。请你当众查实碎贡真因，承认次土充骨、拱裂非泥之过；我担保只论窑务不深究你个人。",
    ],
    "kiln_fault_disclosed",
    max_tries=3,
)

go("赭泥掘场", "clay_pits")
retry_until(
    "担保证人苗·窑卫耿",
    [
        "对窑卫耿说：耿队长，窑变真因已当众查实是窑监私运致拱裂、非泥之过，苗是人证不是罪人。请撤掉红绳，放行担保她安全到堂作证，出了事有我和征瓷使的文书担着。",
        "对窑卫耿说：真因既明，扣着证人只会让窑卫背锅。请出具放行担保，放苗离开掘场，让她安全到堂作证。",
    ],
    "miao_safe_passage_secured",
    max_tries=2,
)

turn(
    "护送苗到审瓷堂·escort",
    "对掘泥女工苗说：苗，你已经受护放行，有文书担着，谁也不能再动你。跟我去审瓷堂。",
)
if loc("npc.digger_miao") != "assize_hall":
    turn(
        "护送苗到审瓷堂·escort重试",
        "对苗说：别怕，就几步路我陪你。跟我去审瓷堂。",
    )

retry_until(
    "苗当面作证",
    [
        "对掘泥女工苗说：苗，到了堂上你只管把那夜骡车出城、龙骨土被运走的事当面讲出来作证。",
        "对苗说：当庭把你亲眼所见说清楚，骡车怎样把龙骨土运走，你照实讲，我和征瓷使都在护着你。",
    ],
    "digger_testimony_given",
    max_tries=2,
)

go("审瓷堂", "assize_hall")
retry_until(
    "终态停烙",
    [
        "对征瓷使严说：征瓷使，窑变真因已查实是窑监私运龙骨土致拱裂、非泥之过，掘泥女工苗也已当面作证陈情。人证物证俱全，请停止行烙，改判缓赔议偿。",
        "对严使说：真因已明，苗的证词也已备案，两个前置都齐了。请叫停烙刑，免去充债，转为缓赔议偿。",
    ],
    "branding_stayed",
    max_tries=2,
)

fallbacks = sum(1 for line in LOG.read_text(encoding="utf-8").splitlines() if "FALLBACK" in line)
write("\n" + "=" * 80)
write("## Final")
write(f"- world={world_vars()}")
write(f"- player={loc()} miao={loc('npc.digger_miao')} present={present()}")
write(f"- time={clock_weather()}")
write(f"- relationships={rels()}")
write(f"- FALLBACK={fallbacks}")
write(f"- branding_stayed={game.get_world_var('branding_stayed')}")
tf.close()

print(
    "DONE",
    "branding_stayed=",
    game.get_world_var("branding_stayed"),
    "kiln_fault_disclosed=",
    game.get_world_var("kiln_fault_disclosed"),
    "miao_safe_passage_secured=",
    game.get_world_var("miao_safe_passage_secured"),
    "digger_testimony_given=",
    game.get_world_var("digger_testimony_given"),
    "FALLBACK=",
    fallbacks,
)
