# NF06-ProjectManagement

This is the repository of the project we, Amine-jabote and TeddyRoncin, are creating for a subject called NF06, at the UTT university (France).
The objective of the project is to make a project management tool.

## Technologies used

We are using Python and C. The GUI is made with Pygame, a python library.

## How to install

### With binaries

To run this program, you simply need to download the right ZIP file in the release section, according to your operating system. Then, you need to extract the ZIP file, and run the executable file (it should be called main.exe or main, or something like that depending on your OS).

### Running from sources

First, download the source code, either from the releases section, or directly from this branch. You can also clone the repository with git (`git clone https://github.com/TeddyRoncin/NF06-ProjectManagement`).
You also need to install Python, which is the programming language we used to create this software.
You also need to install Pygame, which is a Python library that allows us to create a GUI. You can install it with pip (`pip install pygame`).
The project uses a C dependency. You need to compile it. You can for example do it with the following command : `gcc -o Core.{the_extension_of_your_platform} -shared -fPIC src/Core.c`
Replace `{the_extension_of_your_platform}` with the extension of your platform. For example, on Windows, you need to replace it with `dll`, on Linux, you need to replace it with `so`, and on macOS, you need to replace it with `dylib`.
You can now launch the project by launching the file `src/main.py`

### Installing from sources

To install this project from sources, you need to download the source code, Python and a C compiler (like gcc). More information are in the [Running from sources section](#running-from-sources).

You will need to install pyinstaller from pip (`pip install pyinstaller`)
Once this is done, open a command prompt, and go in the unzipped folder containing the sources.
Depending on your operating system, execute the appropriate commands. You may need to restart your computer first.

#### Linux

```bash
gcc -o Core.so -shared -fPIC src/Core.c
pyinstaller src/main.py
cp Core.so dist/main/Core.so
mkdir dist/main/data
mkdir dist/main/data/projects
cp -r assets dist/main/assets
```

#### Windows

```bash
gcc -o Core.dll -shared -fPIC src/Core.c
pyinstaller src/main.py
copy Core.dll dist\main\Core.dll
mkdir dist\main\data\projects
copy -r assets dist/main
```

Your executable should now be in `dist/main/`

## Issues

If you encounter any issues, let us know by creating an issue on GitHub.
