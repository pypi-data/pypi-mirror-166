#! /usr/bin/env python
#_*_ coding:utf-8 _*_

from setuptools import setup, find_packages     # 这个包没有的可以pip一下

setup(
    name= "WorkFlow_HS_Utils",
    version= "0.1.0",
    keywords= ["pip","WorkFlow_HS_Utils"],
    description= "Allen.huang's private utils",
    license= "MIT Licence",

    url = "https://hs-personproject.coding.net/p/ttt/d/workflow/git",
    author="Allen.huang",
    author_email="fengyeyoni@163.com",
    packages= find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires = ["graphviz"]   # 这个项目依赖的第三方库
)