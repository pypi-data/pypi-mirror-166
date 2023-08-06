from setuptools import setup

setup(
    name='mnft',
    version='0.1.0',    
    description='Model NFT Pytorch Lightning Callback',
    url='https://github.com/SharifElfouly/NFT-Pytorch-Callback',
    author='Sharif Elfouly',
    author_email='selfouly@gmail.com',
    license='BSD 2-clause',
    packages=['mnft'],
    install_requires=[
      'pytorch-lightning',                     
      'termcolor',                     
      'torch',                     
    ],

    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
