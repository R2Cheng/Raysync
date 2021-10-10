import os
import re
import subprocess
import time
from common.logger import logger


def rayfile_c(sessions_num):
    file1 = "E:\\testFile\\1G.txt"
    file2 = "E:\\testFile\\2G.txt"
    file3 = "E:\\testFile\\3G.txt"
    if sessions_num == 0:
        pass
    elif sessions_num ==1 :
        subprocess.Popen(
            ["C:\\Program Files (x86)\\Raysync Client\\rayfile-c.exe", "-a", "172.16.4.252", "-p", "2442", "-u", "test1", "-w", "Test!123", "-o", "upload", "-d","/", "-s", file1], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
    elif sessions_num > 1:
        time.sleep(10)
        subprocess.Popen(
            ["C:\\Program Files (x86)\\Raysync Client\\rayfile-c.exe", "-a", "172.16.4.252", "-p", "2442", "-u", "test1", "-w", "Test!123", "-o", "upload", "-d","/", "-s", file1], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10)
        subprocess.Popen(
            ["C:\\Program Files (x86)\\Raysync Client\\rayfile-c.exe", "-a", "172.16.4.252", "-p", "2442", "-u", "test1", "-w", "Test!123", "-o", "upload", "-d","/", "-s", file2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10)
        subprocess.Popen(
            ["C:\\Program Files (x86)\\Raysync Client\\rayfile-c.exe", "-a", "172.16.4.252", "-p", "2442", "-u", "test1", "-w", "Test!123", "-o", "upload", "-d","/", "-s", file3], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10)

def rayfile_c_remove_all():
    subprocess.Popen(
        ["C:\\Program Files (x86)\\Raysync Client\\rayfile-c.exe", "-a", "172.16.4.252", "-p", "2442", "-u", "test1","-w", "Test!123", "-o", "remove", "-s", "/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def t_rayfile_c():
    file1 = "E:\\testFile\\5M.txt"
    p = subprocess.Popen(
        ["C:\\Program Files (x86)\\Raysync Client\\rayfile-c.exe", "-a", "172.16.4.252", "-p", "2442", "-u", "test1","-w", "Test!123", "-o", "upload", "-d", "/", "-s", file1,"-l","./log.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, unused_err = p.communicate()
    print(output.decode('utf-8'))

def t_rayfile_c2():
    p = subprocess.Popen(
        ["C:\\Program Files (x86)\\Raysync Client\\rayfile-c.exe", "-a", "172.16.4.252", "-p", "2442", "-u", "test1","-w", "Test!123", "-o", "mkdir", "-dd", "/test1", "-l", "./log.log"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output, unused_err = p.communicate()
    print(output.decode('utf-8'))

def t_rayfile_c3():
    p = subprocess.Popen(
        ["C:\\Program Files (x86)\\Raysync Client\\rayfile-c.exe", "-h"], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    output, unused_err = p.communicate()
    print(output.decode('utf-8'))
def rayfile_cmd(address,user,password,operation,destination,source,p="Port",num=1):
    root_path = os.path.abspath(os.path.dirname(__file__)).split('pytestDemo-master')[0]
    log_file = str(root_path) + "/rayfile_c.txt"
    if p == "Port":
        cmd = ["C:\\Program Files (x86)\\Raysync Client\\rayfile-c.exe", "-a", address, "-P", "32001", "-u", user,"-w", password,"-l", log_file]
    else:
        cmd = ["C:\\Program Files (x86)\\Raysync Client\\rayfile-c.exe", "-a", address, "-p", "2442", "-u", user,"-w", password,"-l", log_file]
    if operation == "rename" or operation == "move" or operation == "copy":
        cmd.append("-o")
        cmd.append(operation)
        cmd.append("-d")
        cmd.append(destination)
        cmd.append("-s")
        cmd.append(source)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, unused_err = p.communicate()
    elif operation == "list" or operation == "mkdir":
        cmd.append("-o")
        cmd.append(operation)
        cmd.append("-d")
        cmd.append(destination)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, unused_err = p.communicate()
    elif operation == "remove" :
        cmd.append("-o")
        cmd.append(operation)
        if num !=1:
            for i in destination:
                cmd.append("-s")
                cmd.append(i)
        else:
            cmd.append("-s")
            cmd.append(destination)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, unused_err = p.communicate()
    elif operation == "upload" or operation == "download":
        cmd.append("-o")
        cmd.append(operation)
        cmd.append("-d")
        cmd.append(destination)
        if num !=1:
            for i in source:
                cmd.append("-s")
                cmd.append(i)
        else:
            cmd.append("-s")
            cmd.append(source)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, unused_err = p.communicate()
    else:
        output = "请输入正确的operation"
        error_code = None
        return output,error_code
    logger.info(cmd)
    logger.info(output)
    #list和upload 终端输出与日志无显示无权限时的状态和错误码，以终端输出为空来默认无权限
    if operation == "list":
        time.sleep(2)
        if output.decode('utf-8') == '':
            error_code = 16
        else:
            error_code = None
    elif operation == "upload":
        if "Upload file completed. {} file(s) was uploaded. failed: {}".format(num,num) in output.decode("utf-8"):
            error_code = 16
        else:
            error_code = None
    elif operation == "download":
        if "Download file completed. {} file(s) was downloaded. failed: {}".format(num,num) in output.decode("utf-8"):
            error_code = 16
        else:
            error_code = None
    else:
        error_code = getErrorCode(operation,log_file)
    return output.decode('utf-8'), error_code

def getErrorCode(operation,log_file):
    try:
        file = log_file
        if operation == "copy" or operation == "move":
            with open(file,"r+") as f:
                lines = f.readlines()[-15:]
                for line in lines:
                    s = re.match(r".*Move/Copy response: id=5 error_code=(.*?)\n",line,re.M)
                    if s != None:
                        return int(s.group(1))
        # elif operation == "download":
        #     with open(file,"r+") as f:
        #         lines = f.readlines()[-15:]
        #         for line in lines:
        #             s = re.match(r".*Download start response: id=5 error_code=(.*?)\n",line,re.M)
        #             if s != None:
        #                 return s.group(1)
        elif operation == "mkdir":
            with open(file,"r+") as f:
                lines = f.readlines()[-15:]
                for line in lines:
                    s = re.match(r".*Make directory response: id=3 error_code=(.*?)\n",line,re.M)
                    if s != None:
                        return int(s.group(1))
        elif operation == "rename":
            with open(file,"r+") as f:
                lines = f.readlines()[-15:]
                for line in lines:
                    s = re.match(r".*Rename response: id=4 error_code=(.*?)\n",line,re.M)
                    if s != None:
                        return int(s.group(1))
        elif operation == "remove":
            with open(file,"r+") as f:
                lines = f.readlines()[-15:]
                for line in lines:
                    s = re.match(r".*Remove response: id=3 error_code=(.*?)\n",line,re.M)
                    if s != None:
                        return int(s.group(1))
    except Exception as e:
        logger.info("获取日志信息错误,错误是",e)


if __name__ == "__main__":
    # out_list,error_code_list = rayfile_cmd(address="172.16.4.252",user="raysync_test",password="Test!123",operation="list",destination="/",source="")    #list
    # out_upload,error_code_upload = rayfile_cmd(address="172.16.4.252", user="raysync_test", password="Test!123", operation="upload", destination="/",source="E:\\testFile\\5M.txt")  #upload 单个
    # out_uploads,error_code_uploads = rayfile_cmd(address="172.16.4.252", user="raysync_test", password="Test!123", operation="upload", destination="/",source=["E:\\testFile\\42M.txt","E:\\testFile\\41M.txt"],num=2) #upload 多个，num对应其数量
    # out_download,error_code_download = rayfile_cmd(address="172.16.4.252", user="raysync_test", password="Test!123", operation="download", destination="E:\\testFile\\download",source="/5M.txt") #download
    # out_downloads,error_code_downloads = rayfile_cmd(address="172.16.4.252", user="test1", password="Test!123", operation="download",destination="E:\\testFile\\测试下载文件夹", source=["/5M.txt","/4M.txt"],num=2)  # download 多个，num对应其数量
    out_mkdir,error_code_mkdir = rayfile_cmd(address="172.16.4.252", user="raysync_test", password="Test!123", operation="mkdir",destination="/cmdmkdir", source="") #mkdir
    # out_rename,error_code_rename = rayfile_cmd(address="172.16.4.252", user="test1", password="Test!123", operation="rename",destination="test3", source="/test1") #rename
    # out_remove,error_code_remove = rayfile_cmd(address="172.16.4.252", user="test1", password="Test!123", operation="remove",destination="/test1", source="") #remove
    # out_removes,error_code_removes = rayfile_cmd(address="172.16.4.252", user="test1", password="Test!123", operation="remove",destination=["/4M.txt","/5M.txt"], source="",num=2)  # remove 多个,num对应其数量
    # out_copy,error_code_copy = rayfile_cmd(address="172.16.4.252", user="test1", password="Test!123", operation="copy",destination="/test1/test.txt", source="/5M.txt")  #copy
    # out_move,error_code_move = rayfile_cmd(address="172.16.4.252", user="test1", password="Test!123", operation="move",destination="/test1/ssss.txt", source="/5M.txt") #mvoe
    print(out_mkdir,error_code_mkdir)
    # s=getErrorCode("move")
    # print(s)