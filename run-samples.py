import os
from maker import Maker

def runOneSample():
    try:
        sampleDir = "samples/sample-multi-exe"
        buildDir = sampleDir + "/build"
        
        mkr = Maker()
        # load source
        mkr.load(sampleDir)
        print("Files to convert into objects:")
        mkr.printListSources()
        print("Files becoming executables:")
        mkr.printListExecs()
        print("Folders with header files to include:")
        mkr.printListIncludeFolders()
        print("Dependencies for each file:")
        mkr.printListDependencies()
        # compile
        mkr.build(buildDir, run=False, clean=True)
        # create makefile
        mkr.createMakefile(buildDir)

    except Exception as ex:
        print(ex)

def runAllSamples():
    samples = [
    "sample-multi-exe",
    "sample-no-exe",
    "sample-one-exe",
    "sample-one-exe-complex"]

    try:
        # the maker object
        mkr = Maker()

        for i, sample in enumerate(samples):
            print("*"*50)
            print(f"{i+1}. run: {sample}")
            sourceDir = f"samples/{sample}"
            buildDir = f"{sourceDir}/build"

            # load source
            mkr.load(sourceDir)

            # create makefile
            mkr.createMakefile(buildDir)

            # ..or build without the need of a makefile
            #mkr.build(build)

            # run make with that makefile
            cmd = f"cd {sourceDir} && make clean && make"
            print(cmd)
            os.system(cmd)

    except Exception as ex:
        print(ex)


runAllSamples()
#runOneSample()
