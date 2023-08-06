
"""
* 作者：王若宇
* 时间：2022/1/25 14:00
* 功能：打包Python软件包用于发布到pypi.org
* 说明：请看读我.txt，库发布后可使用学而思库管理工具下载
"""
import sys

from setuptools import setup
from xes import AIspeak

if __name__ == '__main__':
    sys.argv += ["sdist"]
setup(
    name='wryColorfulButtons',
    version='0.0.1',
    packages=['wryColorfulButtons'],
    url='http://wry.ljcsunrise.tech/wp',
    license='MIT License',
    author='Ruoyu Wang',
    author_email='wry_beiyong12@outlook.com',
    description='ttkbootstrap彩色按钮/' + AIspeak.translate('ttkbootstrap彩色按钮'),
    long_description='ttkbootstrap彩色按钮/' + AIspeak.translate('ttkbootstrap彩色按钮'),
    requires=["ttkbootstrap",]
)

