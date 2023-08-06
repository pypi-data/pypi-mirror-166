from setuptools import setup, find_packages

setup(
    name='sparkxgb',
    version='0.1',
    description='sparkxgb module',
    url='',
    author='unk',
    author_email='unk@gmail.com',
    liscence='unk',
    packages=['sparkxgb'],
    zip_safe=False,
    install_requires=[
        'pyspark==3.1.1',
    ]
)
