## Installation

Install `wpcEXEbuild` from PyPI:

```
$ pip install wpcEXEbuild
```

## Quick Start

Open a command prompt/shell window, and navigate to the directory where your .py file is located, then build your app with the following command:

```
$ wpcEXEbuild your_program.py
```

wpcEXEbuild will generate a `.spec` file. You can run it at first.
If you want to add something such as icon or picture, you can edit your .spec file.

- Use wpcEXEbuild for one file

```
$ wpcEXEbuild your_program.py
```

- Use .spec file

```
pyinstaller main.spec
```
