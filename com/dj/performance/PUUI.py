import concurrent
import threading
import time
from concurrent.futures import thread
from queue import Queue
from tkinter import *
import CalCpu
from CpuFigure import *

LOG_LINE_NUM = 0


class CpuPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class MY_GUI:
    msg_queue = None  # 创建一个队列
    start_cpu_show = False
    num = 0
    cpu_figure = None

    def __init__(self, root:Tk):
        self.init_data_label = None
        self.cpu_start_button = None
        self.cpu_stop_button = None
        self.result_data_Text = None
        self.root = root
        self.msg_queue = Queue()
        # 设置根窗口默认属性
        self.set_init_window()
        self.root.after(100, self.handleMsg, self.root)
        self.root.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

    def handleMsg(self, root):
        # 把队列中的内容取出赋值给label控件
        mpica = self.msg_queue.empty()  # 检查队列是否为空
        if not mpica:
            single_msg = self.msg_queue.get()
            self.result_data_Text.insert(END, "key %s, value %s" % (single_msg.key, single_msg.value))
            self.result_data_Text.insert(END, "\n")
            self.cpu_figure.refreshAddPoint(single_msg.key, single_msg.value)

        root.after(500, self.handleMsg, root)  # 递归调用实现循环，TKinter UI线程中无法使用传统的while循环只能用它这个自带的函数递归实现循环

    # 设置窗口
    def set_init_window(self):
        self.root.title("性能工具")  # 窗口名
        self.root.geometry('2000x1000+10+10')
        self.init_data_label = Label(self.root, text="cpu 占用率统计")
        self.init_data_label.grid(row=0, column=0)
        self.cpu_start_button = Button(self.root, text="开始统计 ", bg="lightblue", width=10,
                                       command=self.startCpu)
        self.cpu_start_button.grid(row=1, column=0)

        self.cpu_stop_button = Button(self.root, text="停止统计 ", bg="lightblue", width=10,
                                      command=self.stopCpu)
        self.cpu_stop_button.grid(row=2, column=0)
        self.result_data_Text = Text(self.root, width=100, height=5)
        self.result_data_Text.grid(row=3, column=1, sticky=W)
        self.result_data_Text["bg"] = "red"
        self.cpu_figure = CpuFigure()
        self.cpu_figure.showFigureInWindow(self.root)

    def startCpu(self):
        try:
            self.start_cpu_show = True
            start_thread = threading.Thread(target=self.syncShowCpu)
            start_thread.start()
        except Exception as e:
            print(e)

    def stopCpu(self):
        self.start_cpu_show = False

    def syncShowCpu(self):
        print("THREAD NAME : " + threading.currentThread().getName())
        while self.start_cpu_show:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                res = executor.submit(CalCpu.calCpu, self.num)
            self.msg_queue.put(CpuPair(self.num, res.result()))
            self.num += 1
            time.sleep(1)
        self.num = 0
        CalCpu.clear()


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    MY_GUI(init_window)


gui_start()
