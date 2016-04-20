###参数
- 第一个参数：采集信息间隔时间
- 第二个参数：日志文件的放置位置
- 第三个参数：应用的包名

###关于脚本

	该脚本是采集android应用在运行时即时cpu占用，内存占用，流量使用的数据

###完成情况：

- 能采集到相关信息	

###修改情况
	
- 将参数改为从外部接收
- 从环境变量中获取ANDROID_HOME用以使用adb工具
- 修改写日志文件时的打开方式
- 将获取信息的脚本进行分离，每个脚本分别获取CPU占用、内存占用、流量使用、电池温度信息
- 修改了使用说明
- 增加了获取cpu温度的脚本
- 增加了设备的选择
- 流量脚本增加了接受流量的统计
- 获取cpu温度时获取所有的thermmal_zone*的温度，待用
##使用方法

1. getAndroidCpu
	1.  作用：采集应用的CPU占用
	2.  用法：getAndroidCpu.py [options]...
		1. 参数： 
				1. --collect-time 采集间隔
				2. --log-path 日志位置
				3. --package-name 应用包名
				4. --device-id 设备id 
2. getAndroidMemery
	1. 作用：采集应用的内存占用
	2.  用法：getAndroidCpu.py [options]...
		1. 参数： 
				1. --collect-time 采集间隔
				2. --log-path 日志位置
				3. --package-name 应用包名
				4. --device-id 设备id 

3. getAndroidNetwork 
	1. 作用：采集应用的内存占用
	2.  用法：getAndroidCpu.py [options]...
		1. 参数： 
				1. --collect-time 采集间隔
				2. --log-path 日志位置
				3. --package-name 应用包名
				4. --device-id 设备id 
4. getAndroidbatteryTemperature 
	1. 作用：采集手机的电池温度
	2.  用法：getAndroidbatteryTemperature .py [options]...
		1. 参数： 
				1. --collect-time 采集间隔
				2. --log-path 日志位置
				3. --device-id 设备id 
5. getAndroidCpuTemperature 
	1. 作用：采集手机的CPU温度
	2.  用法：getAndroidCpuTemperature .py [options]...
		1. 参数： 
				1. --collect-time 采集间隔
				2. --log-path 日志位置
				3. --device-id 设备id 
	3. 备注：根据手机型号确定脚本能否使用，是否需要命令`shell cat`改为`shell su -c cat`

6. run.py: 
	1. 执行以上的所有监控  
	2.  用法：run.py [options]...
		1. 参数： 
				1. --collect-time 采集间隔
				2. --log-path 日志位置
				3.  --package-name 应用包名
					4. --device-id 设备id 


