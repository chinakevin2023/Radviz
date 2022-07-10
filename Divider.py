def Main(changes, data):
    
    import DataSolver
    import math
    
    n = len(data)

    keys = list(data[0].keys())
    # print(keys)

    def change(x, y):
        ret = []
        for i in range(len(x)):
            ret.append(x[y[i]])
        return ret

    # keys = change(keys, [4, 3, 5, 1, 2, 0, 6])
    # keys = [keys[4], keys[3], keys[5], keys[1], keys[2], keys[0]]
    # print(keys)
    keys = change(keys, changes)
    # print(keys)

    DataSolver.writeJSON(data, keys, "2-1.js")

    # print(data)
    # print("Data Dimension Up Finished...")

    cirR = 1.
    xo = yo = 0
    radvizPos = []

    for i in range(n):
        s0 = s1 = s2 = cnt = 0
        for key in keys:
            if key == "classId":
                break
            # print(cnt, len(data[i].items()) - 1)
            val = data[i][key]
            s0 += val * cirR * math.cos(math.pi * 2 * cnt / (len(data[i].items()) - 1))
            s1 += val * cirR * math.sin(math.pi * 2 * cnt / (len(data[i].items()) - 1))
            s2 += val
            cnt += 1
        sx = xo if s2 == 0 else xo + s0 / s2
        sy = yo if s2 == 0 else yo + s1 / s2
        radvizPos.append((sx, sy))

    # print(radvizPos)
    # print("Radviz Position Done...")

    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(radvizPos)
    radvizLabel = kmeans.predict(radvizPos)

    def getDis(x, y):
        return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

    Maxd = 0
    Mind = 1e100

    for c in range(3):
        for i in range(n):
            for j in range(n):
                if radvizLabel[i] != c or radvizLabel[j] != c:
                    continue
                Maxd = max(Maxd, getDis(radvizPos[i], radvizPos[j]))

    for c1 in range(3):
        for c2 in range(3):
            if c1 != c2:
                for i in range(n):
                    for j in range(n):
                        if radvizLabel[i] != c1 or radvizLabel[j] != c2:
                            continue
                        Mind = min(Mind, getDis(radvizPos[i], radvizPos[j]))

    # print(Mind, Maxd)
    Dunn = Mind / Maxd
    # print("Dunn: {:.4f}".format(Dunn))

    import itertools

    reflect = list(itertools.permutations([0, 1, 2]))

    Accuracy = 0

    for r in reflect:
        cnt = 0
        for i in range(n):
            if r[radvizLabel[i]] + 1 == int(data[i]["classId"]):
                cnt += 1
            # print(radvizLabel[i], data[i]["classId"])
        Accuracy = max(Accuracy, cnt / n)

    # print("Accuracy: {:.4f}".format(Accuracy))

    return Accuracy, Dunn