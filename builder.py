
import os
import shutil
from pathlib import Path
import builder_cfg as cfg


class Builder:
    def __init__(self) -> None:
        self._origin = Path()
        self._srcs = []
        self._execs = []
        self._folders = []
        self._deps = {}
        self._paths = {}
        self._tstamps = {}
        
    def load(self, path="."):
        self._origin = Path(path)
        self._srcs.clear()
        self._execs.clear()
        self._folders.clear()
        self._deps.clear()
        self._paths.clear()
        self._tstamps.clear()

        # scan recursively the complete folder tree
        def scanOriginFolder():
            for path in self._origin.rglob("*"):
                # if is a file...
                if path.is_file():
                    # collect all the .c files
                    if path.suffix==".c": 
                        self._srcs.append(path.name)
                        self._paths[path.name] = path
                    # collect all the .h files
                    elif path.suffix==".h": 
                        self._paths[path.name] = path
                # if is a folder...
                elif path.is_dir():
                    # collect only if contains .h files
                    for x in path.glob("*.h"):
                        if x.is_file():
                            self._folders.append(str(path))
                            break

        # load the timestamps for each collected file
        def loadTimestamps():
            for name in self._paths:
                self._tstamps[name] = os.path.getmtime(self._paths[name])

        # load dependency tree
        def loadDependencies():

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
                    if pos2<0:
                        # something wrong with the syntax
                        # TODO raise an exception
                        break
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
            for cFile in self._srcs:
                # if it will become executable, save it for the linking process
                path = self._paths[cFile]
                if isExe(path):
                    self._execs.append(cFile)

                # every .c file generates an .o file
                obj = path.stem + ".o"
                self._deps[obj] = [cFile] + getIncludedDeps(path)
                self._paths[obj] = Path(path.parent, obj)

            # deps for exe files
            for cFile in self._execs:
                deps = []
                def getDeps(obj:str):
                    nonlocal deps
                    for name in self._deps[obj]:
                        obj = Path(name).stem + ".o"
                        if obj in self._deps and obj not in deps:
                            deps.append(obj)
                            for obj in getDeps(obj):
                                if obj not in deps:
                                    deps.append(obj)
                    return deps
                objName = Path(cFile).stem + ".o"
                exeName = Path(cFile).stem + cfg.execExtension
                self._deps[exeName] = getDeps(objName)
                self._paths[exeName] = Path(self._paths[cFile].parent, exeName)
    
        scanOriginFolder()
        loadTimestamps()
        loadDependencies()
        
    def printListSources(self):
        for name in self._srcs:
            print(self._paths[name])
        print()

    def printListExecs(self):
        for name in self._execs:
            print(self._paths[name])
        print()

    def printListIncludeFolders(self):
        for path in self._folders:
            print(path)
        print()

    def printListDependencies(self):
        for dep in self._deps:
            print(f"{dep} -> {self._deps[dep]}")
        print()
    
    def build(self, pathBuild="build", run=True, clean=True):

        incFlag = ""
        pathBuild = Path(pathBuild)

        def getBuildRelativePath(file:str, newSuffix=""):
            nonlocal pathBuild
            newName = Path(file).stem + newSuffix

            if(cfg.buildKeepFolderStructure):
                if pathBuild.is_relative_to(self._origin):
                    path = Path(self._origin, pathBuild.relative_to(self._origin), self._paths[file].relative_to(self._origin).parent, newName)
                else:
                    path = Path(pathBuild, self._paths[file].parent, newName)
            else:
                path = Path(pathBuild, newName)

            # create folder structure
            if not os.path.isdir(path.parent):
                os.makedirs(path.parent)
                
            return path

        def gccCompile(cFile:str):
            def getIncludeFlag():
                nonlocal incFlag
                if incFlag !="":
                    return incFlag

                for dir in self._folders: 
                    incFlag += " -I./" + dir
                return incFlag
                
            inc = getIncludeFlag()            
            obj = getBuildRelativePath(cFile, ".o")
            src = self._paths[cFile]
            return f"{cfg.compiler} {cfg.cFlags} -MMD -c {src} {inc} -o {obj}".replace("  ", " ")

        def gccLink(cFile:str):
            def getBuildObjs(exeName):               
                objs = ""
                for cFile in self._deps[exeName]:
                    objs += str(getBuildRelativePath(cFile, ".o")) + " "
                return objs.strip()

            out = getBuildRelativePath(cFile, cfg.execExtension)
            objs = getBuildObjs(Path(cFile).stem + cfg.execExtension)
            return f"{cfg.compiler} {objs} {cfg.lFlags} -o {out}".replace("  ", " ")

        def loopFiles(files, action):
            for file in files:
                cmd = action(file)
                if not cfg.buildQuiet:
                    print(cmd)
                os.system(cmd)

        # remove build folder
        if clean and pathBuild.is_dir() and pathBuild.cwd()!=pathBuild.absolute():
            shutil.rmtree(pathBuild, ignore_errors = True)

        # compile -> create object files
        loopFiles(self._srcs, gccCompile)

        # link -> create executable files
        loopFiles(self._execs, gccLink)

        # run all executables
        if run:
            for cFile in self._execs:
                exePath = getBuildRelativePath(cFile, cfg.execExtension)
                if not cfg.buildQuiet:
                    print()
                    print(f"Running {exePath.name}...")
                os.system(f"./{exePath}")

    def createMakefile(self, pathBuild="./build"):
        pathBuild = Path(pathBuild)
        if pathBuild.is_relative_to(self._origin):
            pathBuild = pathBuild.relative_to(self._origin)

        execs = sources = objectx = objects = phony = ""
        build = targets = tgtmenu = runall = info = ""        
        q = "@" if cfg.makeQuiet else "" 

        for i, cFile in enumerate(self._execs):
            objs = ""
            exeName = Path(cFile).stem + cfg.execExtension
            for cFileDep in self._deps[exeName]:
                objs += str(self._paths[cFileDep]).replace(".o",".c").replace(str(self._origin)+"/", "") + " "

            i += 1
            exec = f"$(BUILD_DIR)/$(EXEC{i})"
            stem = Path(cFile).stem
            execs += f"EXEC{i} := {stem}\n" 
           #sources += f"SRC{i} := $(shell find $(SRC_DIRS) -name '*.c')\n"
            sources += f"SRC{i} := {objs}\n"
            objectx += f"OBJS{i} := $(SRC{i}:%=$(BUILD_DIR)/%.o)\n" 
            objects += f"$(OBJS{i}) "
            build += exec + " "
            runall += f"\t{q}./{exec}\n"
            targets += f"# target: {stem}\n{exec}: $(OBJS{i})\n\t{q}$(CC) $^ $(LFLAGS) -o $@\n\n"
            tgtmenu += f'{stem}: {exec}\n\t@echo "{"*"*50}"\n\t@echo "Running {stem}..."\n\t@echo "{"*"*50}"\n\t{q}./{exec}\n\n'
            phony += stem + " "
            info += f'\t@echo "{stem}: to run {stem}"\n'
        make = f"""#{'-'*50}>
# makefile autogenerated by python script
# customize it following your own needs <3
#{'-'*50}>

# executable(s)
{execs.strip()}

# folders
BUILD_DIR := {pathBuild}
SRC_DIRS := .

# compiler / linker
CC := {cfg.compiler}

# sources
{sources.strip()}

# objects
{objectx.strip()}
OBJS := {objects.strip()}

# folders to include on compilation time
INC_DIRS := $(shell find $(SRC_DIRS) -type d)
INC_FLAGS := $(addprefix -I,$(INC_DIRS))

# flags for compilation & linking
CFLAGS := -MMD -MP {cfg.cFlags}
LFLAGS := {cfg.lFlags}

# targets ------------------>

# build all
build: {build.strip()}

# run all
run: build
\t{runall.strip()}

{targets.strip()}

# targets for each object
$(BUILD_DIR)/%.c.o: %.c
\t{q}mkdir -p $(dir $@)
\t{q}$(CC) $(CFLAGS) $(INC_FLAGS) -c $< -o $@

.PHONY: clean build run {phony.strip()} info

{tgtmenu.strip()}

info:
\t@clear
\t@echo \"{'*'*20} Targets {'*'*21}\"
\t@echo \"info: to print this menu\"
\t@echo \"build: to compile and link all sources (default)\"
\t@echo \"run: to run all the executables\"
\t{info.strip()}
\t@echo \"clean: to remove the {pathBuild} folder\"
\t@echo \"{'*'*50}\"
\t@echo \"\"

clean:
\t{q}rm -rf $(BUILD_DIR)

-include $(OBJS:.o=.d)\n"""
        Path(self._origin, "Makefile").write_text(make)



# make some space :p
print("\n"*20)

b = Builder()
b.load("sample")
"""
print("Files to convert into objects:")
b.printListSources()
print("Files becoming executables:")
b.printListExecs()
print("Folders with header files to include:")
b.printListIncludeFolders()
"""
print("Dependencies for each file:")
b.printListDependencies()
b.build("sample/build", run=False, clean=True)
b.build("sample/build2", run=False, clean=True)
b.build("sample2/build", run=False, clean=True)
b.createMakefile("sample/build")
b.createMakefile("sample/build2")
b.createMakefile("sample2/build")
