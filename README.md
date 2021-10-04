# fish_recognition
海洋鱼类识别系统

# 一.项目介绍

此项目基于paddlex的图片分类（ResNet50）和语义分割模块（FastSCNN）对输入的海洋鱼类图片进行名称识别和边界预测并输出，使用pyqt5 python GUI实现



# 二.部署

1.下载代码到本地

```
git clone git@github.com:OsLeon/fish_recognition.git
```

2.安装pyqt5和依赖组件

```
pip install pyqt5 -y
```
3.运行前需要把模型放入根目录下

4.启动程序：

在根目录目录下运行以下代码启动后端：

```
python Ui_MainWindow.py
```
