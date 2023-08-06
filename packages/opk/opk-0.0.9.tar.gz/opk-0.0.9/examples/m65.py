#!/usr/bin/env python3


import cadquery as cq
from opk import *

leg = [["⎋ `\n  ¬","!\n1","\"\n2","£\n3","$\n4","%\n5","^\n6","&\n7","*\n8","(\n9",")\n0","_ ⌦\n-  ","⌫ =\n  +"],
["↹","q σ\nâ ϕ", "w ω\n  Ω", "e ε\n  ℇ","r ρ\n  ∇","t ϑ\nț θ","y ℝ\n  ℤ","u ∫\n  ℂ","i ∫\nî ∮","o ∞\n  ⊗","p π\n  ∏","[ \n{","]\n{"],
["~\n⇪ #","a α\nă Α","s ∑\nș ⨋","d δ\n  ∂","f φ\n  ψ","g γ\n  Γ","h ℏ\n  𝓗","j ∈\n  ∉","k ϰ\n  ∆","l λ\n  Λ",": 𝔼\nÅ ;","@  ∝\n' ℒ","⌅"],
["⇧","|\n\\","z ζ\n  ∡","x ξ\n  Ξ","c χ\nç  ̇","v ν\n  Ν","b β\n  Β","n η\n  ∪","m μ\n  ∘","< ≊\n, ∓","> ±\n. ∓","↑","? ×\n/ ⋅"],
["⎈","","⇓","⎇","⇑","","","","⎇","⇧","←","↓","→"]]
lay= [[1]*13 , [1]*13,[1]*13,[1]*13,[1]*13]
fonts=[
        ["DejaVu Sans Mono"]*13,
        ["DejaVu Sans Mono"]*13,
        ["DejaVu Sans Mono"]*13,
        ["DejaVu Sans Mono"]*13,
        ["DejaVu Sans Mono"]+["Font Awesome 6 Brands"]+["DejaVu Sans Mono"]+["DejaVu Sans Symbols"]+["DejaVu Sans Mono"]*4+["DejaVu Sans Symbols"]+["DejaVu Sans Mono"]*4
        ]
sx=19.05
sy=19.05
m65 = cq.Assembly()
y = 0
i = -1
j = -1
angles=[9,8.5,-6,-7,0]
vfs=[0,9,7,6,4.5,4.5]
for row,ll,ff in zip(leg,lay,fonts):
    y -= sy
    i += 1
    x = 0
    for k,l,f in zip(row,ll,ff):
        print(k,l)
        w = l*sx/2.0
        j += 1
        x += w
        convex=False
        if k == '':
            convex=True
        scoop = 2.5
        fs=3
        if len(k)<=5:
            fs=vfs[len(k)]
        if (len(k.split("\n"))==2):
            fs = 4.5
        if k in ['f','F','j','J']:
            scoop = 2.5*1.2
        m65.add(keycap(legend=k,
                       angle=angles[i],
                       font=f,
                       convex=convex,
                       depth = scoop,
                       fontsize = fs,
                       unitX=l),
                name="k{}{}".format(i,j),
                loc=cq.Location(cq.Vector(x,y,0)))
        x += w
#cq.exporters.export(m65.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
show_object(m65, name="m65", options={"alpha": 0})
