# LSSA.py

import matplotlib.pyplot as plt
import numpy as np
import DWPA
import copy


import matplotlib.patches as patches

# 水平线类
class Outline:
    def __init__(self, origin, end, height):
        self.origin = origin
        self.end = end
        self.height = height


class Parts:
    def __init__(self, width, height, id):
        self.width = width
        self.height = height
        self. id = id
    "旋转"
    def rotate(self):
        temp = self.width
        self.width = self.height
        self.height = temp


class Layout:
    def __init__(self, width, height, line_list=[]):
        # 布局总高
        self.height = height
        # 布局总宽
        self.width = width
        # 水平线链表
        self.line_list = line_list
        # 最低水平线
        self.lowest_line = None
        # 最低水平线索引
        self.lowest_line_index = 0
        # 结果位置表
        "结果为[[左下横坐标x，左下纵坐标y，矩形width，矩形height，编号id]]"
        self.result_pos = []
        # 记录布局是否有效
        self.valid_flag = True

    # 初始化水平线集合
    def init_line_list(self, origin, end, height):
        init_line = Outline(origin, end, height)
        self.line_list = [init_line]
        self.lowest_line = init_line
        self.lowest_line_index = 0

    # 寻找最低水平线
    def find_lowest_line(self):
        # 找最小高度
        lowest_h = min([_l.height for _l in self.line_list])
        if lowest_h > self.height:
            self.valid_flag = False
            return
        # 找最小高度的最小横坐标
        lowest_ox = min([_l.origin for _l in self.line_list if _l.height == lowest_h])
        # 对最低水平线赋值
        for i, _l in enumerate(self.line_list):
            if _l.height == lowest_h and _l.origin == lowest_ox:
                self.lowest_line_index = i
                self.lowest_line = _l

    # 当所有矩形都放不进最低水平线时，提升水平线,将索引为index的最低水平线提升
    def enhance_line(self, index):
        line_list_len = len(self.line_list)
        # 水平线集合大小为1时，提升毫无意义
        if line_list_len == 1:
            self.valid_flag = False
            return
        if index == 0:
            neighbor_idx = 1
        elif index == line_list_len-1:
            neighbor_idx = line_list_len-2
        else:
            left_neighbor_idx = index-1
            right_neighbor_idx = index+1
            left_neighbor = self.line_list[left_neighbor_idx]
            right_neighbor = self.line_list[right_neighbor_idx]
            if left_neighbor.height <= right_neighbor.height:
                neighbor_idx = left_neighbor_idx
            else:
                neighbor_idx = right_neighbor_idx
        "获得最佳邻居索引完成"
        # 左邻居
        if neighbor_idx < index:
            # 延长左邻居边界
            self.line_list[neighbor_idx].end = self.line_list[index].end
            del self.line_list[index]
        # 右邻居
        elif neighbor_idx > index:
            # 延长边界
            self.line_list[index].end = self.line_list[neighbor_idx].end
            # 提升高度
            self.line_list[index].height = self.line_list[neighbor_idx].height
            # 删除右邻居
            del self.line_list[neighbor_idx]

    # 找最高水平线高度
    def find_max_line_height(self):
        return max([_l.height for _l in self.line_list])
    # 插入水平线,在索引为index的水平线的origin（最左边）插入水平线
    '插入的newline要插入到index索引位置，那么它的origin必须为linelist[index].origin'
    'end 为origin+width'
    def insert_line(self, index, new_line):
        # 如果最低水平线在最左边（开头）
        # newline会在index处
        # check
        if (new_line.origin == self.line_list[index].origin and
                new_line.end-new_line.origin <= (self.line_list[index].end - self.line_list[index].origin)):
            if index == 0:
                self.line_list = [new_line] + self.line_list
                self.line_list[index + 1].origin = self.line_list[index].end
                if self.line_list[index+1].origin == self.line_list[index+1].end:
                    self.line_list.pop(index+1)
            else:
                self.line_list.insert(index, new_line)
                self.line_list[index + 1].origin = self.line_list[index].end
                # 如果水平线合并后 余下水平线宽度为0则删去
                if self.line_list[index+1].origin == self.line_list[index+1].end:
                    self.line_list.pop(index+1)
        else:
            print("error!,零件宽度超出水平线")
    # end insert

    # 计算利用率
    def used_ratio(self):
        max_height = self.find_max_line_height()
        if self.height > max_height:
            return ((self.height-max_height)*self.width)/(self.width*self.height)
        else:
            return -1

    # 计算水平线宽度
    @staticmethod
    def cal_line_width(line):
        return line.end - line.origin

    # 排样

    # 零件id转化为零件集合函数
    @staticmethod
    def part_id_turn_to_set(part_set, pid):
        # part_set 中零件以id从1到N按序排放，即索引等于 id - 1
        _parts = copy.deepcopy(part_set)
        "pid 中均是非零整数"
        for i in range(len(part_set)):
            if pid[i] > 0:
                _parts[i] = copy.deepcopy(part_set[pid[i]-1])
            elif pid[i] < 0:
                _parts[i] = copy.deepcopy(part_set[abs(pid[i])-1])
                _parts[i].rotate()
            else:
                print("error ! pid 为 0 ！")
        return _parts

    # 零件价值函数
    @staticmethod
    def value_of_part(wolf, part, maxlength, lowest_line_width):
        wolfpack = wolf.wolfpack
        sigma = wolfpack.sigma
        n = wolfpack.N
        height = part.height
        width = part.width
        # 找出零件 part 在对应狼上面的索引
        index = 0
        for idx in range(len(wolf.pos)):
            p_id = part.id
            value = wolf.pos[idx]
            if p_id == value:
                index = copy.deepcopy(idx)
        L = lowest_line_width
        w = (height*width)*0.5 + 1/(L - width + 0.5)*sigma + (n - index)*(1 - sigma)
        return w

    # 输入布局函数
    def input_and_layout(self, wolf):
        part_set = wolf.part_set
        parts = self.part_id_turn_to_set(part_set, wolf.pos)
        max_attempts = 1000
        attempt = 0
        while parts and attempt < max_attempts:
            self.find_lowest_line()
            lowest_line_width = self.cal_line_width(self.lowest_line)
            "计算当前的maxlength 与 lowest_line_width"
            maxlength = 0
            for part in parts:
                if part.height > maxlength:
                    maxlength = part.height
            # 零件价值数组
            # parts = sorted(parts, key=lambda x: self.value_of_part(wolf, x, maxlength, lowest_line_width), reverse=True)
            flag = 0
            for idx in range(len(parts)):
                # 能放就放
                if parts[idx].width < lowest_line_width and parts[idx].height + self.lowest_line.height <= self.height:
                    part_width = parts[idx].width
                    part_height = parts[idx].height
                    new_line = Outline(self.lowest_line.origin, self.lowest_line.origin + part_width,
                                       part_height + self.lowest_line.height)
                    # 起始放置坐标x
                    x_0 = self.lowest_line.origin
                    # 起始放置坐标y
                    y_0 = self.lowest_line.height
                    self.insert_line(self.lowest_line_index, new_line)
                    "插入后最低水平线对象会发生变化！"
                    # 输入结果
                    "结果为[[左下横坐标x，左下纵坐标y，矩形width，矩形height，编号id]]"
                    self.result_pos.append([x_0, y_0, parts[idx].width,
                                            parts[idx].height, parts[idx].id])
                    "插入完成后更新的最低水平线"
                    self.find_lowest_line()
                    if not self.valid_flag:
                        break
                    # 更新最低水平线宽
                    lowest_line_width = self.cal_line_width(self.lowest_line)
                    # 删除零件表元素
                    parts.pop(idx)
                    flag = 1
                    break
                else:
                    continue
            if not flag:
                self.enhance_line(self.lowest_line_index)
                if not self.valid_flag:
                    break
            attempt += 1
        if attempt >= max_attempts:
            print("布局失败：达到最大尝试次数")
            return

    # 画图
    @staticmethod
    def draw_nest(x, y, width, height):
        x_0 = x
        y_0 = y
        x_1 = x_0 + width
        y_1 = y
        x_2 = x_1
        y_2 = y_1 + height
        x_3 = x_0
        y_3 = y_0 + height
        x_points = np.array([x_0, x_1, x_2, x_3, x_0])
        y_points = np.array([y_0, y_1, y_2, y_3, y_0])
        plt.plot(x_points, y_points, 'b')

    # 寻找最高水平线
    def find_max_line(self):
        return max([_h.height for _h in self.line_list])

    def nesting(self, parts):
        while parts:
            self.find_lowest_line()
            lowest_line_width = self.cal_line_width(self.lowest_line)
            flag = 0
            for idx in range(len(parts)):
                # 直接放到最低水平线上
                if parts[idx].width <= lowest_line_width:
                    part_width = parts[idx].width
                    part_height = parts[idx].height
                    new_line = Outline(self.lowest_line.origin, self.lowest_line.origin + part_width,
                                       part_height+self.lowest_line.height)
                    # 起始放置坐标x
                    x_0 = self.lowest_line.origin
                    # 起始放置坐标y
                    y_0 = self.lowest_line.height
                    self.insert_line(self.lowest_line_index, new_line)
                    "插入后最低水平线对象会发生变化！"
                    # 输入结果
                    "结果为[[左下横坐标x，左下纵坐标y，矩形width，矩形height，编号id]]"
                    self.result_pos.append([x_0, y_0, parts[idx].width,
                                            parts[idx].height, parts[idx].id])
                    "插入完成后更新的最低水平线"
                    self.find_lowest_line()
                    # 更新最低水平线宽
                    lowest_line_width = self.cal_line_width(self.lowest_line)
                    # 删除零件表元素
                    parts.pop(idx)
                    flag = 1
                    break
            # 还有放不下的，只能提升水平线
            if not flag:
                self.enhance_line(self.lowest_line_index)
        print(self.find_max_line())
        print("排样完成")


# 评价函数 LSSA
def lssa(wolf):
    wolfpack = wolf.wolfpack
    ini_line = Outline(0, wolfpack.sheet_width, 0)
    parts_layout = Layout(wolfpack.sheet_width, wolfpack.sheet_height, [ini_line])
    parts_layout.input_and_layout(wolf)
    wolf.layout = parts_layout
    # 无效布局
    if not parts_layout.valid_flag:
        wolf.result = None
        wolf.used_ratio = -1
        return -1
    wolf.result = parts_layout.result_pos
    wolf.used_ratio = parts_layout.used_ratio()
    wolf.max_line_height = parts_layout.find_max_line()
    return parts_layout.used_ratio()


def test_lssa(wolf):
    sheet_width = 1200
    sheet_height = 2400
    ini_line = Outline(0, sheet_width, 0)
    parts_layout = Layout(sheet_width, sheet_height, [ini_line])
    parts_layout.input_and_layout(wolf)
    wolf.layout = parts_layout
    # 无效布局
    if not parts_layout.valid_flag:
        wolf.result = None
        wolf.used_ratio = -1
        return -1
    wolf.result = parts_layout.result_pos
    wolf.used_ratio = parts_layout.used_ratio()
    wolf.max_line_height = parts_layout.find_max_line()
    return wolf.max_line_height


def draw_layout(result, sheet_width, sheet_height):
    # 创建画布和坐标系
    fig, ax = plt.subplots(figsize=(12, 24))  # 根据板材比例设置画布

    # 绘制板材边界
    ax.add_patch(patches.Rectangle((0, 0), sheet_width, sheet_height,
                                   edgecolor='blue', facecolor='none', linewidth=2))

    # 遍历所有排样零件
    for item in result:
        x, y, width, height, pid = item

        # 绘制矩形
        rect = patches.Rectangle((x, y), width, height,
                                 edgecolor='#2c3e50', facecolor='#3498db', alpha=0.7)
        ax.add_patch(rect)

        # 计算文本位置（中心坐标）
        text_x = x + width / 2
        text_y = y + height / 2

        # 添加编号文本
        plt.text(text_x, text_y, str(pid),
                 ha='center', va='center',
                 fontsize=10, color='white',
                 bbox=dict(facecolor='red', alpha=0.7, boxstyle='circle'))

    # 设置坐标轴参数
    plt.xlim(0, sheet_width)
    plt.ylim(0, sheet_height)
    plt.gca().invert_yaxis()  # 反转y轴方向（板材布局通常从上往下绘制）
    plt.axis('equal')  # 保持比例一致
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.title("Nesting Result (Sheet Size: {}x{})".format(sheet_width, sheet_height))

    # 显示绘图
    plt.show()
if __name__ == "__main__":
    # 游走距离因子 要小于 1
    w_0 = 0.99
    # 召唤距离因子
    w_1 = 0.7
    # 攻击距离因子
    w_2 = 0.99
    # 最大迭代次数 K
    k = 200
    # 探索方向
    h = 200
    # 狼群转化比例 theta
    theta = 0.9
    # 优先级比例权重 sigma 越小，索引位置的影响越大
    sigma = 0
    """list = [[500, 400, 0], [330, 440, 1], [350, 450, 2],
            [330,440,3], [440, 330,4], [400, 500,5],
            [400, 500,6], [330,440,7], [450, 350,8],
            [350,450,9], [330,440,10], [500, 400,11]]"""
    list = [[500, 400, 0], [330, 440, 1], [350, 450, 2],
            [330, 440, 3], [440, 330, 4], [400, 500, 5],
            [400, 500, 6], [330, 440, 7], [450, 350,8],
            [350,450,9], [330,440,10], [500, 400,11]]
    part_set = []
    sheet_width = 1200
    sheet_height = 2400
    for _l in list:
        part_set.append(Parts(_l[0],_l[1],_l[2]))
    pos = [1,2,3,4,5,6,7,8,9,10,11,12]
    ini_line = Outline(0, sheet_width, 0)
    parts_layout = Layout(sheet_width, sheet_height, [ini_line])
    print(f"{parts_layout.nesting(part_set)}")
    draw_layout(parts_layout.result_pos, sheet_width, sheet_height)
    print("ok")
