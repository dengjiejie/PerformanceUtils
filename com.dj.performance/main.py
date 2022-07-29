import time
import subprocess
import re

totalcpulist = []
cpuList = []
processJiffies = []





def RealGetCpuInfo(num: int, pid: str):
    pidorder = 'adb shell cat proc/%s/stat' % pid  # 获取连接设备
    order = 'adb shell cat proc/stat'  # 获取连接设备

    pidcpu = str(subprocess.Popen(pidorder, shell=True, stdout=subprocess.PIPE).stdout.read())[2:].split(" ")
    totalcpu = str(subprocess.Popen(order, shell=True, stdout=subprocess.PIPE).stdout.read())[2:].split("\\n")[0]
    totalcpu = totalcpu.split(" ")
    cpumap = {}
    cpumap["cpu"] = totalcpu[0]
    cpumap["user"] = totalcpu[1]
    cpumap["nice"] = totalcpu[2]
    cpumap["system"] = totalcpu[3]
    cpumap["idle"] = totalcpu[4]
    cpumap["iowait"] = totalcpu[5]
    cpumap["irq"] = totalcpu[6]
    cpumap["softirq"] = totalcpu[7]
    cpumap["no1"] = totalcpu[8]
    cpumap["no2"] = totalcpu[9]
    cpumap["no3"] = totalcpu[10]
    cpuList.append(cpumap)
    totalcpulist.append(totalcpu)
    # fo = open("stat%s.txt" % num, "w")
    # for astring in pi:
    #     fo.write(astring)
    #     fo.write("\n")
    # fo.close()
    print(pidcpu)
    print(totalcpu)


def calCpu():
    progerssname = "com.dj.songs"
    pip = getPid(progerssname)
    GetCpu(pip)
    print("next line")
    calUse()


def calUse():
    print(cpuList)
    print(totalcpulist)


def GetCpu(pid: str):
    for num in range(1, 3):
        RealGetCpuInfo(num, pid)
        time.sleep(1)


def getPid(progerssname: str):
    order = 'adb shell ps |grep %s' % progerssname  # 获取连接设备
    pi = str(subprocess.Popen(order, shell=True, stdout=subprocess.PIPE).stdout.read())
    pid = re.split(' +', pi)[1]
    print(pid)
    return pid


if __name__ == '__main__':
    calCpu()
