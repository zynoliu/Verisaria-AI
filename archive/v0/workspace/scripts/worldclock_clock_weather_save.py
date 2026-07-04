"""Scenario 3 — clock variable-rate + weather drift + save/load replay (SECONDARY).

Runs a longer session on a climate-declared pack to observe:
  - clock variable rate: conversation/combat ticks are a few minutes, quiet /skip
    ticks are ~half-hour-scale.
  - weather: slow drift inside the climate ladder, no jumps (温带 never snows).
  - save/load: clock + weather restore identically; weather is replayable (a fresh
    session advanced to the same world hour lands on the same sky — pack-id+hour
    seed).

Uses frostgate (寒带) for a long fast-forward weather series, plus an in-memory
温带 variant of the escort pack to confirm climate-gating (no snow in 温带). The
committed fixtures stay byte-identical (climate/opening injected in-memory only).

Real MiniMax. 90s/tick watchdog + 55s socket.
"""
from __future__ import annotations
import os, sys, time, json, logging, threading, tempfile
from pathlib import Path

ROOT = Path("/Users/gensliu/Documents/rpg")
os.chdir(ROOT); sys.path.insert(0, str(ROOT / "src"))
for raw in (ROOT / ".env").read_text().splitlines():
    line = raw.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip("'\""))

import verisaria.protocol as P
from verisaria.protocol.engine_session import EngineSession
from verisaria.engine import weather as weather_mod

OUTDIR = ROOT / "reports" / "worldclock_weather_test"
OUTDIR.mkdir(parents=True, exist_ok=True)
LOGFILE = str(OUTDIR / "clock_weather_save.log")
RAWOUT = OUTDIR / "clock_weather_save_raw.txt"
PER_TICK_TIMEOUT = float(os.environ.get("PQ_TICK_TIMEOUT", "90"))
SOCK_TIMEOUT = float(os.environ.get("PQ_SOCK_TIMEOUT", "55"))

h = logging.FileHandler(LOGFILE, mode="w", encoding="utf-8")
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
lg = logging.getLogger("verisaria"); lg.setLevel(logging.INFO); lg.addHandler(h)
out = RAWOUT.open("w", buffering=1, encoding="utf-8")
def log(s=""): out.write(s + "\n"); out.flush()

timeouts = 0; fallbacks = 0
PLAYER = "player_001"

def pack_variant(src, **premise):
    p = json.loads((ROOT / "fixtures" / "content_packs" / src).read_text())
    p["world_premise"].update(premise)
    tmp = Path(tempfile.mkdtemp()) / src
    tmp.write_text(json.dumps(p, ensure_ascii=False))
    return str(tmp)

def _watch(fn):
    res = {"v": None, "exc": None, "done": False}
    def _w():
        try: res["v"] = fn()
        except Exception:
            import traceback; res["exc"] = traceback.format_exc()
        finally: res["done"] = True
    t0 = time.time(); w = threading.Thread(target=_w, daemon=True)
    w.start(); w.join(PER_TICK_TIMEOUT); return res, time.time() - t0

clock_deltas = []  # (label, kind, before_min, after_min, delta, weather)

def do(s, fn, label, kind):
    global timeouts
    before = s.game.world.state.clock_minutes
    res, dt = _watch(fn)
    if not res["done"]:
        log(f"!! TIMEOUT {label} {dt:.1f}s"); timeouts += 1; return None
    if res["exc"]: log("!! EXC\n" + res["exc"]); return None
    snap = s.snapshot(); after = s.game.world.state.clock_minutes
    d = after - before
    clock_deltas.append((label, kind, before, after, d, snap.weather))
    log(f"  [{kind}] {label}: clock {before}->{after} (+{d}min) | {snap.time_of_day} {snap.clock} | 天气 {snap.weather} | {dt:.1f}s")
    return snap

def main():
    global timeouts
    log("=== SCENARIO 3: clock rate + weather + save/load ===")

    # ---- PART A: variable-rate clock on a conversation pack (温带 escort) ----
    log("\n## PART A — clock variable rate (温带 escort, opening 上午)")
    pa = pack_variant("escort_proving_ground.json", climate="温带", opening_time="上午")
    s = EngineSession.start(pa, save_dir="_wc_s3a", llm_backend="minimax")
    try: s.game.llm_provider.timeout = SOCK_TIMEOUT
    except Exception: pass
    log(f"START {s.snapshot().clock} {s.snapshot().time_of_day} 天气 {s.snapshot().weather} climate=温带")
    # conversation beats (SLOW ≈ 3min each)
    for line in [
        "对闸官老康说：老康，今天上游的水情怎么样？",
        "对闸官老康说：下游的磨坊和田地都等着水，你看这闸能不能想想办法？",
        "对闸官老康说：我明白你的难处，你要的亲历者我这就去找。",
    ]:
        do(s, lambda l=line: s.submit(P.SubmitInput(text=l)), label=line[:18], kind="对话SLOW")
    # an empty wait (held to 1 step)
    do(s, lambda: s.submit(P.Wait()), label="/wait一拍", kind="WAIT")
    # go to the empty yard then /skip fast-forward (FAST ≈ 30min/step)
    do(s, lambda: s.submit(P.SubmitInput(text="去院子")), label="去院子(移动)", kind="移动")
    do(s, lambda: s.game._handle_command("/skip"), label="/skip空地快进", kind="SKIP-FAST")
    do(s, lambda: s.game._handle_command("/skip"), label="/skip空地快进2", kind="SKIP-FAST")
    log("\n温带天气序列 (应只在 晴/多云/阴/小雨/雨 内, 无雪):")
    a_wx = [w for *_ , w in clock_deltas]
    for lbl, knd, b, a, d, w in clock_deltas:
        log(f"   {lbl} -> {w}")
    has_snow_A = any("雪" in (w or "") for *_, w in clock_deltas)
    log(f"   温带含雪? {has_snow_A}  (应为 False)")

    # ---- PART B: long weather series + save/load round-trip (寒带 frostgate) ----
    log("\n## PART B — long weather drift + save/load (寒带 frostgate, opening 清晨)")
    pb = pack_variant("frostgate_watchpost.json", climate="寒带", opening_time="清晨", npc_daily_rhythm=True)
    s2 = EngineSession.start(pb, save_dir="_wc_s3b", llm_backend="minimax")
    try: s2.game.llm_provider.timeout = SOCK_TIMEOUT
    except Exception: pass
    g2 = s2.game
    # walk alone to refugee_camp so /skip can fast-forward
    do(s2, lambda: s2.submit(P.SubmitInput(text="去难民营")), label="去难民营", kind="移动")
    series = []
    for i in range(6):
        do(s2, lambda: g2._handle_command("/skip"), label=f"/skip#{i}", kind="SKIP-FAST")
        series.append((g2.world.state.clock_minutes, g2.world.state.weather))
    log("\n寒带长天气序列 (clock_min, weather):")
    for cm, w in series:
        from verisaria.engine import worldclock as _wc
        log(f"   {_wc.clock_label(cm)} -> {weather_mod.weather_label(w)} ({w})")
    has_thunder = any("雷" in (w or "") for _, w in series)
    log(f"   寒带含雷雨? {has_thunder} (应为 False)")

    # SAVE here
    saved_clock = g2.world.state.clock_minutes
    saved_weather = g2.world.state.weather
    saved_whour = g2.world.state.weather_hour
    save_ret = g2._handle_command("/save")
    save_id = str(save_ret).split("Saved:")[-1].strip()
    log(f"\nSAVED id={save_id} | clock={saved_clock} weather={saved_weather} weather_hour={saved_whour}")

    # mutate: skip more, weather/clock change
    do(s2, lambda: g2._handle_command("/skip"), label="/skip(存档后继续)", kind="SKIP-FAST")
    after_clock = g2.world.state.clock_minutes; after_weather = g2.world.state.weather
    log(f"after extra skip: clock={after_clock} weather={after_weather} (应与存档不同)")

    # LOAD back
    load_ret = g2._handle_command(f"/load {save_id}")
    lc = g2.world.state.clock_minutes; lw = g2.world.state.weather; lwh = g2.world.state.weather_hour
    log(f"LOADED: clock={lc} weather={lw} weather_hour={lwh}  ret={str(load_ret)[:60]}")
    clock_ok = (lc == saved_clock); weather_ok = (lw == saved_weather and lwh == saved_whour)
    log(f"  存档一致: clock_match={clock_ok}  weather_match={weather_ok}")

    # REPLAY determinism: a FRESH session of the same pack, fast-forwarded to the
    # same world hour, must land on the same sky (pack-id + hour seed).
    s3 = EngineSession.start(pb, save_dir="_wc_s3c", llm_backend="minimax")
    g3 = s3.game
    g3.world.state.clock_minutes = saved_clock
    g3.world.state.weather = weather_mod.initial_weather("寒带", None)
    g3.world.state.weather_hour = 7  # opening 清晨 hour
    g3._advance_weather()
    replay_weather = g3.world.state.weather
    replay_ok = (replay_weather == saved_weather)
    log(f"\nREPLAY: fresh session advanced to clock={saved_clock} -> weather={replay_weather} "
        f"(saved={saved_weather})  replay_match={replay_ok}")

    log("\n=== SUMMARY ===")
    log(f"温带无雪={not has_snow_A}  寒带无雷雨={not has_thunder}")
    log(f"存档clock一致={clock_ok}  存档weather一致={weather_ok}  天气可重放={replay_ok}")
    log(f"FALLBACK={fallbacks}  tick_timeouts={timeouts}")
    out.close()

if __name__ == "__main__":
    main()
