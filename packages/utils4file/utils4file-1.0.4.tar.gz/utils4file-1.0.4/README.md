## 生成dist目录和egginfo
python setup.py sdist

## 上传pypi
twine upload --skip-existing dist/*

## 安装
pip install --upgrade utils4file -i https://pypi.org/simple