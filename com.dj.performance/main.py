import time
import subprocess
import re

# user (690147) 从系统启动开始累计到当前时刻，处于用户态的运行时间，不包含 nice值为负进程。
# nice (127021) 从系统启动开始累计到当前时刻，nice值为负的进程所占用的CPU时间
# system (569289) 从系统启动开始累计到当前时刻，处于核心态的运行时间
# idle (1089017) 从系统启动开始累计到当前时刻，除IO等待时间以外的其它等待时间
# iowait (13320) 从系统启动开始累计到当前时刻，IO等待时间(since 2.5.41)
# irq (60126) 从系统启动开始累计到当前时刻，硬中断时间(since 2.6.0-test4)
# soft_irq (47538) 从系统启动开始累计到当前时刻，软中断时间(since 2.6.0-test4)
total_cpu_list_name = ["cpu", "user", "nice", "system", "idle", "iowait", "irq", "soft_irq", "no1", "no2", "no3"]

#
# pid = 6873
# 进程(包括轻量级进程，即线程)号
# comm = a.out
# 应用程序或命令的名字
# task_state = R
# 任务的状态，R: running, S: sleeping(TASK INTERRUP TIBLE), D: disk
# sleep(TASK_UNINTERRUPTIBLE), T: stopped, T: tracing
# stop, Z: zombie, X: dead
# ppid = 6723
# 父进程ID
# pgid = 6873
# 线程组号
# sid = 6723
# c该任务所在的会话组ID
# tty_nr = 34819(pts / 3)
# 该任务的tty终端的设备号，INT（34817 / 256）=主设备号，（34817 - 主设备号）=次设备号
# tty_pgrp = 6873
# 终端的进程组号，当前运行在该任务所在终端的前台任务(包括shell
# 应用程序)的PID。
# task->flags = 8388608
# 进程标志位，查看该任务的特性
# min_flt = 77
# 该任务不需要从硬盘拷数据而发生的缺页（次缺页）的次数
# cmin_flt = 0
# 累计的该任务的所有的waited - for进程曾经发生的次缺页的次数目
# maj_flt = 0
# 该任务需要从硬盘拷数据而发生的缺页（主缺页）的次数
# cmaj_flt = 0
# 累计的该任务的所有的waited - for进程曾经发生的主缺页的次数目
# utime = 1587
# 该任务在用户态运行的时间，单位为jiffies
# stime = 1
# 该任务在核心态运行的时间，单位为jiffies
# cutime = 0
# 所有已死线程在用户态运行的时间，单位为jiffies
# cstime = 0
# 所有已死在核心态运行的时间，单位为jiffies
# priority = 25
# 任务的动态优先级
# nice = 0
# 任务的静态优先级
# num_threads = 3
# 该任务所在的线程组里线程的个数
# it_real_value = 0
# 由于计时间隔导致的下一个
# SIGALRM
# 发送进程的时延，以
# jiffy
# 为单位.
# start_time = 5882654
# 该任务启动的时间，单位为jiffies
# vsize = 1409024（page） 该任务的虚拟地址空间大小
# rss = 56(page)
# 该任务当前驻留物理地址空间的大小
# rlim = 4294967295（bytes） 该任务能驻留物理地址空间的最大值
# start_code = 134512640
# 该任务在虚拟地址空间的代码段的起始地址
# end_code = 134513720
# 该任务在虚拟地址空间的代码段的结束地址
# start_stack = 3215579040
# 该任务在虚拟地址空间的栈的结束地址
# kstkesp = 0
# esp(32
# 位堆栈指针) 的当前值, 与在进程的内核堆栈页得到的一致.
# kstkeip = 2097798
# 指向将要执行的指令的指针, EIP(32
# 位指令指针)的当前值.
# pendingsig = 0
# 待处理信号的位图，记录发送给进程的普通信号
# block_sig = 0
# 阻塞信号的位图
# sigign = 0
# 忽略的信号的位图
# sigcatch = 0
# 82985
# 被俘获的信号的位图
# wchan = 0
# 如果该进程是睡眠状态，该值给出调度的调用点
# nswap
# 被swapped的页数，当前没用
# cnswap
# 所有子进程被swapped的页数的和，当前没用
# exit_signal = 17
# 该进程结束时，向父进程所发送的信号
# task_cpu(task) = 0
# 运行在哪个CPU上
# task_rt_priority = 0
# 实时进程的相对优先级别
# task_policy = 0
# 进程的调度策略，0 = 非实时进程，1 = FIFO实时进程；2 = RR实时进程

pid_cpu_list_name = ["pid", "comm", "task_state", "ppid", "pgid", "sid", "tty_nr", "tty_pgrp", "task",
                     "min_flt", "cmin_flt", "maj_flt", "cmaj_flt", "utime", "stime", "cutime", "cstime", "priority",
                     "nice",
                     "num_threads", "it_real_value",
                     "start_time", "vsize", "rss", "rlim", "start_code", "end_code", "start_stack", "kstkesp",
                     "kstkeip",
                     "pendingsig", "block_sig", "sigign", "sigcatch", "wchan", "nswap", "cnswap", "exit_signal",
                     "task_cpu", "task_rt_priority",
                     "task_policy"]

total_cpu_list = []
pid_cpu_list = []
total_jiffies = []
pid_jiffies = []
pid_cpu_use = {}
cpu_count = 6


def RealGetCpuInfo(pid: str):
    pid_order = 'adb shell cat proc/%s/stat' % pid  # 获取连接设备
    order = 'adb shell cat proc/stat'  # 获取连接设备
    pid_cpu = str(subprocess.Popen(pid_order, shell=True, stdout=subprocess.PIPE).stdout.read())[2:].split(" ")
    total_cpu = str(subprocess.Popen(order, shell=True, stdout=subprocess.PIPE).stdout.read())[2:].split("\\n")[0]
    total_cpu = re.split(' +', total_cpu)
    total_cpu_map = {}
    for item in total_cpu_list_name:
        total_cpu_map[item] = total_cpu[total_cpu_list_name.index(item)]
    total_cpu_list.append(total_cpu_map)

    pid_cpu_map = {}
    for item in pid_cpu_list_name:
        pid_cpu_map[item] = pid_cpu[pid_cpu_list_name.index(item)]
    pid_cpu_list.append(pid_cpu_map)

    print(pid_cpu)
    print(total_cpu)

    # fo = open("stat%s.txt" % num, "w")
    # for astring in pi:
    #     fo.write(astring)
    #     fo.write("\n")
    # fo.close()


def calCpu():
    process_name = "com.dj.songs"
    pip = getPid(process_name)
    GetCpu(pip)
    print("next line")
    calCpuJiffies()
    calPidCpuUse()
    print(pid_cpu_use)


def calPidCpuUse():
    for item in range(0, cpu_count - 1):
        pid_cpu_use["第 %s 个时间间隔" % item] = (pid_jiffies[item + 1] - pid_jiffies[item]) / float(
            total_jiffies[item + 1] - total_jiffies[item]) * 100


def calCpuJiffies():
    for item in total_cpu_list:
        total_jiffies.append(addTotalCpuJiffies(item))
    print(total_jiffies)

    for item in pid_cpu_list:
        pid_jiffies.append(calPidCpuJiffies(item))
    print(pid_jiffies)


def calPidCpuJiffies(cur: {}):
    pid_jiffie = 0
    for item in pid_cpu_list_name[13:17]:
        pid_jiffie = pid_jiffie + int(cur[item])
    return pid_jiffie


def addTotalCpuJiffies(cur: {}):
    total_jiffie = 0
    for item in total_cpu_list_name[1:8]:
        total_jiffie = total_jiffie + int(cur[item])
    return total_jiffie


def GetCpu(pid: str):
    for num in range(0, cpu_count):
        RealGetCpuInfo(pid)
        time.sleep(1)


def getPid(process_name: str):
    order = 'adb shell ps |grep %s' % process_name  # 获取连接设备
    pi = str(subprocess.Popen(order, shell=True, stdout=subprocess.PIPE).stdout.read())
    pid = re.split(' +', pi)[1]
    print(pid)
    return pid


if __name__ == '__main__':
    calCpu()
