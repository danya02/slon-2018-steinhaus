def test(a,b,c,d,l):
    asq=a**2
    bsq=b**2
    csq=c**2
    dsq=d**2
    lsq=l**2
    return 3*((l**4)+(b**4)+(a**4)+(c**4)+(d**4)) == 2*(bsq*lsq+asq*lsq+asq*bsq+bsq*csq+csq*lsq+asq*csq+asq*dsq+bsq*dsq+csq*dsq+lsq*dsq)

limit=100
found = []
try:
    with open('steinhaus-3d-tetrahedron') as o:
        for i in o:
            i=i.strip()
            if i:
                found.append(sorted([int(n) for n in i.split(' ')]))
except FileNotFoundError:
    pass

for a in range(1,limit):
    for b in range(1,limit):
        for c in range(1,limit):
            for d in range(1,limit):
                for l in range(1,limit):
                    print(f'a={a} b={b} c={c} d={d} l={l}')
                    if sorted([a,b,c,d,l]) not in found:
                        if test(a,b,c,d,l):
                            with open('steinhaus-3d-tetrahedron','a') as o:
                                print(a,b,c,d,l,file=o)
                                print(a,b,c,d,l)
                                found.append(sorted([a,b,c,d,l]))

