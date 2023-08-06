from setuptools import setup, find_packages


setup(
    name='lord_kumaresh',
    version='0.6',
    license='MIT',
    author="kumaresh ",
    author_email='kk8180183@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/kumaresh-rgb/example-publish-pypi',
    keywords='addiction',
    install_requires=[
          'scikit-learn',
      ],

)