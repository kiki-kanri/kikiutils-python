from setuptools import find_packages, setup


setup(
    name='kiki_utils',
    classifiers=[
        'License :: Freely Distributable'
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    version='1.1.0',
    description='Utils functions without cv2 and pillow',
    author='kiki-kanri',
    author_email='a470666@gmail.com',
    keywords=['Utils'],
    install_requires=[
        'aiofiles',
        'loguru',
        'pycryptodomex',
        'pyopenssl',
        'python-magic;platform_system=="Linux"',
        'python-magic-bin;platform_system=="Windows"',
        'requests'
    ],
    python_requires=">=3.6"
)
