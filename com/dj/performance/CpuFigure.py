import time
import tkinter
from tkinter import W, Frame

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class CpuFigure:

    def __init__(self):
        self.toolbar = None
        self.canvas = None
        # self.figure, self.figure_plot = plt.subplots(figsize=(5, 4))
        self.figure = plt.figure(figsize=(8, 2))

        # self.figure = Figure(figsize=(5, 4), dpi=100)
        # self.figure_plot = self.figure.add_subplot(111)  # 添加子图:1行1列第1个
        self.x = np.arange(0, 10, 1)
        self.y = np.zeros(10)
        # self.line, = self.figure_plot.plot(self.x, self.y)
        plt.plot(self.x, self.y)

    def showFigureInWindow(self, root):
        # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.draw()  # 注意show方法已经过时了,这里改用draw
        self.canvas.get_tk_widget().grid(row=4, column=1, sticky=W)

            # pack(side=tkinter.TOP,  # 上对齐
            #                              fill=tkinter.BOTH,  # 填充方式
            #                              expand=tkinter.YES)  # 随窗口大小调整而调整
        # # matplotlib的导航工具栏显示上来(默认是不会显示它的)

        toolbarFrame = Frame(master=root)
        toolbarFrame.grid(row=5, column=1, sticky=W)

        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)
        self.toolbar.update()
        # self.toolbar.grid(row=5, column=1, sticky=W)
            # pack(side=tkinter.TOP,  # get_tk_widget()得到的就是_tkcanvas
            #                        fill=tkinter.BOTH,
            #                        expand=tkinter.YES)
        self.canvas.mpl_connect('key_press_event', self.on_key_event)
        # self.bu = tkinter.Button(root, text="refresh ", bg="lightblue", width=10,
        #                          command=self.refreshAddPoint)
        # self.bu.pack(side=tkinter.BOTTOM)

    def on_key_event(self, event):
        """键盘事件处理"""
        print("你按了%s" % event.key)
        key_press_handler(event, self.canvas, self.toolbar)

    def refreshAddPoint(self, num, value):
        print("num %s, value %s" %(num, value))
        self.figure.clear()
        if num == 0:
            self.x = np.arange(0, 10, 1)
            self.y = np.zeros(10)
        elif num >= len(self.x):
            self.x = np.append(self.x, num)
            self.y = np.append(self.y, value)
        else:
            self.y[num] = value
        plt.plot(self.x, self.y)
        plt.draw()
        self.canvas.flush_events()


if __name__ == "__main__":
    root = tkinter.Tk()  # 实例化出一个父窗口
    hh = CpuFigure()
    hh.showFigureInWindow(root)
    root.mainloop()
