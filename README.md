# MakefileGenerator

A very simple makefile generator script for C code.

This script contains an object that is capable of collecting all the source files within any folder structure. It generates a standard GNU makefile, with targets and dependencies. It scans the files for the 'main' function(s) and with that generates the executables.

It is possible to customize via a configuration file. Read the file 'maker.ini' for more details.

As a side effect, this script also offers the possibility to compile, link and run all executables.

It is still a "work in progress" and it is not intended for professional use.
..I was just tired of writing makefiles and decided to make an automatic "smart" generator.
