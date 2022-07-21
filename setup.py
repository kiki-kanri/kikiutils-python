import platform
import os

from setuptools import setup


install_requires = [
    'bs4',
    'numpy',
    'opencv-python',
    'pillow',
    'redis',
    'requests'
]

if os.name == 'nt':
    install_requires.append('python-magic-bin')
else:
    install_requires.append('python-magic')

python_version = platform.python_version()

print(f'Python version: {python_version}')

if '3.10' in python_version:
    install_dir = 'kikiutils-py310'
else:
    install_dir = 'kikiutils-py3'

os.rename(f'./{install_dir}', 'kikiutils')


setup(
    name = 'kiki_utils',
    classifiers = [
        'License :: Freely Distributable'
    ],
    packages = ['kikiutils'],
    include_package_data=True,
    zip_safe = True,
    version = '1.4.2',
    description = 'Utils functions',
    author = 'kiki-kanri',
    author_email = 'a470666@gmail.com',
    keywords = ['Utils'],
    install_requires = install_requires
)

os.rename('kikiutils', f'./{install_dir}')
