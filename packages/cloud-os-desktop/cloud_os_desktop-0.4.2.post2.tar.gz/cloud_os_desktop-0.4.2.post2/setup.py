#!/usr/bin/env python3
# -*- coding: utf-8 -*- 


"""
Инструкции:

python3 setup.py sdist bdist_wheel - Сборка пакета
sudo python3 setup.py develop - Установка пакета для разработки
sudo python3 setup.py develop -u - Uninstall
sudo pip3 install dist/cloud_os_desktop-1.2.0.tar.gz - Установка пакета
sudo pip3 uninstall cloud_os_desktop - Удаление пакета
python3 -m twine upload --repository pypi dist/* - Залить на сервер
twine upload -r pypi dist/* - Новая команда залить в pypi

Список классификации:
https://pypi.python.org/pypi?%3Aaction=list_classifiers
"""


from setuptools import setup, find_packages
from os.path import abspath, dirname, join

setup(
	name="cloud_os_desktop",
	version="0.4.2-2",
	description="Bayrell OS Desktop Client",
	long_description=open(join(abspath(dirname(__file__)), 'README.md'), encoding='utf-8').read(),
	long_description_content_type='text/markdown',
	author="Ildar Bikmamatov",
	author_email="ildar@bayrell.org",
	license="Apache License Version 2.0",
	url = "https://github.com/bayrell-os/desktop_client",
	packages=find_packages(),
	include_package_data = True,
	scripts=[
		'scripts/cloud_os_desktop'
	],
	install_requires=[
		'PyQt5',
		'PyQtWebEngine',
		'paramiko',
		'sshtunnel',
		'PyNaCl',
	],
	classifiers=[
		'Environment :: X11 Applications :: Qt',
		'License :: OSI Approved :: Apache Software License',
		'Operating System :: POSIX :: Linux',
		'Operating System :: Microsoft :: Windows :: Windows 10',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.8',
		'Topic :: Internet',
		'Topic :: System :: Operating System',
		'Topic :: Utilities',
	],
	keywords = [
		"bayrell", "bayrell cloud os", "bayrell desktop client"
	],
)