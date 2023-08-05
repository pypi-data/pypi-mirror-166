from setuptools import setup

setup(
    name='hadata',
    version='0.8.0',
    description='HiAcuity common Data Models',
    url='https://github.com/hiacuity/ha-data',
    author='Nayana Hettiarachchi',
    author_email='nayana@hiacuity.com',
    license='BSD 2-clause',
    packages=['hadata', 'hareqres'],
    install_requires=['mongoengine==0.23.1', 'pydantic==1.8.2'],
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