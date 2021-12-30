# ------------------------------------->
# configuration for the building process
# ------------------------------------->

# compiler, tyipically gcc or clang
compiler = "gcc"

# flags for gcc -> compile process
cFlags = "-Wall -Werror -Wpedantic -Wextra"

# flags for gcc -> linking process
lFlags = ""

# print gcc commands
# True: do not print shell commands on the terminal
# False: print the shell commands on the terminal
beQuiet = True

# extension (suffix) for executables
# in linux/unix typically there is no extension for executables
# in windows is generally used the ".exe" extension
execExtension = ""

# replicate the folder structure on the build destination folder
# True: the resulting files duplicate the same folder structure
# False: the resulting files are collected all together under one single folder
keepFolderStructure = False

# destination for executable(s)
# this variable is depending on 'keepFolderStructure==True'
# True: place exec on build folder
# False: place exec on the relative folder
execOnBuildRoot = False