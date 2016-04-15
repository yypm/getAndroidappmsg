# -*- coding:utf-8 -*-
import subprocess
import threading
import os
import sys

class Temp_cpu_Thread(threading.Thread):
    def __init__(self, arg_collect_time, arg_log_path, arg_device_id):
        threading.Thread.__init__(self)
        self.collect_time = arg_collect_time
        self.log_path = arg_log_path
        self.device_id = arg_device_id
    def run(self):
        cmd = ['python', './getAndroidCpuTemperature.py', "--collect-time", self.collect_time,"--log-path" ,self.log_path,"--device-id",self.device_id]
        child = subprocess.Popen(cmd)
        child.wait()

class Temp_battery_Thread(threading.Thread):
    def __init__(self, arg_collect_time, arg_log_path, arg_device_id):
        threading.Thread.__init__(self)
        self.collect_time = arg_collect_time
        self.log_path = arg_log_path
        self.device_id = arg_device_id
    def run(self):
        cmd = ['python', './getAndroidbatteryTemperature.py', "--collect-time", self.collect_time,"--log-path" ,self.log_path,"--device-id",self.device_id]
        child = subprocess.Popen(cmd)
        child.wait()

class Cpu_Thread(threading.Thread):
    def __init__(self, arg_collect_time, arg_log_path, arg_device_id, arg_app_package):
        threading.Thread.__init__(self)
        self.collect_time = arg_collect_time
        self.log_path = arg_log_path
        self.device_id = arg_device_id
        self.app_package = arg_app_package
    def run(self):
        cmd = ['python', './getAndroidCpu.py', "--collect-time", self.collect_time,"--log-path" ,self.log_path,"--package-name", self.app_package, "--device-id",self.device_id]
        child = subprocess.Popen(cmd)
        child.wait()

class Memory_Thread(threading.Thread):
    def __init__(self, arg_collect_time, arg_log_path, arg_device_id, arg_app_package):
        threading.Thread.__init__(self)
        self.collect_time = arg_collect_time
        self.log_path = arg_log_path
        self.device_id = arg_device_id
        self.app_package = arg_app_package
    def run(self):
        cmd = ['python', './getAndroidMemery.py', "--collect-time", self.collect_time,"--log-path" ,self.log_path,self.log_path,"--package-name", self.app_package,"--device-id",self.device_id]
        child = subprocess.Popen(cmd)
        child.wait()

class Network_Thread(threading.Thread):
    def __init__(self, arg_collect_time, arg_log_path, arg_device_id, arg_app_package):
        threading.Thread.__init__(self)
        self.collect_time = arg_collect_time
        self.log_path = arg_log_path
        self.device_id = arg_device_id
        self.app_package = arg_app_package
    def run(self):
        cmd = ['python', './getAndroidNetwork.py', "--collect-time", self.collect_time,"--log-path" ,self.log_path,self.log_path,"--package-name", self.app_package,"--device-id",self.device_id]
        child = subprocess.Popen(cmd)
        child.wait()

def getparam():
    global param_collect_time
    global param_log_path
    global param_package_name
    global param_device_id
    count = 1
    while count < len(sys.argv):
        if sys.argv[count] == "-h" or sys.argv[count] == "--help":
            print_help()
            sys.exit(0)
        if sys.argv[count] == "--collect-time":
            count += 1
            if count < len(sys.argv):
                param_collect_time = sys.argv[count]
                
        if sys.argv[count] == "--log-path":
            count += 1
            if count < len(sys.argv):
                param_log_path = sys.argv[count]
                
        if sys.argv[count] == "--package-name":
            count += 1
            if count < len(sys.argv):
                param_package_name = sys.argv[count]
        if sys.argv[count] == "--device-id":
            count += 1
            if count < len(sys.argv):
                param_device_id = sys.argv[count]
        count +=1

def check_device():
    global param_device_id;
    cmd = [os.path.join(defulat_adb_tool_path, "adb"),"devices"]
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 cwd=defulat_adb_tool_path)
    child.wait()
    child_out = child.stdout.readlines()
    child.stdout.close()

    flag = False;
    for item in child_out:
        if item.find(param_device_id) >= 0 and item.find("offline") < 0:
            flag = True
            break
    
    return flag;

def print_help():
    print u"用法 python getAndroidCpu.py --collect-time ... --log-path ... --package-name ... --device-id ..."
    print u"选项："
    print u"\t -h/--help 帮助"
    print u"\t --collect-time 信息采集间隔，以秒为单位"
    print u"\t --log-path 日志文件的放置位置"
    print u"\t --package-name 应用的包名"
    print u"\t --device-id 设备序列号"


if __name__ == "__main__":
    adb_path = os.environ.get('ANDROID_HOME')

    if os.path.isdir(os.path.join(adb_path, "platform-tools")):
        defulat_adb_tool_path = os.path.join(adb_path, "platform-tools")
    else:
        print u"请设置‘ANDROID_HOME’环境变量"
        sys.exit(0)

    param_collect_time = ""  # 采集信息时间间隔
    param_log_path = ""  # 日志的放置位置 d:\mi.log
    param_package_name = ""  # 应用的appname
    param_device_id = ""
    if len(sys.argv) <= 3:
        print_help()
        sys.exit(0)

    getparam()

    if param_collect_time is "" or param_log_path is "" or param_package_name is "" or param_device_id is "":
        print u"参数不足"
        print_help();
        sys.exit(0)

    if check_device() is False:
        print U"设备序列号不存在或离线"
        print_help();
        sys.exit(0)
    threads = []
    # cpu temp
    temp_thread = Temp_cpu_Thread(param_collect_time, param_log_path,param_device_id)
    temp_thread.start()
    threads.append(temp_thread)

    temp_thread = Temp_battery_Thread(param_collect_time, param_log_path,param_device_id)
    temp_thread.start()
    threads.append(temp_thread)

    temp_thread = Cpu_Thread(param_collect_time, param_log_path,param_device_id,param_package_name)
    temp_thread.start()
    threads.append(temp_thread)

    temp_thread = Memory_Thread(param_collect_time, param_log_path,param_device_id,param_package_name)
    temp_thread.start()
    threads.append(temp_thread)

    temp_thread = Network_Thread(param_collect_time, param_log_path,param_device_id,param_package_name)
    temp_thread.start()
    threads.append(temp_thread)
    
    for t in threads:
        t.join()

