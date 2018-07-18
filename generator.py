from fractions import gcd
import json
try:
    found=json.load(open('steinhaus.json'))
except FileNotFoundError:
    found=[]
bot=int(input('bottom border='))
top = int(input('top border='))
try:
    for a in range(bot,top):
        print(((a-bot)/(top-bot))*100,'% done')
        try:
            found=json.load(open('steinhaus.json'))
        except FileNotFoundError:
            found=[]
        for b in range(bot,top):
            for c in range(bot,top):
                for l in range(bot,top):
                    asq=a*a
                    bsq=b*b
                    csq=c*c
                    lsq=l*l
                    if asq*asq+bsq*bsq+csq*csq+lsq*lsq==asq*bsq+asq*csq+asq*lsq+bsq*csq+bsq*lsq+csq*lsq:
                        if sorted([a,b,c,l]) not in found:
                            found+=[sorted([a,b,c,l])]
                            print(sorted([a,b,c,l]))
                            json.dump(found, open('steinhaus.json', 'w'))
except KeyboardInterrupt:
    print('Found:',found)
finally:
    print('Writing json...')
    json.dump(found, open('steinhaus.json', 'w'))
