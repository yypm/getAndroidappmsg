# -*- coding:utf-8 -*-

import os
import json
import csv
import collections
import pylab

# 根据日志文件生成对应的csv文件
def log_deal(arg_floder_path,arg_floder_name):
    for item in os.listdir(arg_floder_path):
        if item.endswith(".log"):
            item_path = os.path.join(arg_floder_path,item)
            # print arg_floder_path
            with open(item_path,"r") as item_file:
                line = item_file.readline()
                # print line
                while(line):
                    message_item = line.split("|")[1]
                    jsondata = json.loads(message_item)
                    # cpu占用
                    if item.endswith("s_cpu.log") or item.endswith("ee_cpu.log"):
                        with open(item_path[:len(item_path) - 4] + ".csv", "ab") as write_file:
                            csv_writer = csv.writer(write_file)
                            csv_writer.writerow([line.split("|")[0][1:len(line.split("|")[0]) - 1],jsondata["cpu"][:-1]])
                    # 内存
                    if item.endswith("_memory.log"):
                        with open(item_path[:len(item_path) - 4] + ".csv", "ab") as write_file:
                            csv_writer = csv.writer(write_file)
                            csv_writer.writerow([line.split("|")[0][1:len(line.split("|")[0]) - 1],jsondata["memory"][:-1]])
                    # 网络
                    if item.endswith("_network.log"):
                        with open(item_path[:len(item_path) - 4] + ".csv", "ab") as write_file:
                            csv_writer = csv.writer(write_file)
                            csv_writer.writerow([line.split("|")[0][1:len(line.split("|")[0]) - 1],jsondata["rec_data"][:-1],jsondata["send_data"][:-1]])
                    # 电池
                    if item.endswith("_battery.log"):
                        with open(item_path[:len(item_path) - 4] + ".csv", "ab") as write_file:
                            csv_writer = csv.writer(write_file)
                            csv_writer.writerow([line.split("|")[0][1:len(line.split("|")[0]) - 1],jsondata["battery_temperature"]])
                    # cpu温度
                    # if item.endswith("e_cpu.log"):
                    #     temp = []
                    #     temp.append(line.split("|")[0][1:len(line.split("|")[0]) - 1])
                    #     sort_item = sorted(jsondata.items(), key=lambda x: int(x[0][4:len(x[0])]))
                    #     for _,val in sort_item:
                    #         temp.append(val)
                    #     with open(item_path[:len(item_path) - 4] + ".csv", "ab") as write_file:
                    #         csv_writer = csv.writer(write_file)
                    #         csv_writer.writerow(temp)
                    line = item_file.readline()

# 计算总共使用的流量数据单位M
def summery_net_work(arg_floder_path,arg_item_name,arg_summery_path):
    temp = 0.0
    for item in os.listdir(arg_floder_path):
        if item.endswith("network.csv"):
            item_path = os.path.join(arg_floder_path,item)
            with open(item_path,'rb') as file_:
                reader = csv.reader(file_)
                score = [float(row[1]) for row in reader]
                temp = (score[len(score) - 1 ] - score[0])/1024/1024
            with open(arg_summery_path + "net_Summery.csv",'ab') as write_file:
                csv_writer = csv.writer(write_file)
                csv_writer.writerow([arg_item_name,temp])

# 绘制某一列的走势图
def print_chart(arg_floder_path,arg_floder_name,arg_chart_path):
    for item in os.listdir(arg_floder_path):
        if item.endswith("_network.csv"):
            item_path = os.path.join(arg_floder_path,item)
            count = 1
            x = []
            y = []
            with open(item_path, 'rb') as network_file:
                reader = csv.reader(network_file)
                for row in reader:
                    y.append(float(row[1]))
                    x.append(count)
                    count += 1


                point = dict(zip(x, y))
                point_set = collections.OrderedDict(sorted(point.items()))
                pylab.plot(point_set.keys(), point_set.values(), 'b')
                pylab.title('brisque')
                pylab.savefig(os.path.join(arg_chart_path, arg_floder_name +".png"), dpi=200)
                pylab.clf()

# 获取电池温度起始温度
def get_bettery_tempreture(arg_floder_path,arg_floder_name,arg_csv_path):
    for item in os.listdir(arg_floder_path):
        if item.endswith("temperature_battery.csv"):
            item_path = os.path.join(arg_floder_path,item)
            with open(item_path,'rb') as battery_file:
                reader = csv.reader(battery_file)
                for row in reader:
                    if ( reader.line_num > 1):
                        break
                    else:
                        with open(os.path.join(arg_csv_path,"battery_start_tempreture.csv"),'ab') as write_file:
                            csv_writer = csv.writer(write_file)
                            csv_writer.writerow([item,row[1]])


if __name__ == "__main__":

    # log_deal('./hy_h264_boat_s5_04')
    for item in os.listdir('.'):
        if os.path.isdir(os.path.join('.',item)):
            log_deal(os.path.join('.',item),item)
    # for floder in os.listdir('./data'):
    #     floder_path = os.path.join('./data',floder)
    #     for item in os.listdir(floder_path):
    #         if item.endswith('.log'):
    #             os.remove(os.path.join('./data',floder,item))
    # for item in os.listdir('./csv'):
    #     if os.path.isdir(os.path.join('./csv',item)):
    #         dummery_net_work(os.path.join('./csv',item),item,'./')
    # for item in os.listdir('./log'):
    #     if os.path.isdir(os.path.join('./log',item)):
    #         # print_chart(os.path.join('./log',item),item,'./chart')
    #         get_bettery_tempreture(os.path.join('./log',item),item,'./')
