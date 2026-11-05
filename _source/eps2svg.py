import sys,re
src,out=sys.argv[1],sys.argv[2]
L=open(src,encoding='latin-1').read().split('\n')
start=next(i for i,l in enumerate(L) if l.startswith('%%EndPageSetup'))
end=next(i for i,l in enumerate(L) if l.startswith('%%PageTrailer'))
body='\n'.join(L[start+1:end])
# drop text/font blocks (Myriad label text) by only tokenising numeric path ops
toks=re.findall(r'-?\d*\.?\d+(?:e-?\d+)?|[A-Za-z_]+|/\S+|\[|\]',body)
stack=[];path=[];color='#000';fills=[];clipdepth=0
def cmyk(c,m,y,k):
    r=round(255*(1-c)*(1-k));g=round(255*(1-m)*(1-k));b=round(255*(1-y)*(1-k));return f'#{r:02X}{g:02X}{b:02X}'
first_clip_done=False
for t in toks:
    if re.fullmatch(r'-?\d*\.?\d+(?:e-?\d+)?',t): stack.append(float(t)); continue
    if t=='mo': y=stack.pop();x=stack.pop();path.append(f'M{x:.3f} {y:.3f}')
    elif t=='li': y=stack.pop();x=stack.pop();path.append(f'L{x:.3f} {y:.3f}')
    elif t=='cv':
        a=stack[-6:];del stack[-6:];path.append('C'+' '.join(f'{v:.3f}' for v in a))
    elif t=='cp': path.append('Z')
    elif t=='cmyk':
        if len(stack)>=4: k=stack.pop();y=stack.pop();m=stack.pop();c=stack.pop();color=cmyk(c,m,y,k)
    elif t in('f','ef'):
        if path: fills.append((color,' '.join(path),'evenodd' if t=='ef' else 'nonzero'))
        path=[]
    elif t in('clp','np','n'):
        path=[]
    else:
        if t not in('cv','li','mo'): stack=stack[-12:]
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1083.08 1312.06">']
for c,d,r in fills: svg.append(f'<path fill="{c}" fill-rule="{r}" d="{d}"/>')
svg.append('</svg>')
open(out,'w').write('\n'.join(svg))
print(len(fills),'fills'); 
from collections import Counter; print(Counter(c for c,_,_ in fills))
