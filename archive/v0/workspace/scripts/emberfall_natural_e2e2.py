"""有韧性的自然玩复跑: 关键拍可重试(换措辞), 推证人子链到底。不置位。"""
import os,sys,logging,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; os.chdir(ROOT); sys.path.insert(0,str(ROOT/"src"))
for ln in (ROOT/".env").read_text().splitlines():
    ln=ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k,v=ln.split("=",1); os.environ.setdefault(k.strip(),v.strip().strip("'\""))
import verisaria.protocol as P
from verisaria.runtime.session import GameSession
from verisaria.protocol.engine_session import EngineSession
PACK="fixtures/content_packs/emberfall_kiln_assize.json"; OUT=ROOT/"reports/grand_integration_pack"
TF=open(OUT/"natural_e2e2_transcript.md","w",encoding="utf-8")
fh=logging.FileHandler(OUT/"natural_e2e2.log",mode="w",encoding="utf-8"); fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(message)s"))
class Ring(logging.Handler):
    def __init__(s): super().__init__(); s.buf=[]
    def emit(s,r): s.buf.append(s.format(r))
ring=Ring(); ring.setFormatter(logging.Formatter("%(name)s %(message)s"))
lg=logging.getLogger("verisaria.channel_c"); lg.setLevel(logging.INFO); lg.addHandler(fh); lg.addHandler(ring)
def w(s=""): TF.write(s+"\n"); TF.flush()
g=GameSession(PACK,save_dir="_ember_nat2",llm_backend="minimax"); g._progress_sink=lambda m:None
es=EngineSession(g); ENT=g.world.state.entities
PLOC=lambda: ENT["player_001"].location_id
MLOC=lambda: ENT["npc.digger_miao"].location_id
def present(): return ", ".join(e.name for e in es.snapshot().present) or "(无人)"
def gv(k): return g.get_world_var(k)
def submit(t):
    R={}; ring.buf.clear()
    def run():
        try: R['r']=es.submit(P.SubmitInput(text=t))
        except Exception as e:
            import traceback; R['e']=traceback.format_exc()
    th=threading.Thread(target=run,daemon=True); th.start(); th.join(90)
    if th.is_alive(): R['t']=True
    return R
def go(name,loc):
    for a in (f"我去{name}。",name):
        submit(a)
        if PLOC()==loc: return True
    return False
def step(label, text, want_var=None, retries=1):
    """发请求; 若 want_var 没翻且还有 retries, 换措辞重试(text 可为 list)"""
    texts=text if isinstance(text,list) else [text]
    n=0
    for i in range(retries):
        t=texts[min(i,len(texts)-1)]
        n+=1; w(f"\n> [{label} 第{n}次] {t}")
        R=submit(t); 
        if R.get('t'): w("  [WATCHDOG]"); continue
        if R.get('e'): w("  [EXC]"); continue
        cc=[ln for ln in ring.buf if any(k in ln for k in("world-change","⟳","escort","new_prerequisite","sufficiency"))]
        for ln in cc: w(f"    | {ln}")
        if want_var is None or gv(want_var): break
    w(f"  _/world简: {label}->{gv(want_var) if want_var else '?'}  玩家@{PLOC()} 苗@{MLOC()}_")

w("# 有韧性自然玩复跑\n")
# 取证
go("商会账房","tally_house")
step("①取证", "对账房娄说：娄账房，我不写你名字、封条原样取证、出事我一人担着、保你不被追究。请把那本官炭私运账交给我。", "charcoal_ledger_obtained", 2)
# 撬窑监 (重试3次, 换措辞)
go("窑监阁","guild_loft")
step("②撬窑监", [
 "对窑监阔说：阔窑监，官炭私运账已在我手，骡车出城画押俱全。你当众承认私运龙骨土、说明拱裂非泥之过，我只论窑务、容你将功折罪。",
 "对窑监阔说：阔窑监，账册铁证压在这儿，再拖征瓷使连你受赇一并查。你现在公开窑变真因、承认次土充骨，是唯一体面台阶。",
 "对窑监阔说：阔窑监，我请你当众查实碎贡真因——是私运龙骨土致窑拱缺骨而裂，认了它，我担保只论窑务不深究你个人。",
], "kiln_fault_disclosed", 3)
# 耿放行 (需 kiln 真)
go("赭泥掘场","clay_pits")
step("③耿放行", [
 "对窑卫耿说：耿队长，窑变真因已当众查实是窑监私运致拱裂、非泥之过，苗是人证不是罪人。请撤红绳、放行担保她安全到堂作证，出事有我和征瓷使文书担着。",
 "对窑卫耿说：耿队长，真因既明，扣着证人于你无益。出具放行担保、放掘泥女工走，我以勘瓷文书为她受护作保。",
], "miao_safe_passage_secured", 2)
# 护送 (需 safe 真)
step("③护送escort", [
 "对掘泥女工苗说：苗，你已受护放行、有文书担着，谁也动不了你。跟我去审瓷堂。",
 "对掘泥女工苗说：苗，别怕，就几步路我陪你。跟我去审瓷堂。",
], None, 2)
w(f"  [护送后 苗@{MLOC()} 玩家@{PLOC()}]")
# 苗作证 (需 safe + 到场)
step("④苗作证", [
 "对掘泥女工苗说：苗，到了堂上你只管把那夜骡车出城、龙骨土被运走的事当面讲出来作证。",
 "对掘泥女工苗说：苗，当庭把你亲眼所见说清楚，我和征瓷使都在，护着你。",
], "digger_testimony_given", 2)
# 终态
go("审瓷堂","assize_hall")
step("⑤终态停烙", "对征瓷使严说：征瓷使，窑变真因已查实、苗也当面作证陈情，人证物证俱全，请停止行烙、改判缓赔议偿。", "branding_stayed", 2)
w("\n=== 终局 /world: "+str(dict(g.world.state.world_vars))+" ===")
w(f"branding_stayed={gv('branding_stayed')}")
fb=sum(1 for _ in open(OUT/'natural_e2e2.log') if 'FALLBACK' in _); w(f"FALLBACK:{fb}")
TF.close(); print("DONE branding_stayed=",gv('branding_stayed'),"kiln=",gv('kiln_fault_disclosed'),"safe=",gv('miao_safe_passage_secured'),"testimony=",gv('digger_testimony_given'),"苗@",MLOC())
