import copy

import GUI
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from view import ViewUI as View
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen
import main
import LSSA
import DWPA
from PySide6.QtWidgets import QGraphicsTextItem
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QFileDialog  # 导入文件对话框
from PySide6.QtGui import QIcon


# 全局变量：缩放比例
graphic_zoom_ratio = 5
# 全局变量：狼群参数
# 设定狼群参数
# 游走距离因子 要小于 1
w_0 = 0.8
# 召唤距离因子
w_1 = 0.7
# 攻击距离因子
w_2 = 0.8
# 最大迭代次数 K
k = 20
# 探索方向
h = 50
# 狼群转化比例 theta
theta = 1
# 优先级比例权重 sigma 越小，索引位置的影响越大
sigma = 0.5


class Subwindow(View):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # **调用 setupUi 方法，初始化 UI 元素**
        # 固定窗口大小
        self.setFixedSize(820, 558)
        # 场景引用初始为 None
        self.current_scene = None
        # 当前旋转角度
        self.current_rotation = 0
        # 绑定旋转按钮
        self.Rotate_Button.clicked.connect(self.rotate_image)  # 注意：不要带参数

    def set_scene(self, scene):
        """
        设置场景并更新引用
        """
        self.graphicsView.setScene(scene)
        self.current_scene = scene

    def rotate_image(self):
        """
        旋转视图 90 度，并调整文本项位置
        """
        if self.current_scene is None:
            print("场景未设置！")
            return

            # 创建旋转变换（每次点击旋转90度）
        transform = self.graphicsView.transform()
        transform.rotate(90)
        self.graphicsView.setTransform(transform)

        # 逆时针旋转文本90度（抵消视图旋转）
        """
        for item in self.current_scene.items():
            if isinstance(item, QGraphicsTextItem):
                # 使用变换操作保持文本方向
                item.setRotation(- 90)  # 逆时针旋转

        # 更新当前旋转角度
        """
        self.current_rotation += 90
        if self.current_rotation >= 360:
            self.current_rotation = 0


class NestingThread(QThread):
    # 定义一个信号，用于将结果传递回主线程
    nesting_finished = Signal(object)  # 信号传输类对象数据

    def __init__(self, parts, wolf_quantity,
                 sheet_width, sheet_height,
                 w_0, w_1, w_2, k, h, theta,
                 sigma, parent=None):
        super().__init__(parent)
        self.parts = parts
        self.wolf_quantity = wolf_quantity
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.w_0 = w_0
        self.w_1 = w_1
        self.w_2 = w_2
        self.k = k
        self.h = h
        self.theta = theta
        self.sigma = sigma
        # 单线程狼群
        self.wolfpack = None

    def run(self):
        # 设置重试次数上限
        retry_max_times = 5
        retry_used_ratio = -1
        result = None
        i = 1
        # 可能出现 -1 的情况，那就多试几遍
        while i <= retry_max_times and retry_used_ratio == -1:
            # 执行 nesting 任务
            wolfpack = DWPA.Wolfpack(self.wolf_quantity, len(self.parts), head_wolf=None, w_0=self.w_0, w_1=self.w_1, w_2=self.w_2, k=self.k, h=self.h,
                                     theta=self.theta, sheet_width=self.sheet_width, sheet_height=self.sheet_height,
                                     sigma=self.sigma)
            wolfpack.randomization(self.parts)
            self.wolfpack = wolfpack
            # 对狼群的处理函数 main_nesting
            "类对象是可变对象，main_nesting函数传引用"
            result = main.main_nesting(wolfpack)
            # result 形式：[ result排布, head_wolf.used_ratio, head_wolf.max_line_height]
            retry_used_ratio = result[1]
            i += 1

        # 发射信号，将结果传递回主线程
        if result is not None:
            self.nesting_finished.emit(self.wolfpack.head_wolf)
        else:
            print("结果意外为空！")


class Window(QMainWindow, GUI.GraphicUI):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # **调用 setupUi 方法，初始化 UI 元素**
        # 固定窗口大小
        self.setFixedSize(941, 694)
        # nesting线程标志位
        self.nesting_in_progress = False
        self.setWindowTitle("DWPA")
        self.setWindowIcon(QIcon("icon.ico"))
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: rgba(251, 252, 252, 1);  /* 半透明乳白色背景 */
            }
            QLabel {
                background-color: rgba(251, 252, 252, 1);  
            }
            QPushButton {
                background-color: rgba(150, 150, 150, 0.9);  
                color: black;  /* 黑色文字 */
                border: 1px solid black;  /* 黑色边框 */
                border-radius: 5px;  /* 圆滑边框 */
            }
            QPushButton:hover {
                /* 线性渐变 */
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(150, 150, 150, 0.9), 
                    stop:1 rgba(100, 100, 100, 0.9)
                );
            }
            QPushButton:pressed {
                background-color: rgba(90, 90, 90, 0.9);  /* 按下时的背景色 */
            }
            QListWidget {
                background-color: rgba(244, 245, 245, 0.9);  
                color: black;  /* 黑色文字 */
                border: 1px solid black;  /* 黑色边框 */
                border-radius: 5px;  /* 圆滑边框 */
            }
            QTextBrowser {
                background-color: rgba(217, 220, 221, 0.9);  
                color: black;  /* 黑色文字 */
                border: 1px solid black;  /* 黑色边框 */
                border-radius: 5px;  /* 圆滑边框 */
            }
            QLineEdit {
                background-color: rgba(217, 220, 221, 0.9);  /* 淡灰色背景 */
                color: black;  /* 黑色文字 */
                border: 1px solid black;  /* 黑色边框 */
                border-radius: 5px;  /* 圆滑边框 */
            }
            QSpinBox {
                background-color: rgba(217, 220, 221, 0.9);  /* 淡灰色背景 */
                color: black;  /* 黑色文字 */
                border: 1px solid black;  /* 黑色边框 */
                border-radius: 5px;  /* 圆滑边框 */
            }
        """)
        self.setWindowOpacity(0.95)  # 设置窗口透明度为 95%
        # 高度输入框
        self.heigh_input.setPlaceholderText("Enter height ")
        self.heigh_input_sheet.setPlaceholderText("Enter height ")
        # 宽度输入框
        self.width_input.setPlaceholderText("Enter width ")
        self.width_input_sheet.setPlaceholderText("Enter width ")
        # Add按钮
        self.add_button.clicked.connect(self.add_size)
        # SET按钮
        self.SET_button.clicked.connect(self.set_button_run)
        # wolf SET按钮
        "self.wolf_set_button.clicked.connect(self.set_wolf_quantity)"
        # Nesting按钮
        self.nesting_button.clicked.connect(self.nesting_button_run)
        # Delete按钮
        self.delete_button.clicked.connect(self.delete_size)
        # Preview按钮
        self.preview_button.clicked.connect(self.bind)
        # Import按钮
        self.import_button.clicked.connect(self.import_file)
        # 数据列表
        self.data_result = []
        # 子窗口生成标志
        self.subwindow_flag = 0
        # 零件集合
        self.part_size = []
        # 板材宽度
        self.sheet_width = None
        # 板材高度
        self.sheet_height = None
        # 利用率
        self.used_ratio = None
        # 高度
        self.max_height = None
        # 狼个数
        self.wolf_quantity = 15
        # 狼群数
        self.wolfpack_num = 5
        # 隐藏wolf的label与输入框
        self.sheetsize_display_2.hide()
        self.wolf_label.hide()
        # 创建线程队列
        self.threads = []
        self.results = []

    def bind(self):
        # 画图
        # 实例化子窗口
        self.subwindow = Subwindow()
        self.subwindow_flag = 1
        # 创建场景
        self.scene = QGraphicsScene()
        "逻辑关系：点击preview按钮后生成子窗口并画图"
        self.subwindow.setStyleSheet("""
            QMainWindow {
                background-color: rgba(255, 255, 255, 0.8);  /* 半透明乳白色背景 */
            }
            QLabel {
                background-color: rgba(220, 220, 220, 0.9);  /* 淡灰色背景 */
                color: black;  /* 黑色文字 */
                border: 1px solid black;  /* 黑色边框 */
                border-radius: 3px;  /* 圆滑边框 */
            }
            QPushButton {
                background-color: rgba(220, 220, 220, 0.9);  /* 淡灰色背景 */
                border: 1px solid black;  /* 黑色边框 */
                border-radius: 3px;  /* 圆滑边框 */
            }
        """)
        self.subwindow.setWindowOpacity(0.95)  # 设置窗口透明度为 95%
        self.subwindow.set_scene(self.scene)  # 更新场景引用
        self.draw_parts()
        # 旋转 180°
        self.subwindow.show()

    def draw_parts(self):
        self.scene.clear()
        sheet_width = copy.deepcopy(float(self.sheet_width) / graphic_zoom_ratio)
        sheet_height = copy.deepcopy(float(self.sheet_height) / graphic_zoom_ratio)  # 这是图像缩放比例

        # 绘制板材（矩形），边框为蓝色，背景淡黄色
        sheet_item = QGraphicsRectItem(0, 0, sheet_width, sheet_height)
        sheet_pen = QPen(Qt.blue)
        sheet_item.setPen(sheet_pen)
        sheet_item.setBrush(QColor(255, 255, 224))
        self.scene.addItem(sheet_item)

        # 绘制矩形部件
        for part in self.data_result:
            part_info = copy.deepcopy(part)
            part_info[0] = float(part[0]) / graphic_zoom_ratio
            part_info[1] = float(part[1]) / graphic_zoom_ratio
            part_info[2] = float(part[2]) / graphic_zoom_ratio
            part_info[3] = float(part[3]) / graphic_zoom_ratio
            x, y, height, width, part_id = part_info
            ox, oy, oheight, owidth, opart_id = part

            rect_item = QGraphicsRectItem(x, y, height, width)
            # 设置矩形边框颜色保持半透明绿色
            rect_pen = QPen(QColor(0, 255, 0, 150))
            rect_item.setPen(rect_pen)
            rect_item.setBrush(Qt.gray)  # 设置部件填充为灰色
            self.scene.addItem(rect_item)

            # 在矩形中央绘制编号
            text_item = QGraphicsTextItem(f"{part_id} "
                                          f"{owidth} "
                                          f"{oheight}")
            text_item.setPos(x + height / 2 - 10, y + width / 2 - 10)  # 调整文本位置使其居中
            text_item.setDefaultTextColor(Qt.red)  # 设置文本颜色
            self.scene.addItem(text_item)
            # text_item.setFlag(QGraphicsTextItem.ItemIgnoresTransformations)  # 忽略视图变换

            # 计算居中位置
            """
            text_rect = text_item.boundingRect()
            rect_center = rect_item.boundingRect().center()
            text_item.setPos(
                rect_center.x() - text_rect.width() / 2,
                rect_center.y() - text_rect.height() / 2
            )
            """
            text_item.setDefaultTextColor(Qt.red)
            self.scene.addItem(text_item)


        # 设置场景边界
        self.scene.setSceneRect(0, 0, sheet_width, sheet_height)

    # ADD 按钮
    def add_size(self):
        # 获取用户输入的高度和宽度及零件个数
        height = self.heigh_input.text().strip()
        width = self.width_input.text().strip()
        counts = self.Counters.text().strip()

        # 检查输入是否有效
        if height and width and counts:
            try:
                counts = int(counts)
                while counts:
                    # 将输入的高度和宽度转换为数字，避免输入无效的文本
                    height = int(height)
                    width = int(width)
                    self.part_display.addItem(f"Height: {height} , Width: {width} ")
                    self.heigh_input.clear()
                    self.width_input.clear()
                    self.part_size.append([height, width])
                    counts = counts-1
            except ValueError:
                # 如果输入无法转换为数字，提示错误
                print("Invalid input. Please enter valid numbers for height and width.")

    def delete_size(self):
        selected_item = self.part_display.currentItem()
        if selected_item:
            # 获取当前选中项的文本
            selected_text = selected_item.text()
            # 提取出高度和宽度数据
            try:
                "map 遍历所有元素，对所有元素执行相应的函数 int "
                height, width = map(int, [s.strip() for s in
                                          selected_text.replace("Height:", "").replace("Width:", "").split(",")])
                # 在 main.parts_size 中删除对应的项
                if [height, width] in self.part_size:
                    self.part_size.remove([height, width])
                # 删除列表显示中的项
                self.part_display.takeItem(self.part_display.row(selected_item))
            except ValueError:
                print("Failed to parse the selected item for deletion.")

    def set_button_run(self):
        height = self.heigh_input_sheet.text().strip()
        width = self.width_input_sheet.text().strip()
        # 检查输入是否有效
        if height and width:
            try:
                self.sheetsize_display.clear()
                # 将输入的高度和宽度转换为数字，避免输入无效的文本
                height = int(height)
                width = int(width)
                self.sheet_height = height
                self.sheet_width = width
                self.sheetsize_display.setText(f"当前板材规格：Height:{height} ,Width:{width}")
                self.sheetsize_display.show()
            except ValueError:
                # 如果输入无法转换为数字，提示错误
                print("Invalid input. Please enter valid numbers for height and width.")

    # 批量导入按钮
    def import_file(self):
        """
        批量导入 .txt 文件
        """
        # 打开文件对话框，选择 .txt 文件
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "文本文件 (*.txt)")
        if not file_path:  # 如果用户取消选择文件
            return

        try:
            with open(file_path, "r", encoding='utf-8') as file:
                for line in file:
                    # 解析每一行的数据
                    data = line.strip().split()
                    if len(data) != 3:  # 确保每行有 3 个数据
                        continue

                    height, width, count = data
                    try:
                        height = int(height)
                        width = int(width)
                        count = int(count)
                    except ValueError:
                        continue

                    # 将数据添加到 part_display 和 part_size 中
                    for _ in range(count):
                        self.part_display.addItem(f"Height: {height} , Width: {width}")
                        self.part_size.append([height, width])

            self.usedratio_display.clear()
            self.usedratio_display.setText("批量导入完成")
        except Exception as e:
            self.usedratio_display.clear()
            self.usedratio_display.setText("导入失败")

    def nesting_button_run(self):
        if self.nesting_in_progress:
            return
        if self.wolf_quantity is None:
            self.usedratio_display.clear()
            self.usedratio_display.setText("未设置狼的个数！")
            return
        self.nesting_in_progress = True
        self.usedratio_display.setText(f"Calculating...")
        # 初始化零件列表
        parts = []
        if not self.part_size:
            self.usedratio_display.clear()
            self.usedratio_display.setText("零件集合为空！")
            return
        # 检验板材面积是否不足
        area = 0
        for part in self.part_size:
            area += part[0]*part[1]
        if area > self.sheet_width*self.sheet_height:
            self.usedratio_display.clear()
            self.usedratio_display.setText("板材面积不足！")
            return

        _parts_size = sorted(self.part_size, key=lambda x: x[0] * x[1], reverse=True)
        lens = len(self.part_size)
        ids = [i + 1 for i in range(lens)]
        for id in range(lens):
            parts.append(LSSA.Parts(_parts_size[id][0], _parts_size[id][1], ids[id]))
        # 刷新线程队列
        self.threads = []
        self.results = []

        "for 外仍然可以使用self.thread[i]"
        "这是因为内存回收机制，append是浅拷贝，传的是地址"
        "在for循环结束后thread[i]的引用指针数非0所以不会被回收"
        for _ in range(self.wolfpack_num):
            # 创建线程
            thread = NestingThread(parts, self.wolf_quantity, self.sheet_width, self.sheet_height, w_0, w_1,
                                            w_2, k, h, theta, sigma)
            # 连接信号与槽
            thread.nesting_finished.connect(self.on_nesting_single_thread_finished)
            # 添加至线程队列
            self.threads.append(thread)  # append函数是浅拷贝，call by reference
            # 启动线程
            thread.start()

    """
    def set_wolf_quantity(self):
        quantity = self.wolf_input.text().strip()
        if quantity:
            try:
                self.sheetsize_display_2.clear()
                quantity = int(quantity)
                self.wolf_quantity = quantity
                self.sheetsize_display_2.setText(f"当前狼的数量：{self.wolf_quantity}")
                self.sheetsize_display_2.show()
            except ValueError:
                print("Invalid input")
    """
    def on_nesting_finished(self, result):
        # 处理线程返回的结果
        self.data_result = result[0]
        self.used_ratio = result[1]
        self.max_height = result[2]
        if self.used_ratio is None or self.data_result is None:
            self.usedratio_display.clear()
            self.usedratio_display.setText("材料不可排，超出板材高度！")
            return
        if self.used_ratio != -1:
            self.usedratio_display.clear()
            self.usedratio_display.setText(f"利用率：{self.used_ratio}，最高高度{self.max_height}")
        else:
            self.usedratio_display.clear()
            self.usedratio_display.setText("材料不可排，超出板材高度！")
        self.nesting_in_progress = False  # 重置标志位
        return

    # 选择最佳头狼
    def select_best_result(self):
        best_wolf = min(self.results, key=lambda x: x.max_line_height)
        # 更改数据
        self.used_ratio = best_wolf.used_ratio
        self.max_height = best_wolf.max_line_height
        self.data_result = best_wolf.result  # data_result 是最后的布局位置数据

        if self.used_ratio is None or self.data_result is None:
            self.usedratio_display.clear()
            self.usedratio_display.setText("材料不可排，超出板材高度！")
            return
        if self.used_ratio != -1:
            self.usedratio_display.clear()
            self.usedratio_display.setText(f"利用率：{self.used_ratio}，最高高度{self.max_height}")
        else:
            self.usedratio_display.clear()
            self.usedratio_display.setText("材料不可排，超出板材高度！")
        self.nesting_in_progress = False  # 重置标志位
        return

    # 多线程调用
    def on_nesting_single_thread_finished(self, head_wolf):
        self.results.append(head_wolf)
        if len(self.results) == self.wolfpack_num:
            self.select_best_result()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
