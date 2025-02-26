# DWPA.py
import copy

import numpy as np
import math

import LSSA
import random
import time


# 使用高精度时间作为种子
def generate_unique_random_sequence(a, b, length):
    random.seed(time.perf_counter_ns())  # 纳秒级时间戳
    return random.sample(range(a, b+1), length)


# 交换列表两元素位置
def swap_positions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


class Wolf:
    "只狼属性"
    "pos 是 零件id ，是非 0 正整数 !"
    def __init__(self, n, id, part_set, wolfpack, pos=[], result=None, used_ratio=None, value=0):
        # 只狼位置属性
        "pos 是id表"
        self.pos = pos
        # 只狼维数
        self.N = n
        # 狼的 id
        "例外，以0开头！此索引等于id!"
        self.ID = id
        # 狼的评价值
        self.value = value
        # 狼的维度
        self.part_set = part_set
        # 狼所属狼群
        self.wolfpack = wolfpack
        # 狼结果
        self.result = result
        # 利用率
        self.used_ratio = used_ratio
        # 最高水平线高度
        self.max_line_height = None
        # 狼所对应的布局对象
        self.layout = None

    def __del__(self):
        del self.pos,self.N,self.ID,self.value,self.part_set,self.wolfpack,self.result,self.used_ratio
    # 游走算子
    "T(X_i, Q, S)"
    "Q = [0, 1, ... N-1]"
    @staticmethod
    def wander(wolf, q, s):
        "q = Q, Q 中任意选 s 个随机位"
        "随机重排 + 旋转 -----------------------"
        # 取随机位置序列 sequence 对狼的位置进行游走操作
        sequence = random.sample(q, s)
        if s == 2:
            swap_positions(wolf.pos, sequence[0], sequence[1])
        else:
            temp = []
            for k in sequence:
                temp.append(wolf.pos[k])
            "随机旋转（取相反数）"
            # 0 到 len(temp)-1 的整数序列 rotate_q
            rotate_q = []
            for i in range(len(temp)):
                rotate_q.append(i)
            # 从rotate_q 中任选 rd_k 个数 旋转
            rd_k = random.randint(0, len(temp)-1)
            # rotate_sequence 记录旋转位置
            rotate_sequence = random.sample(rotate_q, rd_k)
            while rotate_sequence:
                i = rotate_sequence.pop(0)
                # 对应位取相反数
                temp[i] = -temp[i]

            "打乱temp序列"
            random.shuffle(temp)
            # 当重排序列temp, sequence 不为空时弹出列表头元素
            # 同时弹出sequence头元素
            while temp and sequence:
                t = temp.pop(0)
                k = sequence.pop(0)
                wolf.pos[k] = t
        # 更新狼的评价值
        wolf.value = LSSA.lssa(wolf)

        "end ---------------------------------"

    # 奔袭算子 R(X_i, L_1, L_2, s)
    "注意 l1已0开头，l2不以0开头！"
    @staticmethod
    def raid(wolf, l1, l2, s):
        # l1 是待选中 '位值' ，l2 是奔袭目标值，从 L1 中任意选 s个数
        sequence_id = []
        temp = []
        "步长因子可能大于不同的位置个数！"
        lens_l1 = len(l1)
        min_step = min(lens_l1, s)
        for i in range(len(l1)):
            temp.append(i)
        "对应奔袭目标位索引表sequence_id（0开头）,任选s个给temp"
        sequence_id = random.sample(temp, min_step)
        for i in range(len(sequence_id)):
            # 索引值 k 可能为 0
            k = sequence_id[i]
            # 先进行绝对值替换
            for j in range(len(wolf.pos)):
                "pos 与 l2 均是 id 列表，都是非零整数"
                if abs(wolf.pos[j]) == abs(l2[k]):
                    wolf.pos[j] = copy.deepcopy(wolf.pos[k])
            # 再进行对应位替换
            wolf.pos[k] = copy.deepcopy(l2[k])
        # 实时更新狼的价值
        wolf.value = LSSA.lssa(wolf)


class Wolfpack:
    "狼群属性"
    # 狼群初始化
    def __init__(self, _m, _n, head_wolf,
                 w_0, w_1, w_2, k, h, theta,  sheet_width, sheet_height,
                 sigma):
        # 狼群矩阵
        self.wolfs = []
        # 狼群规模 M
        self.M = _m
        # 只狼位置序列维数（零件个数）N
        self.N = _n
        # 头狼
        self.head_wolf = head_wolf
        # 游走步长 step_wander
        self.step_wander = w_0
        # 召唤距离因子 step_summon
        self.step_summon = w_1
        # 攻击距离步长 step_attack
        self.step_attack = w_2
        # 最大迭代次数 K
        self.K_max = k
        # 最大游走次数 h
        self.H_max = h
        # 狼群更新比例 theta
        self.theta = theta
        # 单狼索引列表Q
        self.Q = []
        # 板材数据
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        # 优先级比例权重
        self.sigma = sigma

    def __del__(self):
        del self.wolfs,self.M,self.N,self.head_wolf,self.step_wander
        del self.step_summon,self.step_attack,self.K_max,self.H_max
        del self.theta,self.Q,self.sheet_width,self.sheet_height
        del self.sigma

    # 随机化狼群矩阵
    def randomization(self, part_set):
        # part_set的形式是 list[ class Parts ]
        # id 以0开头
        if self.M is None:
            return
        for i in range(self.M):
            # 生产 1 到 N 的随机序列
            "随机生成狼"
            p = generate_unique_random_sequence(1, self.N, self.N)
            wolf = Wolf(n=self.N, id=i, part_set=part_set, wolfpack=self, pos=p)
            wolf.value = LSSA.lssa(wolf)
            self.wolfs.append(wolf)
        # 初始化索引序列
        for i in range(self.N):
            self.Q.append(i)
        # 产生头狼
        self.head_wolf = self.wolfs[0]
        for wolf in self.wolfs:
            if wolf.value > self.head_wolf.value:
                self.head_wolf = wolf

    # 计算两狼距离函数
    @staticmethod
    def cal_wolf_distance(wolf_1, wolf_2):
        lens = len(wolf_1.pos)
        sum = 0
        for i in range(lens):
            delta = wolf_1.pos[i] - wolf_2.pos[i]
            if abs(delta) != 0:
                sum += 1
        return sum

    # 更新头狼
    def update_head_wolf(self, wolf):
        self.head_wolf = wolf

    # 游走行为
    def wander_behavior(self, wolf):
        y_star = wolf.value
        # 游走步长
        step_a = math.ceil(self.step_wander * self.N)
        # 记录是否产生头狼
        flag = 0
        # 深拷贝
        best_wolf = copy.deepcopy(wolf)
        for i in range(self.H_max):
            new_wolf = copy.deepcopy(wolf)
            Wolf.wander(new_wolf, self.Q, step_a)
            y_i = new_wolf.value
            "发生头狼转换，立刻交换头狼"
            if y_i >= self.head_wolf.value:
                # 如果新狼评价值高于头狼，那么更新头狼
                wolf = new_wolf
                self.update_head_wolf(wolf)
                flag = 1
                break
            else:
                if y_i > y_star:
                    best_wolf = new_wolf
        "未发生头狼转换，历史最好的位置为该狼新位置"
        if flag == 0:
            wolf = best_wolf
        return flag

    # 围猎判别函数，判断是否符合围猎要求
    def hunting(self, d_near):
        head_wolf = self.head_wolf
        flag = 1
        for wolf in self.wolfs:
            if self.cal_wolf_distance(wolf, head_wolf) > d_near:
                flag = 0
        return flag

    # 召唤行为
    "返回布尔变量值，召唤是否成功"
    def summon(self):
        # 极限奔袭次数
        max_raidtimes = 100
        # 建立头狼别名
        head_wolf = self.head_wolf
        # 游走步长
        step_b = math.ceil(self.N * self.step_summon)
        # 围猎临界半径 d_near
        d_near = math.ceil(self.N * self.step_summon)
        # 计数器 times
        times = 0
        while2_conters = 0
        end_flag = 0
        # do...while
        "while 2"
        while True:
            while2_conters += 1
            if while2_conters >= max_raidtimes:
                break
            "while 1"
            while True:
                # 一次奔袭 (summon 1)
                times += 1
                flag = 0
                for wolf in self.wolfs:
                    # 初始化 l1 ,l2
                    l1 = []
                    l2 = []
                    for i in range(self.N):
                        if wolf.pos[i] != head_wolf.pos[i]:
                            l1.append(i)
                            l2.append(head_wolf.pos[i])
                    # 生成随机数决定是否转移
                    ran_num = np.random.randint(low=0, high=1)
                    "如果生成的随机数小于等于theta,那么探狼转化成猛狼，发生奔袭"
                    if ran_num <= self.theta:
                        Wolf.raid(wolf, l1, l2, step_b)
                    # 如果 y_i > y_lead 那么实时地将奔袭之后的猛狼改为头狼
                    y_i = wolf.value
                    y_lead = head_wolf.value
                    if y_i > y_lead or times >= max_raidtimes:
                        # 注意 ，更新操作只更新个头狼ID
                        self.update_head_wolf(wolf)
                        flag = 1
                        "break the for loop"
                        break
                "continue or break the while 1"
                if flag == 1:
                    continue
                else:
                    break
            "summon 1 end"

            if self.hunting(d_near):
                end_flag = 1
            else:
                end_flag = 0
            # end_flag为 0 代表边界外还有狼 ，要进行第二次奔袭
            if not end_flag:
                end_while_2_flag = 0
                # for tag : **
                for wolf in self.wolfs:
                    distance = self.cal_wolf_distance(wolf, head_wolf)
                    if distance > d_near:
                        # 初始化 l1 ,l2
                        l1 = []
                        l2 = []
                        for i in range(self.N):
                            if wolf.pos[i] != head_wolf.pos[i]:
                                l1.append(i)
                                l2.append(head_wolf.pos[i])
                        Wolf.raid(wolf, l1, l2, distance-d_near)
                        if wolf.value >= head_wolf.value:
                            self.update_head_wolf(wolf)
                            end_while_2_flag = 1
                            # break for : **
                            break
                        else:
                            continue
                if end_while_2_flag == 1:
                    continue
                else:
                    break

    # 围攻行为
    def seige_behavior(self):
        head_wolf = self.head_wolf
        d_close = math.ceil(self.N * self.step_attack)
        for wolf in self.wolfs:
            distance = self.cal_wolf_distance(wolf, head_wolf)
            # 距离大于围猎距离，说明不在目标范围内，奔袭
            if distance > d_close:
                step_c = distance - d_close
                # 初始化 l1 ,l2
                l1 = []
                l2 = []
                for i in range(self.N):
                    if wolf.pos[i] != head_wolf.pos[i]:
                        l1.append(i)
                        l2.append(head_wolf.pos[i])
                wolf.raid(wolf, l1, l2, step_c)
            if wolf.value >= head_wolf.value:
                self.update_head_wolf(wolf)
