from setuptools import setup


setup(
    name='Torch Client',
    packages=['torchclient'],
    scripts=['run_client.py'],
    include_package_data=True,
    install_requires=[
        'tornado',
        'xtermcolor',
    ],
)
