# main.py

import matplotlib.pyplot as plt
import numpy as np
import LSSA
import DWPA
import copy

# main()
if __name__ == "__main__":
    # 板材大小
    sheet_width = 1400
    sheet_height = 3500
    parts_size = [[454, 954], [454, 954], [504, 942], [442, 979], [534, 1089], [410, 142], [410, 142], [410, 142],
                  [410, 142], [410, 142], [409, 976], [409, 976], [409, 976]]
    parts = []
    "优先将最大面积的零件放进去"
    # 按面积由大到小排序
    _parts_size = sorted(parts_size, key=lambda x: x[0] * x[1], reverse=True)
    # id 数组
    lens = len(parts_size)
    ids = [i + 1 for i in range(lens)]
    # 初始化零件列表 parts
    for id in range(lens):
        parts.append(LSSA.Parts(_parts_size[id][0], _parts_size[id][1], ids[id]))
    # 设定狼群参数
    "狼的个数：m"
    m = 50
    # 游走距离因子 要小于 1
    w_0 = 0.5
    # 召唤距离因子
    w_1 = 0.8
    # 攻击距离因子
    w_2 = 1
    # N ：零件个数
    n = 13
    # 最大迭代次数 K
    k = 100
    # 探索方向
    h = 30
    # 狼群转化比例 theta
    theta = 0.98
    # 优先级比例权重
    sigma = 0.65
    # 建狼群
    wolfpack = DWPA.Wolfpack(m, n, head_wolf=None, w_0=w_0, w_1=w_1, w_2=w_2, k=k, h=h,
                             theta=theta, sheet_width=sheet_width, sheet_height=sheet_height,
                             sigma=sigma)
    # 初始化狼群
    wolfpack.randomization(parts)
    # 转换位数 s
    s = 2
    # 探狼游走
    flag_generate_head_wolf = 0
    while True:
        for wolf in wolfpack.wolfs:
            if wolfpack.wander_behavior(wolf):
                flag_generate_head_wolf = 1
        if flag_generate_head_wolf == 1:
            break
    # 头狼召唤
    wolfpack.summon()
    # 狼群围攻
    wolfpack.seige_behavior()
    # 将狼的信息转化成有序零件序列
    head_wolf = wolfpack.head_wolf
    # 利用率
    used_ratio = head_wolf.used_ratio
    # 结果
    result = head_wolf.result
    # 输出利用率
    print(used_ratio)
    # 画图
    for item in result:
        x_0 = item[0]
        x_1 = item[1]
        width = item[2]
        height = item[3]
        LSSA.Layout.draw_nest(x_0, x_1, width, height)

    sheet_x = np.array([0, sheet_width, sheet_width, 0, 0])
    sheet_y = np.array([0, 0, sheet_height, sheet_height, 0])
    plt.plot(sheet_x, sheet_y, 'g')
    plt.show()