# sphinx-autodeploy
## 功能说明
自动创建sphinx文档，并通过scp，将打包好的war包部署到指定的tomcat服务器。

`文档格式仅支持: .md .rst`

工作原理：

1. 调用sphinx-quickstart，在临时目录初始化sphinx工程
1. 将项目复制到临时目录，并将所有文件、目录进行随机重命名（为了解决tomcat中文名称乱码问题）
1. 遍历目录，并在每个文件夹下生成对于的index.txt（sphinx目录文件）
1. 调用sphinx的“make html”，生成sphinx文档，并打包成.war格式
1. 调用scp将.war格式压缩包上传到指定的服务器目录（由tomcat自动解压、部署war包）
1. 打开浏览器进行访问
1. 清除本地临时目录及文件

## 安装

**安装sphinx**

首先必须确保已经正确安装了sphinx，并能在Terminal直接输入“sphinx-quickstart”

[sphinx安装方法](http://firechecking.github.io/2017/08/18/sphinx%E7%94%A8%E6%B3%95/)

**当前路径使用sphinx-autodeploy**

1. 将下载的sphinx-autodeploy.py放到任意路径
1. 在控制台输入python sphinx-autodeploy.py测试是否安装成功

**任意路径使用sphinx-autodeploy**

1. 将下载的sphinx-autodeploy.py修改为sphinx-autodeploy（去掉.py后缀）
1. 打开sphinx-autodeploy文件，修改第一行

		#!/Users/innovation_mbp/anaconda/bin/python
	
	为自己电脑中已安装的有效python路径
	
1. 将sphinx-autodeploy复制到PATH目录，如果/usr/local/bin

1. 将sphinx-autodeploy权限设置为可执行，如“chome 777 sphinx-autodeploy”

1. 在控制台输入sphinx-autodeploy，测试是否安装成功

## 使用

**调用格式**

sphinx-autodeploy.py 动作 [路径]

**动作**

* g: 本地生成测试
* d: 生成并服务器部署
* c: 清理生成内容
    
**路径**

* 默认为当前路径
* 可指定相对或绝对路径

**参数配置**

在控制台输入"sphinx-autodeploy g"（如果安装方法参照“当前路径使用sphinx-autodeploy”，需输入"python sphinx-autodeploy.py g"）后，程序会检测文档目录是否存在". sphinx-autodeploy.conf"配置文件

首次创建时，不存在配置文件，需要根据提示依次输入以下信息：

* PROJECT_NAME：项目名称
* PROJECT_AUTHER：文档作者
* PROJECT_VERSION：文档版本
* SERVER_ADDRESS：服务器地址
* SSH_PORT：ssh登陆端口
* SSH_USER：ssh登陆用户名
* SSH_PASSWORD：ssh登陆密码
* APACHE_PATH：服务器tomcat地址
* APACHE_PORT：服务器tomcat访问端口