from distutils.core import setup

setup(
    name='gridfscmd',
    version='0.1.0',
    packages=['gridfsOps'],
    url='https://github.com/alrouen/gridfscmd',
    license='',
    author='alrouen',
    author_email='',
    description='Command line tool to interact with MongoDB GridFs',
    install_requires = ["hurry.filesize==0.9", "pymongo=3.4.0"]
)
