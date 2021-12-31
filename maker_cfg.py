# ------------------------------------->
# configuration for the building process
# ------------------------------------->

# compiler, tyipically gcc or clang
compiler = "gcc"

# flags for gcc (compile process)
# added to CFLAGS
cFlags = "-Wall -Werror -Wpedantic -Wextra -MMD -MP"

# flags for gcc (linking process)
# added to LDFLAGS
ldFlags = ""

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
# False: the resulting files are all together under one single destination folder
keepFolderStructure = False

# destination for executable(s)
# this variable is depending on 'keepFolderStructure==True'
# True: place executable(s) on build folder
# False: place executable(s) on each relative folder
execOnBuildRoot = False