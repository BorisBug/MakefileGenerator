
from pathlib import Path
import os

class Builder:
    def __init__(self) -> None:
        self._cFiles = []
        self._exeFiles = []
        self._folders = []
        self._deps = {}
        self._paths = {}
        
    def load(self, pathOrigin="."):
        pathOrigin = Path(pathOrigin)
        self._cFiles.clear()
        self._exeFiles.clear()
        self._folders.clear()
        self._deps.clear()
        self._paths.clear()

        # scan recursively the complete folder tree
        def scanOriginFolder():
            for path in pathOrigin.rglob("*"):
                # if is a file...
                if path.is_file():
                    # collect all the .c files
                    if path.suffix==".c": 
                        self._cFiles.append(path.name)
                        self._deps[path.name] = []
                        self._paths[path.name] = path
                    # collect all the .h files
                    elif path.suffix==".h": 
                        self._deps[path.name] = []
                        self._paths[path.name] = path
                # if is a folder...
                elif path.is_dir():
                    # collect only if contains .h files
                    for x in path.glob("*.h"):
                        if x.is_file():
                            self._folders.append(str(path))
                            break
        
        # load dependency tree
        def buildDependencyTree():

            # is going to be an executable (link!)
            def isExe(path):
                content = ""
                with open(path, "r") as f:
                    content = f.read()
                return content.find(" main(")>=0

            # get the list of #include files 
            def getIncludedDeps(path):
                content = ""
                with open(path, "r") as f:
                    content = f.read()

                deps = []
                include = '#include "'
                pos1 = content.find(include)
                while pos1>=0:
                    pos1 += len(include)
                    pos2 = content.find('"', pos1)
                    assert pos2>=0
                    depName = content[pos1:pos2]
                    deps.append(depName)
                    pos1 = content.find(include, pos2+1)

                depextra = []
                for dep in deps:
                    if dep in self._paths:
                        depextra += getIncludedDeps(self._paths[dep])
                    else:
                        # include out of the folder structure
                        pass
                return deps + depextra
        
            # deps for .c files
            for cFile in self._cFiles:

                # if it will become executable, save it for the linking process
                path = self._paths[cFile]
                if isExe(path):
                    self._exeFiles.append(cFile)

                # every .c file generates an .o file and a dependency
                obj = cFile.replace(".c",".o")
                self._deps[obj] = [cFile]
                self._paths[obj] = Path(str(path).replace(".c",".o"))

                # load it's .h dependencies
                self._deps[cFile] = getIncludedDeps(path)

            # deps for exe files
            for cFile in self._exeFiles:

                skip = []

                def getDepDeps(cFileName:str):
                    nonlocal skip
                    deps = []
                    if cFileName in skip:
                        return deps
                    skip += [cFileName]
                    for name in self._deps[cFileName]:
                        name = str(name)
                        if name.find(".h")>=0:
                            src = name.replace(".h", ".c")
                            if src in self._deps:
                                obj = name.replace(".h", ".o")
                                if obj not in deps:
                                    deps += [obj]
                                for obj in getDepDeps(src):
                                    if obj not in deps:
                                        deps += [obj] 
                    return deps

                exeName = cFile.replace(".c",".exe")
                objName = cFile.replace(".c",".o")
                self._deps[exeName] = [objName]
                self._paths[exeName] = Path(str(self._paths[cFile]).replace(".c",".exe"))

                deps = getDepDeps(cFile)
                self._deps[exeName] += deps
    
        scanOriginFolder()
        buildDependencyTree()
        
    def printListSources(self):
        print("Files to convert into objects:")
        for name in self._cFiles:
            print(self._paths[name])
        print()

    def printListExecs(self):
        print("Files becoming executables:")
        for name in self._exeFiles:
            print(self._paths[name])
        print()

    def printListIncludeFolders(self):
        print("Folders for include flag:")
        for path in self._folders:
            print(path)
        print()
    
    def printListDependencies(self):
        print("Dependencies for each file:")
        for dep in self._deps:
            print(f"{dep} -> {self._deps[dep]}")
        print()
    
    def build(self, pathBuild="build", cFlags="-Wall -Werror -Wextra -Wpedantic", lFlags="", run=True):

        incFlag = ""

        def gccCompile(cFile:str):
            def getIncludeFlag():
                nonlocal incFlag
                if incFlag !="":
                    return incFlag

                for dir in self._folders: 
                    incFlag += " -I./" + dir
                return incFlag

            inc = getIncludeFlag()
            out = str(Path(pathBuild, cFile.replace(".c",".o")))
            src = self._paths[cFile]
            gcc = f"gcc {cFlags} -c {src} {inc} -o {out}"
            gcc = gcc.replace("  ", " ")
            return gcc

        def gccLink(cFile:str):
            def getBuildObjs(exeName):
                    objs = ""
                    for obj in self._deps[exeName]:
                        objs += str(Path(pathBuild, obj)) + " "
                    return objs.strip()

            exeName = cFile.replace(".c",".exe")
            out = Path(pathBuild, exeName)
            objs = getBuildObjs(exeName)
            gcc = f"gcc {objs} {lFlags} -o {out}"
            return gcc.replace("  ", " ")

        print("Build all:")

        # create build bolder
        if not os.path.isdir(pathBuild):
            os.makedirs(pathBuild)

        # compile -> create object files
        for cFile in self._cFiles:
            gcc = gccCompile(cFile)
            print(gcc)
            os.system(gcc)

        # link -> create executable files
        for cFile in self._exeFiles:
            gcc = gccLink(cFile)
            print(gcc)
            os.system(gcc)

        # run all executables
        if run:
            for cFile in self._exeFiles:
                exeName = cFile.replace(".c",".exe")
                exePath = Path(pathBuild, exeName)
                print()
                print(f"Running {exeName}...")
                os.system(f"./{exePath}")


print("\n"*20)
b = Builder()
b.load("sample")
b.printListSources()
b.printListExecs()
b.printListIncludeFolders()
b.printListDependencies()
b.build("sample/build", run=True)
#b.createMakefile(".", "./build")
