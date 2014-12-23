res = {}
for i in range(0,50000):
    a = str(i)[0]
    if a not in res: res[a] = 0
    res[a] += 1

print res
