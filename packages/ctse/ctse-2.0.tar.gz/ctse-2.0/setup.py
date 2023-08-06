
from setuptools import setup, find_packages


setup(
    name='ctse',
    version='2.0',
    license='MIT',
    author="Gilaxy GEOLOUP",
    author_email='franckiebbb@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/franck403/stce',
    keywords='word checker',
    install_requires=[
          'scikit-learn',
      ],

)