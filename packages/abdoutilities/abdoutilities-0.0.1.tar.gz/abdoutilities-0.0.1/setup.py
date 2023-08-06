from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='abdoutilities',
    version='0.0.1',
    description='Various abdoutilities, displaying a random quote',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Abdelkhalik Mosa',
    author_email='abdelkhalik.mosa@yahoo.com',
    license='MIT',
    classifiers=classifiers,
    keywords='random quotes',
    packages=find_packages(),
    install_requires=['']
)