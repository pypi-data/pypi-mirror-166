import base64
def add(a,b):return a+b


def encode(filename):
    with open(filename , 'rb') as f:
        text = f.read()
    # print(text)
    ttt =  base64.b64encode(text)
    # print(ttt)
    # print(base64.b64decode(ttt))
    with open(filename+'.b64.txt','wb' ) as f:
        f.write(ttt)

def decode(filename):
    with open(filename , 'r') as f:
        text = f.read()
    de = base64.b64decode(text)
    # print(de)
    with open(filename+'.decode','wb' ) as f:
        f.write(de)


if __name__ == '__main__':
    decode(r'C:\Users\Administrator\Desktop\新建文件夹\dist\utils4file-1.0.0.tar.gz.b64.txt')