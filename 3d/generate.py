import multiprocessing
def test(a,b,c,d,l):
    asq=a**2
    bsq=b**2
    csq=c**2
    dsq=d**2
    lsq=l**2
    return 3*((l**4)+(b**4)+(a**4)+(c**4)+(d**4)) == 2*(bsq*lsq+asq*lsq+asq*bsq+bsq*csq+csq*lsq+asq*csq+asq*dsq+bsq*dsq+csq*dsq+lsq*dsq)

limit=60
procs = 16
def worker(num):
    print('I am worker',num)
    for a in range(num,limit,procs):
        for b in range(1,limit):
            print(f'{num}: a={a}, b={b}')
            for c in range(1,limit):
                for d in range(1,limit):
                    for l in range(1,limit):
                        if test(a,b,c,d,l):
                            with open(f'steinhaus-3d-tetrahedron.part{num}','a') as o:
                                print(a,b,c,d,l,file=o)
                                print(num,': FOUND!!!!!',a,b,c,d,l)

if __name__=='__main__':
    proclist = [multiprocessing.Process(target=worker,args=tuple([i+1])) for i in range(procs)]
    for i in proclist:
        i.start()
    try:
        for i,j in enumerate(proclist):
            print(f'Waiting for process {i}...')
            j.join()
    finally:
        print('Combining data!')
        data=[]
        for i in range(procs):
            try:
                data.extend(open(f'steinhaus-3d-tetrahedron.part{i+1}'))
            except:
                pass
        try:
            data.extend(open('steinhaus-3d-tetrahedron'))
        except:
            pass
        data=set(data)
        open('steinhaus-3d-tetrahedron','w').write(''.join(data))
