#!/Users/innovation_mbp/anaconda/bin/python
#  -*- coding:utf8 -*-

import os
import pexpect
import sys
import commands
import string
import random
import webbrowser

FILE_TYPE =  [".rst", ".md"]
TARGET_DIR = "."
TEMP_DIR = "_sphinxTempAutuRun"

PROJECT_NAME = ""
PROJECT_AUTHER = ""
PROJECT_VERSION = ""

SERVER_ADDRESS = ""
SERVER_PORT = ""
SERVER_USER = ""
SERVER_PASSWORD = ""
APACHE_PATH = ""
APACHE_PORT = ""

namePair = {}
namePair_S = {}

def createConfig(confpath):
    import ConfigParser
    config = ConfigParser.ConfigParser()
    path = confpath + '/.sphinx-autodeploy.conf'

    config.add_section("project")

    PROJECT_NAME = raw_input("PROJECT_NAME:\n")
    config.set("project", "name", "sphinx-docs-"+PROJECT_NAME)

    PROJECT_AUTHER = raw_input("PROJECT_AUTHER(etc: xxx@xxx.com):\n")
    config.set("project", "auther", PROJECT_AUTHER)

    PROJECT_VERSION = raw_input("PROJECT_VERSION(etc: 0.1):\n")
    config.set("project", "version", PROJECT_VERSION)

    config.add_section("server")

    SERVER_ADDRESS = raw_input("SERVER_ADDRESS:\n")
    config.set("server", "address", SERVER_ADDRESS)

    SERVER_PORT = raw_input("SSH_PORT:\n")
    config.set("server", "ssh-port", SERVER_PORT)

    SERVER_USER = raw_input("SSH_USER:\n")
    config.set("server", "ssh-user", SERVER_USER)

    SERVER_PASSWORD = raw_input("SSH_PASSWORD:\n")
    config.set("server", "ssh-password", SERVER_PASSWORD)

    APACHE_PATH = raw_input("TOMCAT_PATH:\n")
    config.set("server", "tomcat-path", APACHE_PATH)

    APACHE_PORT = raw_input("TOMCAT_PORT:\n")
    config.set("server", "tomcat-port", APACHE_PORT)

    config.write(open(path,"w"))

def getConfig(confpath):
    import ConfigParser
    config = ConfigParser.ConfigParser()
    path = confpath + '/.sphinx-autodeploy.conf'
    print "配置文件: ",path

    if not os.path.exists(path):
        createConfig(confpath)
    else:
        config.read(path)
        global PROJECT_NAME,PROJECT_AUTHER,PROJECT_VERSION,SERVER_ADDRESS,SERVER_PORT,SERVER_USER,SERVER_PASSWORD,APACHE_PATH,APACHE_PORT
        PROJECT_NAME = config.get("project","name")
        PROJECT_AUTHER = config.get("project", "auther")
        PROJECT_VERSION = config.get("project", "version")

        SERVER_ADDRESS = config.get("server", "address")
        SERVER_PORT = config.get("server", "ssh-port")
        SERVER_USER = config.get("server", "ssh-user")
        SERVER_PASSWORD = config.get("server", "ssh-password")
        APACHE_PATH = config.get("server", "tomcat-path")
        APACHE_PORT = config.get("server", "tomcat-port")
    return config

def changeConf(newpath):
    filename = os.path.join(newpath,"conf.py")
    fp = file(filename)
    lines = []
    for line in fp:
        lines.append(line)
    fp.close()

    lines.insert(16, 'from recommonmark.parser import CommonMarkParser')
    lines.insert(39, "source_parsers={'.md': CommonMarkParser,}")
    lines[40] = "\nsource_suffix = ['.rst', '.md']\n"
    lines[112] = "html_theme = 'classic'\n"
    s = ''.join(lines)
    # print s
    # exit()
    fp = file(filename, 'w')
    fp.write(s)
    fp.close()

def initSphinx(newpath):
    if os.path.exists(newpath):
        __import__('shutil').rmtree(newpath)
    os.makedirs(newpath)
    os.chdir(newpath)
    ssh = pexpect.spawn("sphinx-quickstart")
    # ssh.logfile = sys.stdout
    ssh.expect("Enter the root path for documentation.",timeout=5)
    ssh.sendline("")
    ssh.sendline("")
    ssh.sendline("")
    ssh.sendline(PROJECT_NAME)
    ssh.sendline(PROJECT_AUTHER)
    ssh.sendline(PROJECT_VERSION)
    ssh.sendline("")
    ssh.sendline("zh_CN")
    ssh.sendline(".rst")
    ssh.sendline("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    ssh.read()
    changeConf(newpath)

def createFile(filename,content):
    output = open(filename, 'w')
    output.write(content)
    output.close()

def getDocsPath(cpath,tpath):
    ret = os.path.join(cpath,tpath)
    if tpath == ".":
        ret = cpath
    elif tpath.startswith("./"):
        ret = os.path.join(cpath,tpath[2:])
    elif tpath.startswith("~/"):
        ret = os.path.join(os.path.expanduser('~'),tpath[2:])
    elif tpath.startswith("/"):
        ret = tpath
    return ret

def iterateFiles(path,temppath):
    os.chdir(path)
    temppath = os.path.join(temppath,TEMP_DIR)
    cmd = 'cp -r '+getDocsPath(path,TARGET_DIR)+" "+temppath
    (status, output) = commands.getstatusoutput(cmd)

    mixName(temppath)

    for parent, dirnames, filenames in os.walk(temppath):
        indexFile = os.path.join(parent, "index.rst")
        content = ""

        flag = 1

        oriFilenames = []
        for filename in filenames:
            if filename == "index.rst": continue
            if filename.startswith("."): continue
            if os.path.splitext(filename)[1] in FILE_TYPE:
                oriFilenames.append(namePair[filename])
        oriFilenames.sort()

        for oriFilename in oriFilenames:  # 输出文件信息
            if oriFilename == "index.rst": continue
            if oriFilename.startswith("."): continue
            if os.path.splitext(oriFilename)[1] in FILE_TYPE:
                if flag == 1:
                    flag = 0
                    content += "\n" \
                               ".. toctree::\n" \
                               "   :maxdepth: 2\n" \
                               "\n"
                content += "   " + os.path.splitext(namePair_S[oriFilename])[0] + "\n"

        for dirname in dirnames:
            if dirname.startswith("."):
                dirnames.remove(dirname)
        names = [namePair[dirname] for dirname in dirnames]
        names.sort()
        for dirname in names:  # 输出文件夹信息
            content += "\n"+dirname+"\n================================\n" \
                                    "\n" \
                                    ".. toctree::\n" \
                                    "   :maxdepth: 2\n" \
                                    "\n"
            content += "   "+namePair_S[dirname]+"/index\n"


        createFile(indexFile,content)

def sphinxMake(path):
    os.chdir(path)
    cmd = "make html"
    (status, output) = commands.getstatusoutput('make html')
    if "build succeeded" in output:
        return 0
    return 1

def zipFile(path,filename):
    cmd = "zip -r "+filename+".war ./*"
    os.chdir(path+"/_build/html")
    (status, output) = commands.getstatusoutput(cmd)
    return status

def sshDeploy(path,projectname):
    import pexpect
    import sys
    filename = os.path.join(path,"_build/html/"+projectname+".war")
    addr = "scp -P "+SERVER_PORT+" "+filename+" "+SERVER_USER+"@"+SERVER_ADDRESS+":"+APACHE_PATH+"/webapps/"
    ssh = pexpect.spawn(addr)
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)

        if i == 0:
            ssh.sendline(SERVER_PASSWORD)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(SERVER_PASSWORD)

        r = ssh.read()
        print r
        ret = 0
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        ret = -2
def delBuild(path):
    cmd = "rm -rf "+os.path.join(path,"_build")
    (status, output) = commands.getstatusoutput(cmd)

def delTemp(path):
    os.chdir(path)
    cmd = "rm -rf " + path
    (status, output) = commands.getstatusoutput(cmd)

def id_generator(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def mixName(path):
    filenames = os.listdir(path)  # list the file name

    for filename in filenames:  # 输出文件信息
        if filename.startswith("."):continue
        oldfile = os.path.join(path, filename)
        newfile = os.path.join(path,id_generator(32))
        while (newfile in namePair):
            newfile = os.path.join(path, id_generator(32))
        if os.path.isfile(oldfile):
            if filename == "index.rst": continue
            if os.path.splitext(filename)[1] in FILE_TYPE:
                newfile = newfile+os.path.splitext(filename)[1]
                os.rename(oldfile,newfile)
                namePair[os.path.basename(newfile)] = os.path.basename(oldfile)
                namePair_S[os.path.basename(oldfile)] = os.path.basename(newfile)
        else:
            os.rename(oldfile,newfile)
            namePair[os.path.basename(newfile)] = os.path.basename(oldfile)
            namePair_S[os.path.basename(oldfile)] = os.path.basename(newfile)

            mixName(newfile)

if __name__ == "__main__":
    path = os.getcwd()
    sys.argv.append("g")
    sys.argv.append("/Users/innovation_mbp/Git/DocsManager/Learning-Path")
    if (len(sys.argv) < 2):
        msg = "\nerror:" \
              "\n    缺少参数\n" \
              "\n格式:" \
              "\n    sphinx-autodeploy.py 动作 [路径] [项目名称]\n" \
              "\n动作:\n" \
              "    g: 本地生成测试\n" \
              "    d: 生成并服务器部署\n" \
              "    c: 清理生成内容"
        exit(msg)
    TARGET_DIR = "."
    if len(sys.argv) > 2:
        TARGET_DIR = sys.argv[2]

    print "工作目录:",path
    print "文档目录: ",getDocsPath(path,TARGET_DIR)

    # 获取项目及服务器配置参数
    getConfig(getDocsPath(path,TARGET_DIR))

    if (sys.argv[1] == "g"):
        print "本地生成测试"
        cmdType = 0
    elif (sys.argv[1] == "d"):
        print "生成并服务器部署"
        cmdType = 1
    elif (sys.argv[1] == "c"):
        print "清理生成内容"
        cmdType = 2
    else:
        msg = "\nerror: 缺少参数\n" \
              "\n格式:" \
              "\nsphinx-autodeploy.py 动作 [路径] [项目名称]\n" \
              "\n动作:\n" \
              "    g: 本地生成测试\n" \
              "    d: 生成并服务器部署\n" \
              "    c: 清理生成内容"
        exit(msg)

    temppath = os.path.join(os.path.expanduser('~'),TEMP_DIR)

    initSphinx(temppath)

    if cmdType < 2:
        content = "文档目录\n" \
              "===============\n" \
              "\n" \
              ".. toctree::\n" \
              "   :maxdepth: 2\n" \
              "\n" \
              "   "+TEMP_DIR+"/index"
        print "\n创建首页文件..."
        createFile(os.path.join(temppath, "index.rst"),content)

        print "\n遍历目录创建目录文件..."
        iterateFiles(path,temppath)

        print "\n运行Sphinx make..."
        if (sphinxMake(temppath)):
            exit("ERROR:\n    sphinx make错误")

    if (cmdType==1):
        print "\n创建压缩文件..."
        if (zipFile(temppath, PROJECT_NAME)):
            exit("ERROR:\n    zip文件打包错误")

        print "\n部署到服务器..."
        sshDeploy(temppath, PROJECT_NAME)

    if (cmdType == 1):
        url = "http://"+SERVER_ADDRESS+":"+APACHE_PORT+"/"+PROJECT_NAME
        print "\n文档部署成功, 请浏览器访问:\n    "+url
        webbrowser.open_new_tab(url)
    elif (cmdType == 0):
        url = "file:///"+temppath+"/_build/html/index.html"
        print "\n文档生成成功, 请浏览器访问:\n    "+url
        webbrowser.open_new_tab(url)
    else:
        print "\n内容清理成功"

    if (cmdType != 0):
        print "\n清理临时文件..."
        delTemp(temppath)

    print "\n完成并退出"
