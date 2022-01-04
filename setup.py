from os import path as os_path
from setuptools import find_packages, setup

# import xenny

this_directory = os_path.abspath(os_path.dirname(__file__))

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]
# print(find_packages('.'))
setup(
    name='xenny',  # 包名
    python_requires='>=3.8.0', # python环境
    version='1.1',#xenny.__version__, # 包的版本
    description="Xenny's tool",  # 包简介，显示在PyPI上
    long_description=read_file('README.md'), # 读取的Readme文档内容
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    author="X3NNY", # 作者相关信息
    author_email='xennyxd1@gmail.com',
    url='https://github.com/X3NNY/xenny',
    # 指定包信息，还可以用find_packages()函数
    packages=find_packages('.'),
    install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    include_package_data=True,
    license="MIT",
    keywords=['ctf', 'xenny', 'web', 'misc', 'crypto', 'reverse', 'pwn'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
