from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wpcEXEbuild",
    version="0.0.1",
    description='WPC EXE builder',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="chunglee_people",
    author_email="wu@wpc.com.tw",
    # url="https://github.com/WPC-Systems-Ltd/WPC_PyPI_wpcEXEbuilder",
    packages=['wpcEXEbuild'],
    license='MIT',
    keywords='wpc, executable, standalone, packaging, app, apps, exe',
    install_requires=['pyinstaller>=5.3'],
    entry_points={
        'console_scripts': ['wpcEXEbuild=wpcEXEbuild.script:main'],
    },
    python_requires=">=3.10",
)
