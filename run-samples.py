import os
from maker import Maker

mkr = Maker()
# mkr.load("samples/sample-multi-exe")
# print("Files to convert into objects:")
# mkr.printListSources()
# print("Files becoming executables:")
# mkr.printListExecs()
# print("Folders with header files to include:")
# mkr.printListIncludeFolders()
# print("Dependencies for each file:")
# mkr.printListDependencies()
# mkr.build("sample/build", run=False, clean=True)
# mkr.createMakefile("samples/sample-multi-exe/build")

samples = [
"sample-multi-exe",
"sample-no-exe",
"sample-one-exe",
"sample-one-exe-complex"]

try:

    for i, sample in enumerate(samples):
        print("*"*50)
        print(f"{i+1}. run: {sample}")
        path = f"samples/{sample}"
        build = f"{path}/build"

        # load source
        mkr.load(path)

        # create makefile
        mkr.createMakefile(build)

        # run make with that makefile
        os.system(f"cd {path} && make clean && make")

except Exception as ex:
    print(ex)
    exit(1)



    