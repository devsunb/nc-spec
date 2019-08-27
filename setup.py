from setuptools import setup, find_packages

with open('VERSION', mode='r') as f:
    VERSION = f.readline().strip()

setup(
    name='img_val_helper',
    version=VERSION,
    description='Image data validation helper',
    author='Lee Jaeseok',
    author_email='leejs@satreci.com',
    packages=find_packages(exclude=['test']),
    setup_requires=[],
    zip_safe=False,
    install_requires=['argparse', 'numpy', 'matplotlib',
                      'scipy', 'h5py', 'netCDF4', 'openpyxl']
)
