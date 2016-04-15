# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import time

defulat_adb_tool_path = "D:\\developSdk\\Android\\sdk\\platform-tools"


def collect_msg(arg_time, arg_log_path, arg_app_name):
    # 根据应用的包名称 获取CPU以及内存占用
    global param_device_id
    app_id_str = ""
    send_network_str = ""
    rec_network_str = ""
   
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    cpu_memery_cmd = [os.path.join(defulat_adb_tool_path, "adb"), "-s", param_device_id, "shell", "top", "-m", "10", "-n", "1"]
    child = subprocess.Popen(cpu_memery_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             cwd=defulat_adb_tool_path)
    child.wait()
    child_out = child.stdout.readlines()
    child.stdout.close()
    for item in child_out:
        if item.find(arg_app_name) > 0:
            app_pid_location = item.find(" ")  # 获取app pid
            begin_find = 0
            while app_pid_location == 0:
                begin_find += 1
                app_pid_location = item[begin_find:].find(" ")
            # print app_pid_location
            app_id_str = item[begin_find:app_pid_location + begin_find]
            break
    while 1:
        # 获取流量使用情况
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        flow_cmd = [os.path.join(defulat_adb_tool_path, "adb"), "-s", param_device_id, "shell", "cat", "/proc/" + app_id_str + "/net/dev"]
        child = subprocess.Popen(flow_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=defulat_adb_tool_path)
        child.wait()
        child_out = child.stdout.readlines()
        child.stdout.close()
        for item in child_out:
            if item.find('wlan0') > 0:
                # print item
                begin_find = item.find(": ")
                tmp_l = 0;
                last_location = item[begin_find + 2:].find(" ")
                while last_location == 0:
                	tmp_l += 1
                	last_location = item[begin_find + 2 + tmp_l:].find(" ")
                # network_str = item[begin_find + 2:last_location + begin_find + 2]  # 流量数值
                rec_network_str = str(int(item[begin_find + 2:begin_find + last_location + tmp_l + 2 ]))
                begin_find = begin_find + 2
                count_time = 0
                tmp_l = 0
                tmp_la = 0
                while count_time < 9:
                	tmp_l = 0;
                	tmp_la = item[begin_find:].find(" ")
                	while tmp_la == 0:
                		tmp_l += 1
                		tmp_la = item[begin_find + tmp_l:].find(" ")
                	begin_find = begin_find + tmp_l + tmp_la
                	count_time += 1
                send_network_str = str(int(item[begin_find - tmp_la:begin_find]))
                # print item[begin_find + tmp_lo + 2:last_location + begin_find + tmp_lo + tmp_l + 2]
                # network_str = item[begin_find + 2:last_location + begin_find + 2]  # 流量数值
                break
        # 将数据写入文件

        with open(os.path.join(arg_log_path, param_device_id + "_" + arg_app_name + "_network.log"), "a") as f:
            write_str = '[' + str(now_time) + ']|{"rec_data":"' + rec_network_str + 'B","send_data":"' + send_network_str + 'B"} \n'
            f.write(write_str)
        time.sleep(float(arg_time))


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

    collect_msg(param_collect_time, param_log_path, param_package_name)

