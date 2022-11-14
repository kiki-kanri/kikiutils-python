from setuptools import find_packages, setup


install_requires = [
    'loguru'
]

setup(
    name='kiki_utils_base',
    classifiers=[
        'License :: Freely Distributable'
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    version='1.0.0',
    description='Utils functions without other packages',
    author='kiki-kanri',
    author_email='a470666@gmail.com',
    keywords=['Utils'],
    install_requires=install_requires,
    python_requires=">=3.6"
)
