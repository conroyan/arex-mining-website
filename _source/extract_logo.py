import re,sys,os
svg=open(sys.argv[1]).read(); OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)
paths=re.findall(r'<path fill="(#\w+)" fill-rule="(\w+)" d="([^"]+)"/>',svg)
def bbox(d):
    n=list(map(float,re.findall(r'-?\d+\.?\d*',d)));xs=n[0::2];ys=n[1::2];return min(xs),min(ys),max(xs),max(ys)
items=[(c,r,d,bbox(d)) for c,r,d in paths]
def pick(x0,y0,x1,y1,want):
    sel=[it for it in items if it[0]==want and it[3][0]>=x0 and it[3][2]<=x1 and it[3][1]>=y0 and it[3][3]<=y1]
    X0=min(i[3][0] for i in sel);Y0=min(i[3][1] for i in sel);X1=max(i[3][2] for i in sel);Y1=max(i[3][3] for i in sel)
    return sel,(X0,Y0,X1,Y1)
def write(name,sel,bb,color,pad=0,bg=None,square=False):
    X0,Y0,X1,Y1=bb;w=X1-X0;h=Y1-Y0
    if square:
        s=max(w,h)+2*pad; vb=f"{X0-(s-w)/2:.2f} {Y0-(s-h)/2:.2f} {s:.2f} {s:.2f}"; W=H=s
    else:
        vb=f"{X0-pad:.2f} {Y0-pad:.2f} {w+2*pad:.2f} {h+2*pad:.2f}"; W=w+2*pad;H=h+2*pad
    body=''.join(f'<path fill-rule="{r}" d="{d}"/>' for _,r,d,_ in sel)
    bgr=''
    if bg:
        vx,vy,vw,vh=map(float,vb.split()); bgr=f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="{vw*0.18:.1f}" fill="{bg}"/>'
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{W:.0f}" height="{H:.0f}" role="img" aria-labelledby="t"><title id="t">AREX Mining</title>{bgr}<g fill="{color}">{body}</g></svg>\n')
TEAL='#00868E'
# horizontal lockup: bottom-left panel (white background), teal artwork
hsel,hbb=pick(0,950,541,1312,'#2AAD8A')
# stacked lockup: top-right panel (white background), teal artwork
vsel,vbb=pick(541,500,1083,910,'#2AAD8A')
print('horizontal',len(hsel),[round(v) for v in hbb]); print('stacked',len(vsel),[round(v) for v in vbb])
for nm,col in [('teal',TEAL),('white','#FFFFFF'),('dark','#043837')]:
    write(f'arex-mining-logo-{nm}.svg',hsel,hbb,col)
    write(f'arex-mining-logo-stacked-{nm}.svg',vsel,vbb,col)
# mark only = paths of horizontal lockup left of the 'A' of AREX: take the leftmost cluster
xs=sorted(set(round(i[3][0]) for i in hsel))
mark=[i for i in hsel if i[3][2] < hbb[0]+ (hbb[2]-hbb[0])*0.27]
mbb=(min(i[3][0] for i in mark),min(i[3][1] for i in mark),max(i[3][2] for i in mark),max(i[3][3] for i in mark))
print('mark',len(mark),[round(v) for v in mbb])
for nm,col in [('teal',TEAL),('white','#FFFFFF'),('dark','#043837')]:
    write(f'arex-mining-icon-{nm}.svg',mark,mbb,col,pad=12)
write('favicon.svg',mark,mbb,'#FFFFFF',pad=(mbb[2]-mbb[0])*0.22,bg=TEAL,square=True)
