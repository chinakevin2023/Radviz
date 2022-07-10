def Main(dimensionUp):
    import DataSolver
    import matplotlib.pyplot as plt
    import math

    # dataRaw = DataSolver.readCSV("./iris-normalization.csv")
    dataRaw = DataSolver.readCSV("./4DIn12D-350point-withClass3-withXYpointByMDS.csv")
    n = len(dataRaw)

    dataMap = [[0.] * 51 for _ in range(4)]
    col = [[0.] * n for _ in range(4)]

    for i in range(n):
        # col[0][i] = float(dataRaw[i]['col1'])
        # col[1][i] = float(dataRaw[i]['col2'])
        # col[2][i] = float(dataRaw[i]['col3'])
        # col[3][i] = float(dataRaw[i]['col4'])
        col[0][i] = float(dataRaw[i]['dim2'])
        col[1][i] = float(dataRaw[i]['dim6'])
        col[2][i] = float(dataRaw[i]['dim7'])
        col[3][i] = float(dataRaw[i]['dim8'])

    # for j in range(4):
    #     Sum = sum(col[j])
    #     Ave = Sum / len(col[j])
    #     SumStd = 0
    #     for i in range(n):
    #         SumStd += (col[j][i] - Ave) ** 2
    #     SumStd /= n
    #     Std = math.sqrt(SumStd)
    #     for i in range(n):
    #         col[j][i] = (col[j][i] - Ave) / Std
    #     Max = max(col[j])
    #     Min = min(col[j])
    #     for i in range(n):
    #         col[j][i] = (col[j][i] - Min) / (Max - Min)
    #     print(col[j])

    for i in range(n):
        for j in range(4):
            dataMap[j][int(col[j][i] * 100) // 2] += 1

    for i in range(51):
        for j in range(4):
            dataMap[j][i] /= n

    # print(dataMap)

    # plt.hist(col[3], bins=50)
    # plt.show()

    from sklearn.cluster import MeanShift
    import numpy as np
    import copy

    data = [dict() for _ in range(len(dataRaw))]
    # dimensionUp = [2, 3]
    bandwidth = [0.3, 0.2, 0.27, 0.27]

    for dim in range(4):
        ps = []
        index = 0
        reflect = [0] * 51
        for i in range(51):
            # if dataMap[dim][i] == 0:
            #     continue
            reflect[i] = index
            ps.append((i * 2 / 100 + 0.01, dataMap[dim][i]))
            index += 1
        ms = MeanShift(bandwidth=bandwidth[dim])
        ps = np.array(ps)
        ms.fit(ps)
        labels = ms.labels_
        centers = ms.cluster_centers_
        has_label = [0] * (np.max(labels) + 1)
        for i in range(51):
            if dataMap[dim][i] > 0:
                has_label[labels[reflect[i]]] = 1
        unique_labels = sum(has_label)
        real_labels = []
        for i in range(np.max(labels) + 1):
            if has_label[i] == 1:
                real_labels.append(i)
        print(real_labels)
        # print(labels)
        if dim not in dimensionUp:
            for i in range(n):
                data[i]["col" + str(dim)] = col[dim][i]
            continue
        for i in range(n):
            label = labels[reflect[int(col[dim][i] * 100) // 2]]
            data[i]["col" + str(dim) + "." + str(label)] = col[dim][i]
            for j in real_labels:
                if j != label:
                    data[i]["col" + str(dim) + "." + str(j)] = 0

    for i in range(n):
        # data[i]["classId"] = dataRaw[i]["classId"]
        if dataRaw[i]["Name3Class"] == "ClassC":
            data[i]["classId"] = 3
        elif dataRaw[i]["Name3Class"] == "ClassB":
            data[i]["classId"] = 2
        else:
            data[i]["classId"] = 1
    
    return data