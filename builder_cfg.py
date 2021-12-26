# ------------------------------------->
# configuration for the building process
# ------------------------------------->

# compiler, tyipically gcc, clang
compiler = "gcc"

# flags for gcc -> compile process
cFlags = "-Wall -Werror -Wpedantic -Wextra"

# flags for gcc -> linking process
lFlags = ""

# in linux/unix typically there is no extension for executables
# in windows is generally used the ".exe"
execExtension = ""

# when building..
# True: the resulting files duplicate the same folder structure
# False: the resulting files are collected all together under one single folder
buildKeepFolderStructure = True

# print gcc commands
buildQuiet = False