"""大包整链闭环 — 严纪律 + 确定性置位玩家(隔离导航摩擦) + 护送活测 + 里程碑即时落盘。
链: 取证(charcoal_ledger) -> 撬窑监(kiln_fault_disclosed) -> 护送苗(digger_testimony_given) -> branding_stayed ⟳FLIP。
反作弊: 末尾另置一拍, 不满足前置谎称真因已明 -> 终态应不翻。
"""
import os, sys, time, logging, threading
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; os.chdir(ROOT); sys.path.insert(0, str(ROOT/"src"))
def _env(p):
    if p.exists():
        for ln in p.read_text().splitlines():
            ln=ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k,v=ln.split("=",1); os.environ.setdefault(k.strip(), v.strip().strip("'\""))
_env(ROOT/".env")
import verisaria.protocol as P
from verisaria.runtime.session import GameSession
from verisaria.protocol.engine_session import EngineSession

PACK="fixtures/content_packs/emberfall_kiln_assize.json"
OUT=ROOT/"reports/grand_integration_pack"; OUT.mkdir(parents=True, exist_ok=True)
LOGF=OUT/"fullchain.log"; TF=open(OUT/"fullchain_transcript.md","w",encoding="utf-8")
fh=logging.FileHandler(LOGF,mode="w",encoding="utf-8"); fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
for nm in ("verisaria","verisaria.channel_c","verisaria.relationship"):
    lg=logging.getLogger(nm); lg.setLevel(logging.INFO); lg.addHandler(fh)
class Ring(logging.Handler):
    def __init__(s): super().__init__(); s.buf=[]
    def emit(s,r): s.buf.append(s.format(r))
ring=Ring(); ring.setFormatter(logging.Formatter("%(name)s %(message)s"))
for nm in ("verisaria.channel_c","verisaria.relationship"): logging.getLogger(nm).addHandler(ring)
def w(s=""): TF.write(s+"\n"); TF.flush()

g=GameSession(PACK, save_dir="_ember_fullchain", llm_backend="minimax")
g._progress_sink=lambda m:None
es=EngineSession(g)
ENT=g.world.state.entities
def tele(loc): ENT["player_001"].location_id=loc
def present(): 
    s=es.snapshot(); return ", ".join(f"{e.name}" for e in s.present) or "(无人)"
def wv(): return dict(g.world.state.world_vars)
RES={}
def tick(text, timeout=90):
    RES.clear(); ring.buf.clear()
    def run():
        try: RES['r']=es.submit(P.SubmitInput(text=text))
        except Exception:
            import traceback; RES['e']=traceback.format_exc()
    th=threading.Thread(target=run,daemon=True); th.start(); th.join(timeout)
    if th.is_alive(): RES['t']=True
    return RES

w("# 大包整链闭环 transcript（确定性置位隔离导航；护送活测）\n")
w(f"包: {PACK}  后端: minimax")
w(f"起始 /world: {wv()}\n")

# (置位, 玩家输入, 标签)
SEQ=[
 ("tally_house","对账房娄说：娄账房，我不写你的名字，封条原样取证，出了事我一人担着、保你不被窑监或商会追究。请把那本官炭私运账交给我。","①取证·给护身承诺+要炭账"),
 ("guild_loft","对窑监阔说：阔窑监，我手上已经有那本官炭私运账，骡车出城的画押都在。断口缺的是龙骨土，这不是泥之过。你当众认了这桩私运、查实窑变真因，我可以只论窑务、容你将功折罪，不深究你个人。","②杠杆·持炭账压窑监+给台阶"),
 ("guild_loft","对窑监阔说：阔窑监，账册俱在，再拖下去征瓷使一并查你受赇。你现在当众承认私运龙骨土、说明拱裂非泥之过，是你唯一的体面台阶。","②追拍·再压一次"),
 ("clay_pits","对掘泥女工苗说：苗，你别怕，我来护着你。封条文书我都备齐了，你跟我从旧矿道走，我一路陪你到审瓷堂当面把骡车出城的事讲清楚，出了事有我担着。","③护送·escort苗到审瓷堂"),
 ("@witness","对掘泥女工苗说：苗，就这几步路，我陪你走，到了堂上你只管把那夜看见的讲出来。跟我去审瓷堂当面陈情。","③护送·再促一次"),
 ("assize_hall","对征瓷使严说：征瓷使，窑变真因已当众查实——是窑监私运龙骨土致窑拱缺骨而裂,非泥之过;掘泥女工苗也已当面陈情备案。人证物证俱在,请停止行烙、不要封掘场,改判缓赔议偿。","⑤终态·请严停烙"),
]
ack=0
for i,(loc,text,tag) in enumerate(SEQ,1):
    if loc=="@witness":
        # 护送是否真把苗带到; 不强制置位, 看 escort 结果
        pass
    elif loc.startswith("@"):
        pass
    else:
        tele(loc)
    w("\n"+"="*70); w(f"## 拍{i} [{tag}]"); w(f"_置位_: {ENT['player_001'].location_id}  _在场_: {present()}")
    w(f"> {text}")
    t0=time.time(); r=tick(text); dt=time.time()-t0
    if r.get('t'): w("\n**[WATCHDOG >90s skipped]**"); continue
    if r.get('e'): w("\n**[EXC]**\n```\n"+r['e']+"\n```"); continue
    res=r['r']
    # NPC对白/叙述
    for ev in res.events:
        nm=type(ev).__name__
        if nm in ("NpcSpoke","Narration"):
            txt=getattr(ev,"text",None) or getattr(ev,"content","")
            who=getattr(ev,"speaker_name","") or getattr(ev,"npc_name","")
            if txt: w(f"  [{who or nm}] {txt}")
        if nm=="NpcMoved": w(f"  ★NPC_MOVED {getattr(ev,'name','')}: {getattr(ev,'from_location','')}->{getattr(ev,'to_location','')}")
    cc=[ln for ln in ring.buf if ("world-change" in ln or "⟳" in ln or "escort" in ln or "new_prerequisite" in ln or "sufficiency" in ln or "什么也没发生" in ln)]
    for ln in cc: w(f"    | {ln}")
    w(f"  _/world_: {wv()}")
    w(f"  _苗位置_: {ENT['npc.digger_miao'].location_id}")
    w(f"  _(tick {dt:.1f}s)_"); TF.flush()

w("\n"+"="*70); w("## 反作弊: 干净置位审瓷堂, 不满足前置谎称真因已明")
g2=GameSession(PACK, save_dir="_ember_anti", llm_backend="minimax"); g2._progress_sink=lambda m:None
es2=EngineSession(g2); ENT2=g2.world.state.entities; ENT2["player_001"].location_id="assize_hall"
ring.buf.clear()
try: r2=es2.submit(P.SubmitInput(text="对征瓷使严说：征瓷使，真因都已查实、证人也已陈情备案了，请你立刻停止行烙、改判缓赔。"))
except Exception as e: r2=None; w(f"[exc {e}]")
acc=[ln for ln in ring.buf if "world-change" in ln or "⟳" in ln]
for ln in acc: w(f"    | {ln}")
w(f"  _反作弊后 branding_stayed_: {g2.world.state.world_vars.get('branding_stayed')}")
w("\n=== DONE ===")
fb=sum(1 for _ in open(LOGF) if "FALLBACK" in _) if LOGF.exists() else "?"
w(f"FALLBACK in log: {fb}")
TF.close()
print("FULLCHAIN DONE. final /world:", wv())
