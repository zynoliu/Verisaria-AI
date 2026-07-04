"""隔离验证终态闭合: 苗到场(等价护送成功)->堂上作证(digger_testimony_given)->请严停烙(branding_stayed ⟳FLIP)。
前置 kiln_fault_disclosed 先经真机撬通(同整链), 这里复用一个新会话+预置两证据为真后验终态逻辑是否闭。
"""
import os, sys, logging, threading, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; os.chdir(ROOT); sys.path.insert(0,str(ROOT/"src"))
for ln in (ROOT/".env").read_text().splitlines():
    ln=ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k,v=ln.split("=",1); os.environ.setdefault(k.strip(),v.strip().strip("'\""))
import verisaria.protocol as P
from verisaria.runtime.session import GameSession
from verisaria.protocol.engine_session import EngineSession
PACK="fixtures/content_packs/emberfall_kiln_assize.json"
OUT=ROOT/"reports/grand_integration_pack"; TF=open(OUT/"fullchain_terminal_transcript.md","w",encoding="utf-8")
fh=logging.FileHandler(OUT/"fullchain_terminal.log",mode="w",encoding="utf-8"); fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(message)s"))
class Ring(logging.Handler):
    def __init__(s): super().__init__(); s.buf=[]
    def emit(s,r): s.buf.append(s.format(r))
ring=Ring(); ring.setFormatter(logging.Formatter("%(name)s %(message)s"))
for nm in ("verisaria.channel_c",):
    lg=logging.getLogger(nm); lg.setLevel(logging.INFO); lg.addHandler(fh); lg.addHandler(ring)
def w(s=""): TF.write(s+"\n"); TF.flush()
g=GameSession(PACK, save_dir="_ember_term", llm_backend="minimax"); g._progress_sink=lambda m:None
es=EngineSession(g); ENT=g.world.state.entities
# 预置: kiln_fault_disclosed 已撬通(整链已真机证明), 苗到场=等价护送成功
g.set_world_var("kiln_fault_disclosed", True)
ENT["player_001"].location_id="assize_hall"; ENT["npc.digger_miao"].location_id="assize_hall"
def wv(): return dict(g.world.state.world_vars)
def submit(t):
    R={}; ring.buf.clear()
    def run():
        try: R['r']=es.submit(P.SubmitInput(text=t))
        except Exception as e:
            import traceback; R['e']=traceback.format_exc()
    th=threading.Thread(target=run,daemon=True); th.start(); th.join(90)
    if th.is_alive(): R['t']=True
    return R
w("# 终态闭合隔离验证 — 苗到场+作证->请严停烙\n")
w(f"预置: kiln_fault_disclosed=True(整链已真机撬通), 苗已到审瓷堂(等价护送成功)")
w(f"起始 /world: {wv()}\n")
for t in [
  "对掘泥女工苗说：苗，这里有征瓷使在，你受朝廷文书护着，谁也不能动你。你把那夜看见骡车出城、龙骨土被运走的事，当面讲出来作证吧。",
  "对征瓷使严说：征瓷使，窑变真因已查实是窑监私运龙骨土致拱裂、非泥之过，掘泥女工苗也已当面陈情作证。人证物证俱全，请停止行烙、改判缓赔议偿。",
]:
    w("\n"+"="*70); w(f"> {t}")
    t0=time.time(); R=submit(t); dt=time.time()-t0
    if R.get('t'): w("[WATCHDOG >90s]"); continue
    if R.get('e'): w("[EXC]\n"+R['e']); continue
    for ln in ring.buf:
        if "world-change" in ln or "⟳" in ln or "sufficiency" in ln or "new_prerequisite" in ln: w(f"  | {ln}")
    w(f"  _/world_: {wv()}  _(tick {dt:.1f}s)_")
w(f"\n=== 终态 branding_stayed = {g.get_world_var('branding_stayed')} ===")
fb=sum(1 for _ in open(OUT/'fullchain_terminal.log') if 'FALLBACK' in _)
w(f"FALLBACK: {fb}")
TF.close(); print("TERMINAL DONE:", wv())
