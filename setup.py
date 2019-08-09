from setuptools import find_packages, setup

setup(
    name='process-ni-io-trace',
    version='1.0.0',
    description='Convert NI IO Trace Capture.txt files into easier to parse SCPI list files',
    long_description=open('README.md').read().strip(),
    author='Nick Lalic',
    author_email='nick.lalic@gmail.com',
    url='http://path-to-my-packagename',
    py_modules=['process_ni_io_trace'],
    packages=find_packages(exclude=['test']),
    install_requires=[],
    extras_require={
    'dev':  [],
    'test': []
    },
    license='MIT License',
    zip_safe=False,
    keywords='RF instrument SCPI NI VISA',
    classifiers=['Packages', 'RF'],
    entry_points={
    'console_scripts': [
        'process-ni-io-trace=process_ni_io_trace.bin.process_ni_io_trace:main'
    ]
    })
