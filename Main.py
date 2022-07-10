import Divider
import DataSolver
import DimensionUp
import itertools
import copy

reflect = list(itertools.permutations([0, 1, 2, 3, 4, 5, 6]))
Max_accuracy = 0
Max_dunn = 0
done = []
index = 0

def cirMove(x):
    y = []
    for i in range(len(x)):
        y.append(x[(i + 1) % len(x)])
    return y

data = DimensionUp.Main([1, 2])

for r in reflect:
    # print("Now Begins...")
    r2 = list(copy.deepcopy(r))

    r3 = copy.deepcopy(r2)
    flag = False
    for _ in range(7):
        r3 = cirMove(r3)
        if r3 in done:
            flag = True
    if flag:
        continue
    done.append(r3)

    r2.append(7)

    # print(r2)
    index += 1
    print(index, r2)

    Accuracy, Dunn = Divider.Main(r2, data)
    if Accuracy > Max_accuracy:
        Max_accuracy = Accuracy
        Save_accuracy = r2
    if Dunn > Max_dunn:
        Max_dunn = Dunn
        Save_dunn = r2
    
print("Max_accuracy: {0:.4f} Max_dunn: {1:.4f}".format(Max_accuracy, Max_dunn))
print(Save_accuracy, Save_dunn)

Divider.Main(Save_accuracy, data)
# Divider.Main(Save_dunn, data)
