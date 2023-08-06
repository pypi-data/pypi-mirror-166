#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='rustdeskauto',
    version='1.0.0',
    description=(
        'rustdesk远程桌面自动化'
    ),
    author='mrj',
    author_email='806189218@qq.com',
    maintainer='jzk',
    maintainer_email='806189218@qq.com',
    license='BSD License',
    packages=find_packages(),
    install_requires=['pyautogui', 'pywinauto', 'requests', 'pywin32'],
    platforms=["all"],
    url='https://github.com/Mr-J-J/shouhou',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)