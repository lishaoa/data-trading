import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def scatter_plot(x_index, y_index, color_list):
    plt.title("Prices offered at each time slot")
    plt.scatter(x_index, y_index, c = color_list, s = 4, marker = "o")
    plt.show()
    return

def generate_data(data_size):
    seed = np.random.randn(data_size * 2)
    seed_result = []
    for seed_ele in seed:
        if -2 <= seed_ele <= 2 and len(seed_result) < data_size:
            seed_ele = 260 + seed_ele * 20
            seed_result.append(round(seed_ele, 3))
    data = [0]
    for i in range(0, data_size):
        if i % 100 == 0:
            data_ele = seed_result[i] * math.pow(1.006,  - i)
        else:
            data_ele = seed_result[i] * (1 - i / data_size)
        data.append(round(data_ele, 3))
    return data


def offer_price(price, time_slot, data, x_index, y_index, y_tmp, color_list):
    y_tmp.append(price)
    y_index.append(data[time_slot])
    x_index.append(time_slot)
    color_list.append('y')
    if price >= data[time_slot]:
        return False
    else:
        return True


def update_weight(k, t, price_set, data, n_set, u_set, x_index, y_index, y_tmp, color_list):
    if offer_price(price_set[k], t, data, x_index, y_index, y_tmp, color_list):
        for i in range(0, k + 1):
            u_set[t][i] = price_set[i]
            n_set[t][i] = 1
    else:
        for i in range(k, H + 1):
            u_set[t][i] = 0
            n_set[t][i] = 1
    return


T = 1000
beta = 0.2
H = 32
gamma = 0.9
c = 400
x_index = []
y_index = []
y_tmp = []
color_list = []
times = 1

for ti in range(0, times):
    price_set = []
    n_set = [[0] * (H + 1)] * (T + 1)
    u_set = [[0] * (H + 1)] * (T + 1)
    print(ti)
    for i in range(0, H + 1):
        price_ele = math.pow((1 + beta), i)
        price_set.append(round(price_ele, 3))
    data = generate_data(T)
    print('step1 ok')
    for t in range(1, H + 2):
        update_weight(t - 1, t, price_set, data, n_set, u_set, x_index, y_index, y_tmp, color_list)
    print("step2 ok")
    for t in range(H + 2, T + 1):
        w_set = []
        ind_max = 0
        for i in range(0, H + 1):
            n = 0
            m = 0
            u = 0
            for s in range(1, t - 1):
                n += n_set[s][i]
                m += n_set[s][i] * math.pow(gamma, t - s)
                u += u_set[s][i] * math.pow(gamma, t - s)
            u = u / m
            w = u + ( (c *  math.log(t - 1))/ n) ** 0.5
            #print(n, ',', m, ', ', u, ', ', w)
            w_set.append(w)
        k = w_set.index(max(w_set))
        #print(k)
        #break
        update_weight(k, t, price_set, data, n_set, u_set, x_index, y_index, y_tmp, color_list)

for i in range(1, times):
    for j in range(0, T):
        y_tmp[j] += y_tmp[j + T * i]
for i in range(0, T):
    y_index.append(y_tmp[i] / times)
    x_index.append(i + 1)
    color_list.append('g')

scatter_plot(x_index, y_index, color_list)

