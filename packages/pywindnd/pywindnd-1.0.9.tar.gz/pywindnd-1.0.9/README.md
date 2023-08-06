# pywindnd

A widget of tkinter, windows drag icon & drop to load absolute file path.

## Installation

clone:

```
$ git clone https://github.com/D-Ayden/pywindnd.git
$ cd pywindnd
```

create & activate virtual env then install dependency:
with venv/virtualenv + pip:

```
$ python -m venv env  # use `virtualenv env` for Python2, use `python3 ...` for Python3 on Linux & macOS
$ source env/bin/activate  # use `env\Scripts\activate` on Windows
$ pip install -r requirements.txt or pip download -r requirements.txt
```

or with pdm:

```
$ pdm install
```

## Usage

```
try:
    import tkinter
except:
    import Tkinter as tkinter

import windnd

tk = tkinter.Tk()
windnd.drop_files(tk)
tk.mainloop()
```

若文件路径过深过长时，可手动调整 buffer 初始值

```
try:
    import tkinter
except:
    import Tkinter as tkinter

import windnd

tk = tkinter.Tk()
windnd.drop_files(tk, init=520)
tk.mainloop()
```
