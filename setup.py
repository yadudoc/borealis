from setuptools import setup, find_packages

with open('borealis/version.py') as f:
    exec(f.read())

with open('requirements.txt') as f:
    install_requires = f.readlines()

# tests_require = parse_requirements('test-requirements.txt')

setup(
    name='borealis',
    version=VERSION,
    description='Fast Python',
    long_description='Python at scale',
    url='https://github.com/yadudoc/borealis',
    author='Yadu Nand Babuji',
    author_email='yadudoc1729@gmail.com',
    license='Apache 2.0',
    download_url='https://github.com/yadudoc/borealis/archive/{}.tar.gz'.format(VERSION),
    package_data={'': ['LICENSE']},
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        # Maturity
        'Development Status :: 3 - Alpha',
        # Intended audience
        'Intended Audience :: Developers',
        # Licence, must match with licence above
        'License :: OSI Approved :: Apache Software License',
        # Python versions supported
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['Scientific computing'],
)
