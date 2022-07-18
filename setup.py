import os

from setuptools import setup


install_requires = [
    'bs4',
    'numpy',
    'opencv-python',
    'pillow',
    'requests',
]

if os.name == 'nt':
    install_requires.append('python-magic-bin')
else:
    install_requires.append('python-magic')


setup(
    name = 'kiki_utils',
    classifiers = [
        'License :: Freely Distributable'
    ],
    packages = ['kikiutils'],
    include_package_data=True,
    zip_safe = True,
    version = '1.3.2',
    description = 'Utils functions',
    author = 'kiki-kanri',
    author_email = 'a470666@gmail.com',
    keywords = ['Utils'],
    install_requires = install_requires
)
