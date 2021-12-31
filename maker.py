import os
import shutil
from pathlib import Path
import maker_cfg as cfg


class Maker:
    def __init__(self) -> None:
        self._origin = Path()
        self._srcs = []
        self._execs = []
        self._folders = []
        self._deps = {}
        self._paths = {}
        
    def load(self, path="."):
        self._origin = Path(path)
        self._srcs.clear()
        self._execs.clear()
        self._folders.clear()
        self._deps.clear()
        self._paths.clear()

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
            print(f"{dep} -> {' '.join(self._deps[dep])}")
        print()
    
    def build(self, pathBuild="build", run=True, clean=True):

        # ensure a type Path
        pathBuild = Path(pathBuild)

        # temp variables for the build process
        incFlag = ""
        relPaths = {}
        timeStamps = {}
        fileCounter = 0

        def getBuildRelativePath(file:str, newSuffix=""):
            nonlocal pathBuild
            newName = Path(file).stem + newSuffix

            if newName in relPaths:
                path = relPaths[newName]
            else:
                if(cfg.keepFolderStructure and (newSuffix!=cfg.execExtension or not cfg.execOnBuildRoot)):
                    path = self._paths[file].relative_to(self._origin)
                    if pathBuild.is_relative_to(self._origin):
                        path = Path(self._origin, pathBuild.relative_to(self._origin), path.parent, newName)
                    else:
                        path = Path(pathBuild, path.parent, newName)
                else:
                    path = Path(pathBuild, newName)
                # create folder structure
                if not os.path.isdir(path.parent):
                    os.makedirs(path.parent)
                
                relPaths[newName] = path
            
            return path

        def getCmdCompile(cFile:str):
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
            return f"{cfg.compiler} -c {src} {cfg.cFlags} {inc} -o {obj}".replace("  ", " ")

        def getCmdLink(cFile:str):
            def getBuildObjs(exeName):
                objs = ""
                for oFile in self._deps[exeName]:
                    objs += str(getBuildRelativePath(oFile, ".o")) + " "
                return objs

            out = getBuildRelativePath(cFile, cfg.execExtension)
            objs = getBuildObjs(Path(cFile).stem + cfg.execExtension)
            return f"{cfg.compiler} {objs} {cfg.ldFlags} -o {out}".replace("  ", " ")

        def getTimestamp(path):
            stamp = 0.0
            if path in timeStamps:
                stamp = float(timeStamps[path])
            if stamp == 0.0:
                stamp = 0.0 if not os.path.isfile(path) else os.path.getmtime(path)
                timeStamps[path] = stamp
            return stamp

        # remove build folder
        if clean and pathBuild.is_dir() and pathBuild.cwd()!=pathBuild.absolute():
            shutil.rmtree(pathBuild, ignore_errors = True)

        # compile -> create object files
        for cFile in self._srcs:
            oName = Path(cFile).stem + ".o"
            stampObj = getTimestamp(getBuildRelativePath(cFile, ".o"))
            for xFile in self._deps[oName]:
                # filter files that are not inside the folder structure
                if xFile in self._paths:
                    stampDep = getTimestamp(self._paths[xFile])
                    if stampObj<stampDep:
                        cmd = getCmdCompile(cFile)
                        if not cfg.beQuiet:
                            print(cmd)
                        errCode = os.system(cmd)
                        if errCode!=0:
                            raise Exception(f"Error during compilation process (code:{errCode})")
                        fileCounter += 1
                        break

        # link -> create executable files
        for cFile in self._execs:
            exeName = Path(cFile).stem + cfg.execExtension
            stampExe = getTimestamp(getBuildRelativePath(cFile, cfg.execExtension))
            for oFile in self._deps[exeName]:
                # filter files that are not inside the folder structure
                if oFile in self._paths:
                    stampObj = getTimestamp(getBuildRelativePath(oFile, ".o"))
                    if stampExe<stampObj:
                        cmd = getCmdLink(cFile)
                        if not cfg.beQuiet:
                            print(cmd)
                        errCode = os.system(cmd)
                        if errCode!=0:
                            raise Exception(f"Error during linking process (code:{errCode})")
                        fileCounter += 1
                        break
        
        if fileCounter<=0 and not cfg.beQuiet:
            print("Nothing to build, all dependencies are up-to-date.")
        
        # run all executables
        if run:
            for cFile in self._execs:
                exePath = getBuildRelativePath(cFile, cfg.execExtension)
                if not cfg.beQuiet:
                    print()
                    print(f"Running {exePath.name}...")
                errCode = os.system(f"./{exePath}")
                if errCode!=0:
                    # should i do something here?
                    pass

    def createMakefile(self, pathBuild="build"):
        def fullReplace(string:str, fromStr:str, toStr:str):
            while string.find(fromStr)>=0:
                string = string.replace(fromStr, toStr)
            return string
        def getAsMultiline(label, enum):
            multi = ""
            line = label 
            for item in enum:
                if len(line + " " + item)>70:
                    multi += line + " \\\n"
                    line = "\t" + item
                else:
                    line += " " + item
            multi += line + "\n"
            return multi

        pathBuild = Path(pathBuild)
        if pathBuild.is_relative_to(self._origin):
            pathBuild = pathBuild.relative_to(self._origin)

        build = []
        phony = ["help", "build"]
        execs = sources = objects = objx = ""
        tgtobjs = tgtexes = tgtmenu = runall = ""

        help = []
        help.append(f"\t@clear")
        help.append(f"\t@echo '{'*'*20} Targets {'*'*21}'")
        help.append(f"\t@echo 'help: to print this menu'")
        help.append(f"\t@echo 'build: to compile {'and link ' if len(self._execs)>0 else ''}all sources (default)'")
        
        # the quiet/verbose mode        
        q = "@" if cfg.beQuiet else ""

        if len(self._execs)<=1:
            sources += f"SRCS := $(shell find $(SOURCE) -name '*.c')\n"
            if cfg.keepFolderStructure:
                objects += f"OBJS := $(SRCS:%.c=$(BUILD)/%.o)\n"
            else:
                objects += f"OBJS := $(addprefix $(BUILD)/, $(notdir $(SRCS:%.c=%.o)))\n" 
        if len(self._execs)<=0:
            build.append("$(OBJS)")

        if len(self._execs)>0:
            phony.append("run")
            help.append("\t@echo 'run: to run all the executables'")

        for i, file in enumerate(self._execs):
            stem = Path(file).stem
            exeName = stem + cfg.execExtension
            if len(self._execs)==1:
                execN = "EXEC"
                srcN = "SRCS"
                objN = "OBJS"
            else:
                i += 1
                execN = f"EXEC{i}"
                srcN = f"SRC{i}"
                objN = f"OBJ{i}"

            # path of each executable
            if cfg.execOnBuildRoot or not cfg.keepFolderStructure:
                exec = f"$(BUILD)/$({execN})"
            else:
                file = self._paths[file].relative_to(self._origin)
                exec = f"$(BUILD)/{file.parent}/$({execN})"

            # target for each executable
            if execs=="":
                execs += "# executable(s)\n"
            execs += f"{execN} := {stem}\n" 
            # source files
            
            if len(self._execs)>1:
                sort = []
                for file in self._deps[exeName]:
                    file = self._paths[file].relative_to(self._origin)
                    sort.append(str(Path(file.parent, file.stem + ".c")))
                sort.sort()
                sources += getAsMultiline(f"{srcN} :=", sort)
                # the transformation from .c to .o, is also deciding the folder structure
                if cfg.keepFolderStructure:
                    objects += f"{objN} := $({srcN}:%.c=$(BUILD)/%.o)\n"
                else:
                    objects += f"{objN} := $(addprefix $(BUILD)/, $(notdir $({srcN}:%.c=%.o)))\n"
                # the sum of all objects (to use later for .d files)
                objx += f"$({objN}) "
            # the dependencies for the big "build"
            build.append(exec)
            # the executables for the big "run"
            if runall=="":
                runall += "# run all\n"
                runall += "run: build\n"
                runall += f"\t@echo '{'*'*50}'\n"
                runall += f"\t@echo 'Running all executables...'\n"
                runall += f"\t@echo '{'*'*50}'\n"
            runall += f"\t@echo ''\n"
            runall += f"\t{q}./{exec}\n"
            # targets for executables
            tgtexes += f"# target: {stem}\n{exec}: $({objN})\n"
            tgtexes += f"\t{q}$(CC) $^ $(LDFLAGS) -o $@\n\n"
            # targets from the "menu"
            tgtmenu += f"{stem}: {exec}\n"
            tgtmenu += f"\t@echo ''\n"
            tgtmenu += f"\t@echo '{'*'*50}'\n"
            tgtmenu += f"\t@echo 'Running {stem}...'\n"
            tgtmenu += f"\t@echo '{'*'*50}'\n"
            tgtmenu += f"\t@echo ''\n"
            tgtmenu += f"\t{q}./{exec}\n\n"
            # items for the help
            help.append(f"\t@echo '{stem}: to run {stem}'")
            # add menu items to phony
            phony.append(stem)
        phony.append("clean")
        help.append(f"\t@echo 'clean: to remove the {pathBuild} folder'")
        help.append(f"\t@echo '{'*'*50}'")
        help.append(f"\t@echo ''")
        help = "\n".join(help)

        if objx!="":
            objects += f"OBJS := {objx}\n"
            
        if cfg.keepFolderStructure:
            # if we replicate the folder structure then we can 
            # use the generic target matching .o and .c files
            tgtobjs += f"# targets for each object\n"
            tgtobjs += f"$(BUILD)/%.o: %.c\n"
            tgtobjs += f"\t{q}mkdir -p $(dir $@)\n"
            tgtobjs += f"\t{q}$(CC) -c $< -o $@ $(CFLAGS) $(INCS)\n\n"
        else:
            # if we don't replicate the folder structure then we are forced to
            # have a dedicated target for each folder level containing sources
            # ..stupid make? ..or me not knowing how to use make properly? :p
            levels = 0
            for file in self._srcs:
                file = self._paths[file].relative_to(self._origin)
                if levels < len(file.parts):
                    levels = len(file.parts)
            for level in range(0, levels):
                dir = "."
                if level>0:
                    dir += "/*"*level
                tgtobjs += f"# target for files inside of '{dir}' (level {level})\n"
                tgtobjs += f"$(BUILD)/%.o: {dir}/%.c\n"
                tgtobjs += f"\t{q}mkdir -p $(dir $@)\n"
                tgtobjs += f"\t{q}$(CC) -c $< -o $@ $(CFLAGS) $(INCS)\n\n"

        make = f"""#{'-'*50}>
# makefile autogenerated by python script
# customize it following your own needs <3
#{'-'*50}>

{execs}

# folders
BUILD := {pathBuild}
SOURCE := .

# compiler / linker
CC := {cfg.compiler}

# sources
{sources}

# objects
{objects.strip()}

# folders to include on compilation time
INCS := $(addprefix -I,$(shell find $(SOURCE) -type f -name "*.h" | xargs dirname | sort | uniq))

# flags for compilation & linking
CFLAGS := {cfg.cFlags}
LDFLAGS := {cfg.ldFlags}

# targets ------------------>

# build all
{getAsMultiline(f"build:", build)}

{runall}

{tgtexes}

{tgtobjs}

{tgtmenu}

help:
{help}

clean:
\t{q}rm -rf $(BUILD)

{getAsMultiline(f".PHONY:", phony)}

-include $(OBJS:.o=.d)\n"""
        make = fullReplace(make, " \n", "\n")
        make = fullReplace(make, "\t\n", "\n")
        make = fullReplace(make, "  ", " ")
        make = fullReplace(make, "\n\n\n", "\n\n")
        with open(Path(self._origin, "Makefile"), "w") as f:
            f.write(make)
