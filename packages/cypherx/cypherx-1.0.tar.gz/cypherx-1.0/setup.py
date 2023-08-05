from gettext import install
from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='cypherx',
    version='1.0',
    url='https://github.com/yuritorresf/cypherx',
    project_urls = {
        'Código fonte': 'https://github.com/yuritorresf/cypherx',
        'Download': 'https://github.com/yuritorresf/cypherx/archive/1.0.0.zip'
    },
    license='MIT',
    author='Yuri Torres',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='feereira@gmail.com',
    keywords='cypherx, package, cryptography, cryptography package',
    description='Ferramenta de criptografia e descriptografia de textos',
    packages=['cypherx'],
    install_requires=['argparse', 'rich'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization'
    ],
)