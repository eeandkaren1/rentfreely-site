# -*- coding: utf-8 -*-
"""
租事無憂 — 文章分享圖(OG image)自動產生器
用途：為 _articles/ 每篇文章產生一張帶標題的 PNG 分享圖，存到 assets/og/<slug>.png
用法：在網站資料夾內執行  python generate_og_images.py
      （新增文章後跑一次即可，已存在的圖預設略過，可加 --force 全部重產）
需求：pip install Pillow pyyaml
"""
import glob, re, sys, os
try:
    import yaml
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("缺少套件，請先執行：pip install Pillow pyyaml")
    sys.exit(1)

FORCE = "--force" in sys.argv

CAT = {
 "landlord": {"label":"房東專區","c1":(52,72,46),"c2":(74,103,65),"accent":(143,183,126)},
 "tenant":   {"label":"房客專區","c1":(109,75,50),"c2":(156,107,71),"accent":(216,168,124)},
 "rules":    {"label":"租賃規範知識","c1":(46,63,69),"c2":(66,88,95),"accent":(127,168,178)},
}

# 字型：優先用系統 Noto CJK；找不到時嘗試 Windows 微軟正黑體
FONT_CANDIDATES_BOLD = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "C:/Windows/Fonts/msjhbd.ttc",   # 微軟正黑體 Bold
    "C:/Windows/Fonts/msjh.ttc",
]
FONT_CANDIDATES_REG = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "C:/Windows/Fonts/msjh.ttc",
]
def find_font(cands):
    for f in cands:
        if os.path.exists(f): return f
    return None
FB = find_font(FONT_CANDIDATES_BOLD)
FR = find_font(FONT_CANDIDATES_REG) or FB
if not FB:
    print("找不到中文字型。Windows 請確認有微軟正黑體，或安裝 Noto Sans CJK。")
    sys.exit(1)

def wrap(title, per=13, max_l=3):
    chars=list(str(title)); lines=[]; line=""
    for ch in chars:
        line+=ch
        if len(line)>=per:
            lines.append(line); line=""
            if len(lines)>=max_l: break
    if line and len(lines)<max_l: lines.append(line)
    if len(lines)==max_l and len(chars)>per*max_l:
        lines[max_l-1]=lines[max_l-1][:per-1]+"…"
    return lines

def gradient(w,h,c1,c2):
    base=Image.new("RGB",(w,h),c1); top=Image.new("RGB",(w,h),c2)
    mask=Image.new("L",(w,h)); md=mask.load()
    for y in range(h):
        for x in range(0,w,4):
            v=int(255*((x/w)*0.6+(y/h)*0.4))
            for dx in range(4):
                if x+dx<w: md[x+dx,y]=v
    base.paste(top,(0,0),mask); return base

def make(title, category, out):
    cat=CAT.get(category,CAT["rules"])
    img=gradient(1200,630,cat["c1"],cat["c2"])
    d=ImageDraw.Draw(img,"RGBA")
    d.ellipse([820,-110,1280,350],fill=cat["accent"]+(30,))
    d.ellipse([960,400,1280,720],fill=cat["accent"]+(25,))
    d.rounded_rectangle([80,72,88,118],4,fill=cat["accent"])
    d.text((108,74),cat["label"],font=ImageFont.truetype(FB,34),fill=cat["accent"])
    lines=wrap(title); fbig=ImageFont.truetype(FB,62)
    start_y=250-(len(lines)-1)*45
    for i,ln in enumerate(lines):
        d.text((80,start_y+i*88),ln,font=fbig,fill=(255,255,255))
    d.line([80,500,1120,500],fill=(255,255,255,70),width=2)
    d.text((80,520),"租事無憂",font=ImageFont.truetype(FB,38),fill=(255,255,255))
    d.text((80,572),"rentfreelylife.com",font=ImageFont.truetype(FR,26),fill=(255,255,255,190))
    ftag=ImageFont.truetype(FR,26); tag="房東房客租屋知識平台"
    tw=d.textlength(tag,font=ftag)
    d.text((1120-tw,576),tag,font=ftag,fill=(255,255,255,150))
    img.save(out,"PNG")

os.makedirs("assets/og", exist_ok=True)
made=skip=0
for f in sorted(glob.glob("_articles/*.md")):
    t=open(f,encoding="utf-8").read()
    m=re.match(r'^---\n(.*?)\n---', t, re.S)
    if not m: continue
    fm=yaml.safe_load(m.group(1))
    slug=fm.get("slug") or os.path.basename(f)[11:-3]
    out=f"assets/og/{slug}.png"
    if os.path.exists(out) and not FORCE:
        skip+=1; continue
    make(fm.get("title",""), fm.get("category","rules"), out)
    made+=1
    print(f"  ✓ {slug}.png")
print(f"\n完成：新產 {made} 張，略過已存在 {skip} 張（要全部重產請加 --force）")
