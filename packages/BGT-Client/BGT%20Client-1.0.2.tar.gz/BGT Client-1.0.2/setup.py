from setuptools import setup
from setuptools import find_packages
from distutils.util import convert_path
main_ns={}
ver_path=convert_path("client/VER.py")

with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup( name="BGT Client",
        version=main_ns['__version__'],
        description = "This package provides a client for the BGT transaction family",
        author = "Misha Khvatov",
        author_email = "misha.khvatov@gmail.com",
        url="https://github.com/Mishark-dev/DGT-Client",
         entry_points={
            'console_scripts': [
                'bgtc = client.bgtc:main',
            ],
        },       
        exclude=["config"],
        packages=find_packages(),
        install_requires=['requests','ipaddress','cbor',
                          'protobuf==3.20','cryptography','configparser','secp256k1']

        )
