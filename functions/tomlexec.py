import toml
import threading
import time

def readtoml(path):  # 读取toml文件数据
    try:
        data = toml.load(path)
        return data
    except Exception as e:
        print(e)
        #log.log_error(f"读取{path}时捕获到异常:{e}")

def readtomlsu():  # 读取toml文件数据
    try:
        data = toml.load("./lib/toml/su/superadmin.toml")
        sus = []
        for i in data["superadmin"]:
            su1 = [i['username'],i['password'],i['email'],i['SID1'],i['SID2'],i['KEY'],i['emailcode']]
            su2 = [i['phonenumber'], i['password'], i['email'], i['SID1'], i['SID2'], i['KEY'], i['emailcode']]
            sus.append(su1)
            sus.append(su2)
        return sus

    except Exception as e:
        print(e)
        #log.log_error(f"读取{path}时捕获到异常:{e}")

def dumptoml(dst_file,data):#接收映射表数据并写入toml文件
    try:
        with open(dst_file, 'w') as f:
            r = toml.dump(data, f)
            #log.log_info(f"{dst_file}(创建)写入成功")
    except Exception as e:
        print(e)
        #log.log_error(f"(创建)写入{dst_file}时捕获到异常:{e}")
    #dst_file为目标文件路径，目标文件夹下文件不存在时自动创建
    #data为字典类型

def suecodeexec(code):
    try:
        dst_file='./lib/toml/su/superadmin.toml'
        data = toml.load(dst_file)
        data['superadmin'][0]['emailcode'] = code
        dumptoml(dst_file=dst_file,data=data)
        t = threading.Thread(target=suclearecode)
        t.start()
    except Exception as e:
        print(e)
        #log.log_error(f"更新并写入num到config.toml时捕获到异常:{e}")
def suclearecode():
        time.sleep(60)
        dst_file = './lib/toml/su/superadmin.toml'
        data = toml.load(dst_file)
        data['superadmin'][0]['emailcode'] = ''
        dumptoml(dst_file=dst_file,data=data)




if __name__ == "__main__":
    print(readtomlsu())