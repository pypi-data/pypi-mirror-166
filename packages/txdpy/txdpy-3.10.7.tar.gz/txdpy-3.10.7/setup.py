from distutils.core import setup

packages = ['txdpy']# 唯一的包名
setup(name='txdpy',
	version='3.10.7',
	author='tangxudong',
    packages=packages,
    package_dir={'requests': 'requests'},)
