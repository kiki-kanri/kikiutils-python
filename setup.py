from setuptools import setup


setup(
    name = 'kiki_utils',
    classifiers = [
        'License :: Freely Distributable'
    ],
    packages = ['kikiutils'],
    include_package_data=True,
    zip_safe = True,
    version = '1.2.4',
    description = 'Utils functions',
    author = 'kiki-kanri',
    author_email = 'a470666@gmail.com',
    keywords = ['Utils'],
    install_requires = [
        'pillow',
        'requests',
        'bs4',
        'python-magic'
    ]
)
