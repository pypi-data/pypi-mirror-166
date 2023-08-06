from setuptools import find_packages, setup


setup(
    name='RubikCipherX',
    version='0.1',
    url='https://github.com/CipherX-B4ar3/rubikaLib',
    description='Rubika Lib python3',
    python_requires='>=3.9',
    packages=find_packages(exclude=['rubika*']),
    install_requires=['aiohttp', 'pycryptodome'],
)