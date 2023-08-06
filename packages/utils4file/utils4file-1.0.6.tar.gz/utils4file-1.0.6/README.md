## 生成dist目录和egginfo
python setup.py sdist

## 上传pypi
twine upload --skip-existing dist/*

## 安装
pip install --upgrade utils4file -i https://pypi.org/simple


## pypi登录 win10
%homepath%\.pypirc
```
[distutils] 
index-servers=pypi 
 
[pypi] repository = https://upload.pypi.org/legacy/ 
username = your account 
password = your path
```