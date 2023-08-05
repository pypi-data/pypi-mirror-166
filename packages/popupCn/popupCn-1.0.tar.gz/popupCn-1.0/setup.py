from setuptools import setup, find_packages

setup(
    name='popupCn',  # 包名
    version='1.0',  # 版本
    description="弹窗",  # 包简介
    long_description=open('README.md').read(),  # 读取文件中介绍包的详细内容
    include_package_data=True,  # 是否允许上传资源文件
    author='zplb',  # 作者
    author_email='felix995493zplb@126.com',  # 作者邮件
    maintainer='zplb',  # 维护者
    maintainer_email='felix995493zplb@126.com',  # 维护者邮件
    license='MIT License',  # 协议
    url='',  # github或者自己的网站地址
    packages=find_packages(),  # 包的目录
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # 设置编写时的python版本
    ],
    python_requires='>=3.7',  # 设置python版本要求
    install_requires=['easygui'],  # 安装所需要的库

)




