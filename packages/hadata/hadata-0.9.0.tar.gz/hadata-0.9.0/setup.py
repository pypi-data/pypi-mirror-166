from setuptools import setup

setup(
    name='hadata',
    version='0.9.0',
    description='HiAcuity common Data Models',
    url='https://github.com/hiacuity/ha-data',
    author='Nayana Hettiarachchi',
    author_email='nayana@hiacuity.com',
    license='BSD 2-clause',
    packages=['hadata', 'hareqres', 'hautils'],
    install_requires=['mongoengine==0.23.1', 'pydantic==1.8.2', "boto3~=1.20.0", "botocore~=1.23.1", "python-dotenv~=0.20.0", 'pika~=1.2.0'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)