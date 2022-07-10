import json

def readCSV(fileName):
    f = open(fileName, 'r')
    content = f.read()
    rows = content.split('\n')
    temp = [st.split(',') for st in rows]
    data = []
    for row in temp[1:]:
        s = {}
        for index in range(len(row)):
            s[temp[0][index]] = row[index]
        data.append(s)
    return data

def writeJSON(data, subs, fileName):
    f = open(fileName, 'w')
    f.write("data = " + json.dumps(data) + ";\n")
    f.write("subs = " + json.dumps(subs) + ";\n")

# writeJSON(readCSV("./iris-normalization.csv"), "./1.js")
