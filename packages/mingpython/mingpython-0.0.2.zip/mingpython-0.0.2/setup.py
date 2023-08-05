from setuptools import setup,find_packages


setup(
    name='mingpython',
    version='0.0.2',
    packages=['mingpython'],
    py_modules=['Tool'],
    url='https://gitee.com/minglie/mingpython',
    author='minglie',
    author_email='934031452@qq.com',
    description='Automatically set package version from Git.',
    license='http://opensource.org/licenses/MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],

    install_requires=[],
)