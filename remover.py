from fractions import gcd
import json
data = json.load(open('steinhaus.json'))
newdata=data[:]
for j in data:
    a,b,c,l = j
    if gcd(a,gcd(b,gcd(c,l)))!=1:
        print('Removing value',j)
        newdata.remove(j)
        json.dump(newdata,open('steinhaus.json','w'))
