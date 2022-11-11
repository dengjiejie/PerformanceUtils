import time
from tkinter import Tk, Canvas

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# x = np.linspace(0, 10, 100)
# y = np.cos(x)
#
# fig = Figure(figsize=(5, 4), dpi=100)
#
# for p in range(50):
#     p=3
#     updated_x=x+p
#     updated_y=np.cos(x)
#     plt.plot(updated_x,updated_y)
#     plt.draw()
#     x=updated_x
#     plt.pause(0.2)
#     # fig.clear()


root = Tk()

root.geometry('1000x500')

root.resizable(False, False)

graph = Canvas(root, width=1000, height=550, background='black')  # 后面查点和删点的时候需要画布类

graph.grid()

# 初始化点

tracePlot = [20, 20, 30, 30, 40, 50, 56, 78]

# 实现动态显示

while True:
  t = time.time()
  tracePlot[3] = int(t % 100)  # 动态变化的数据
  print(tracePlot)

  traceID = graph.create_line(tracePlot, fill='Red', width=2)

  root.update_idletasks()

  root.update()  # 更新显示

  graphItems = graph.find_all()

  for n in graphItems:
    graph.delete(n)  # 如果没有删除操作，旧点不消除，新点也会画在上面
