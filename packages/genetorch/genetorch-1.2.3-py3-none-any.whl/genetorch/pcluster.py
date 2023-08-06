import pandas as pd
import scipy.cluster.hierarchy as hct


class AminoAcid:
    def __init__(self, pro, num):
        self.data = pro[pro['num'] == str(num)]
        self.num = num
        self.name = self.data['aa'].to_list()[0]
        self.x = self.data['x'].to_list()
        self.y = self.data['y'].to_list()
        self.z = self.data['z'].to_list()
        self.x = [float(n) for n in self.x]
        self.y = [float(n) for n in self.y]
        self.z = [float(n) for n in self.z]
        self.median = self.get_grav()

    def get_grav(self):
        n = len(self.x)
        return [sum(self.x) / n, sum(self.y) / n, sum(self.z) / n]


def mat(aa_list):
    matrix = [n.median for n in aa_list]
    ind = [n.name + str(n.num) for n in aa_list]
    return pd.DataFrame(matrix, index=ind)


def cluster_plot(matrix):
    link = hct.linkage(matrix, method='complete', metric='euclidean')
    hct.dendrogram(link, leaf_font_size=10, labels=matrix.index)


def get_num(result, target):
    data = result[result['gene'] == target]['variation'].to_list()[0]
    num_lst = []
    keys = list(data.keys())
    for i in keys:
        if i[-1] != '*':
            num_lst.append("".join(list(filter(str.isdigit, i))))
    while '' in num_lst:
        num_lst.remove('')
    return list(set(num_lst))


def cluster(model_path, result, gene):
    model = []
    with open(model_path) as f:
        for i in f:
            if i.split(' ')[0] == 'ATOM':
                line = i.split(' ')
                while '' in line:
                    line.remove('')
                while '\n' in line:
                    line.remove('\n')
                model.append([line[3], line[-7].strip('A'), line[-6], line[-5], line[-4]])

    model = pd.DataFrame(model,
                         columns=['aa', 'num', 'x', 'y', 'z'])
    num_lst = get_num(result, gene)
    aa_lst = []
    for i in num_lst:
        aa_lst.append(AminoAcid(model, i))
    matrix = mat(aa_lst)
    cluster_plot(matrix)

# 从result行中提取数字
# for i in l:
#     num_lst.append("".join(list(filter(str.isdigit, i[0]))))
# while '' in num_lst:
#     num_lst.remove('')
