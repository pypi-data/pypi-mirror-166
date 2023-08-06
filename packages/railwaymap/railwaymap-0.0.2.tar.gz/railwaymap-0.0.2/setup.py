
import setuptools

setuptools.setup(
    # 项目的名称
    name='railwaymap',
    #项目的版本
    version='0.0.2',
    # 项目的作者
    author='60464',
    # 作者的邮箱
    author_email='huanglujiang@126.com',
    # 项目描述
    description='中国铁路局地图可视化',
    # 项目的长描述
    long_description='基于中国地图的各路局管辖范围地图可视化包',
    # 以哪种文本格式显示长描述
    long_description_content_type='text/markdown',
    # 所需要的依赖
    install_requires=['pyecharts>=1.9.0'],  # 比如["flask>=0.10"]
    # 项目主页
    url="",
    # 项目中包含的子包，find_packages() 是自动发现根目录中的所有的子包。
    packages=setuptools.find_packages(),
    # 其他信息，这里写了使用 Python3，MIT License许可证，不依赖操作系统。
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)