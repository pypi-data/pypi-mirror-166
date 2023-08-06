import base64
import hashlib

def add(a,b):
    return a+b

# 编码 70M1秒完成
def encode(filename):
    with open(filename , 'rb') as f:
        text = f.read()
    ttt =  base64.b64encode(text)
    with open(filename+'.b64.txt','wb' ) as f:
        f.write(ttt)

def decode(filename):
    with open(filename , 'r') as f:
        text = f.read()
    de = base64.b64decode(text)
    # print(de)
    with open(filename+'.decode','wb' ) as f:
        f.write(de)


 
def md5(file_name):
    """
    计算文件的md5
    :param file_name:
    :return:
    """
    m = hashlib.md5()   #创建md5对象
    with open(file_name,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  #更新md5对象
 
    return m.hexdigest()    #返回md5对象


if __name__ == '__main__':
    a = md5(r'C:\Users\Administrator\Desktop\新建文件夹\dist\utils4file-1.0.4.tar.gz')
    print(a)