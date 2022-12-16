# NF06-ProjectManagement

This is the repository of the project we, Amine-jabote and TeddyRoncin, are creating for a subject called NF06, at the UTT university (France).
The objective of the project is to make a project management tool.

## Technologies used

We are using Python and C. The GUI is made with Pygame, a python library.

## How to install

### With binaries

To run this program, you simply need to download the ZIP file in the release section. Then, you need to extract the ZIP file, and run the executable file.  
NOTE : This section is empty for the moment, the project is not finished yet

### Running from sources

First, download the source code, either from the releases section, or direcly from this branch. You can also clone the repository with git (`git clone https://github.com/TeddyRoncin/NF06-ProjectManagement`).
You also need to install Python, which is the programming language we used to create this software
You can now lauch the project by launching the file src/main.py

### Installing from sources

To install this project from sources, you need to download the source code and Python. More information are in the Running from sources section.

You will need to install pyinstaller from pip.
Once this is done, open a command prompt, and go in the unzipped folder containing the sources.
Depending on your operating system, execute the appropriate commands. You may need to restart your computer first.

#### Linux

```bash
pyinstaller src/main.py
cp Core.so dist/main/Core.so
mkdir dist/main/data
```

#### Windows

```bash
pyinstaller src/main.py
copy Core.dll dist\main\Core.dll
mkdir dist\main\data
```

Your executable should now be in `dist/main/`

## Issues

If you encounter any issues, let us know by creating an issue on GitHub.
