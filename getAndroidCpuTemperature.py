# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import time

defulat_adb_tool_path = "D:\\developSdk\\Android\\sdk\\platform-tools"


def collect_msg(arg_time, arg_log_path, arg_app_name):
    # 根据应用的包名称 获取CPU温度
    global param_device_id
    app_id_str = ""
    cpu_temp_str = ""
    while 1:
        cpu_temp_list = []
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        # cpu_memery_cmd = [os.path.join(defulat_adb_tool_path, "adb"),  "-s", param_device_id, "shell", "su", "-c", "'cat","/sys/class/thermal/thermal_zone0/temp'"]
        # cpu_memery_cmd2 = [os.path.join(defulat_adb_tool_path, "adb"),  "-s", param_device_id, "shell", "su", "-c", "'cat","/sys/class/thermal/thermal_zone2/temp'"]
        
        # child = subprocess.Popen(cpu_memery_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                          cwd=defulat_adb_tool_path)
        # child.wait()
        # child_out = child.stdout.readlines()
        # child.stdout.close()
        # redo_flag = False;
        # if child_out[0].find('sh') >= 0:
        #     redo_flag = True;
        # if redo_flag is True:
            
        #     child = subprocess.Popen(cpu_memery_cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                              cwd=defulat_adb_tool_path)
        #     child.wait()
        #     child_out = child.stdout.readlines()
        #     child.stdout.close()
        #     for item in child_out:
        #         if item.find("Permission denied") >= 0:
        #             print u"权限不足，无法读取文件"
        #             sys.exit(0)
        #         cpu_temp_str = str(float(item)/1000.0)
        # # 将数据写入文件
        # with open(os.path.join(arg_log_path, param_device_id + "_" + arg_app_name + "_cpu.log"), "a") as f:
        #     write_str = '[' + str(
        #         now_time) + ']|{"cpu_temperature":"' + cpu_temp_str + '"} \n'
        #     f.write(write_str)

        # list_cmd = [os.path.join(defulat_adb_tool_path, "adb"),"shell","su","-c","'ls /sys/class/thermal/'"]
        
        # child = subprocess.Popen(list_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                          cwd=defulat_adb_tool_path)
        # child.wait()
        # child_out = child.stdout.readlines()
        # child.stdout.close()
       

        # 获取zone的权限
        # for i in range(0,len(child_out)):
        # "su", "-c",  add ‘’
        cpu_memery_cmd = [os.path.join(defulat_adb_tool_path, "adb"),  "-s", param_device_id, "shell", "cat","/sys/class/thermal/thermal_zone*/temp"]
        child = subprocess.Popen(cpu_memery_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             cwd=defulat_adb_tool_path)
        child.wait()
        child_out = child.stdout.readlines()
        child.stdout.close()
        redo_flag = False;
        cpu_temp_list.append(child_out)

        write_str = '[' + str(now_time) + ']|{"zone1":"' + str(child_out[0][0:len(str(child_out[0])) - 3]) + '"'

        for i in range(1,len(child_out)):
            write_str += ',"zone' +  str(i) + '":"' + str(child_out[i][0:len(str(child_out[i])) - 3]) + '"'
        write_str += '} \n'
        # 将数据写入文件
        with open(os.path.join(arg_log_path, param_device_id + "_" + arg_app_name + "_cpu.log"), "a") as f:
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
    print u"用法 python getAndroidCpu.py --collect-time ... --log-path ... --device-id ..."
    print u"选项："
    print u"\t -h/--help 帮助"
    print u"\t --collect-time 信息采集间隔，以秒为单位"
    print u"\t --log-path 日志文件的放置位置"
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

    if param_collect_time is "" or param_log_path is "" or param_device_id is "":
        print u"参数不足"
        print_help();
        sys.exit(0)

    if check_device() is False:
        print U"设备序列号不存在或离线"
        print_help();
        sys.exit(0)

    collect_msg(param_collect_time, param_log_path, "temperature")

