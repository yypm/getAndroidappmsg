### 参数
- 第一个参数：采集信息间隔时间
- 第二个参数：日志文件的放置位置
- 第三个参数：应用的包名

### 关于脚本

	该脚本用于采集 android 应用在运行时即时 cpu 占用，内存占用，流量使用的数据

### 完成情况：

- 能采集到相关信息

### 修改情况

- 将参数改为从外部接收
- 从环境变量中获取 ANDROID_HOME 用以使用 adb 工具
- 修改写日志文件时的打开方式
- 将获取信息的脚本进行分离，每个脚本分别获取 CPU 占用、内存占用、流量使用、电池温度信息
- 修改了使用说明
- 增加了获取 CPU 温度的脚本
- 增加了设备的选择
- 流量脚本增加了接受流量的统计
- 获取 CPU 温度时获取所有的 thermmal_zone* 的温度，待用

### 功能简介
|脚本名称|备注|
|-------|---|
|summery|递归式地将当前目录下所有子目录中的 log 文件转换为格式化 csv 文件|
|run|同时运行以下所有监控脚本|
|getAndroidCpu|获取 CPU 占用率|
|getAndroidMemery|获取内存占用率|
|getAndroidNetwork|获取指定进程的网络流量|
|getAndroidbatteryTemperature|获取电池温度|
|getAndroidCpuTemperature|获取 CPU 温度|
