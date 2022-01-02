#!python

import os
import shutil
from pathlib import Path
from configparser import ConfigParser

class MakerConfig:
    def __init__(self) -> None:
        self._cp = ConfigParser(allow_no_value=True, )
        fileName = "maker.ini"
        if os.path.exists(fileName):
            self._cp.read(fileName)
        else:
            self.save(fileName)
    @property
    def compiler(self): return self._cp.get("config","compiler", fallback="gcc")
    @property
    def cflags(self): return self._cp.get("config","cflags", fallback="-Wall -Werror -Wpedantic -Wextra")
    @property
    def ldflags(self): return self._cp.get("config","ldflags", fallback="")
    @property
    def be_quiet(self): return self._cp.getboolean("config","be_quiet", fallback="True")
    @property
    def exec_extension(self): return self._cp.get("config","exec_extension", fallback="")
    @property
    def keep_folder_structure(self): return self._cp.getboolean("config","keep_folder_structure", fallback="True")
    @property
    def use_explicit_source_list(self): return self._cp.getboolean("config","use_explicit_source_list", fallback="True")

    def save(self, filePath="maker_backup.ini"):
        df = "DEFAULT"
        cf = "config"
        if not self._cp.has_section(cf):
            self._cp.add_section(cf)

        default = self._cp.defaults()
        config = self._cp[cf]

        def ensure(key, val):
           #if not self._cp.has_option(cf,key): config[key] = val
            if not self._cp.has_option(df,key): default[key] = val

        ensure("compiler", "gcc")
        ensure("cflags", "-Wall -Werror -Wpedantic -Wextra")
        ensure("ldflags", "")
        ensure("be_quiet", "yes")
        ensure("exec_extension", "")
        ensure("keep_folder_structure", "yes")
        ensure("use_explicit_source_list", "yes")

        with open(filePath, 'w') as f:
            self._cp.write(f)

cfg = MakerConfig()

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
                exeName = Path(cFile).stem + cfg.exec_extension
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
    
    def build(self, pathBuild="build", clean=False, run=False):
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
                if cfg.keep_folder_structure:
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
            return f"{cfg.compiler} -c {src} {cfg.cflags} {inc} -o {obj}".replace("  ", " ")

        def getCmdLink(cFile:str):
            def getBuildObjs(exeName):
                objs = ""
                for oFile in self._deps[exeName]:
                    objs += str(getBuildRelativePath(oFile, ".o")) + " "
                return objs

            out = getBuildRelativePath(cFile, cfg.exec_extension)
            objs = getBuildObjs(Path(cFile).stem + cfg.exec_extension)
            return f"{cfg.compiler} {objs} {cfg.ldflags} -o {out}".replace("  ", " ")

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
                        if not cfg.be_quiet:
                            print(cmd)
                        errCode = os.system(cmd)
                        if errCode!=0:
                            raise Exception(f"Error during compilation process (code:{errCode})")
                        fileCounter += 1
                        break

        # link -> create executable files
        for cFile in self._execs:
            exeName = Path(cFile).stem + cfg.exec_extension
            stampExe = getTimestamp(getBuildRelativePath(cFile, cfg.exec_extension))
            for oFile in self._deps[exeName]:
                # filter files that are not inside the folder structure
                if oFile in self._paths:
                    stampObj = getTimestamp(getBuildRelativePath(oFile, ".o"))
                    if stampExe<stampObj:
                        cmd = getCmdLink(cFile)
                        if not cfg.be_quiet:
                            print(cmd)
                        errCode = os.system(cmd)
                        if errCode!=0:
                            raise Exception(f"Error during linking process (code:{errCode})")
                        fileCounter += 1
                        break
        
        if fileCounter<=0 and not cfg.be_quiet:
            print("Nothing to build, all dependencies are up-to-date.")
        
        # run all executables
        if run:
            for cFile in self._execs:
                exePath = getBuildRelativePath(cFile, cfg.exec_extension)
                if not cfg.be_quiet:
                    print()
                    print(f"Running {exePath.name}...")
                errCode = os.system(f"./{exePath}")
                if errCode!=0:
                    # should i do something here?
                    pass

    def createMakefile(self, pathBuild="build", runMakeClean=False, runMake=False):
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
        def safePath1(path:str):
            # GNU make is not prepared to have spaces in file names...
            # no meaning in trying to fix the stupid make
            return str(path).replace(" ","\\ ")
        def safePath2(path:str, quot="'"):
            # GNU make is not prepared to have spaces in file names...
            # no meaning in trying to fix the stupid make
            path = str(path)
            if path.find(" ")>=0:
                path = quot+path+quot
            return path
        def getSourceList(files):
            sort = []
            for file in files:
                file = self._paths[file].relative_to(self._origin)
                sort.append(safePath2(Path(file.parent, file.stem + '.c')))
            sort.sort()
            return sort
        
        pathBuild = Path(pathBuild)
        if pathBuild.is_relative_to(self._origin):
            pathBuild = pathBuild.relative_to(self._origin)
        pathBuild = safePath2(pathBuild)

        objx = []
        execs = []
        sources = ["# source files"]
        objects = ["# objects"]
        tgtobjs = []
        tgtexes = []
        build = []
        tgtmenu = []
        runall = []
        phony = ["help", "build"]
        help = ["help:"]
        help.append(f'\t@clear')
        help.append(f'\t@echo "{"*"*20} Targets {"*"*21}"')
        help.append(f'\t@echo "help: to print this menu"')
        help.append(f'\t@echo "build: to compile {"and link " if len(self._execs)>0 else ""}all sources (default)"')
        
        # the quiet/verbose mode        
        q = "@" if cfg.be_quiet else ""

        if len(self._execs)<=1:
            if cfg.use_explicit_source_list:
                if len(self._execs)==0:
                    # use all the source files
                    sources.append(getAsMultiline(f"SRCS :=", getSourceList(self._srcs)).strip())
                else:
                    # use the files to create the only executable (exec[0])
                    exeFileName = Path(self._execs[0]).stem + cfg.exec_extension
                    sources.append(getAsMultiline(f"SRCS :=", getSourceList(self._deps[exeFileName])).strip())
            else:
                # for one or none executables, we can use all the source files
                sources.append(f"SRCS := $(shell find $(SRCDIR) -name '*.c')")

            if cfg.keep_folder_structure:
                objects.append(f"OBJS := $(SRCS:%.c=$(BUILDDIR)/%.o)")
            else:
                objects.append(f"OBJS := $(addprefix $(BUILDDIR)/, $(notdir $(SRCS:%.c=%.o)))")

        if len(self._execs)<=0:
            build.append("$(OBJS)")

        if len(self._execs)>0:
            phony.append("run")
            help.append('\t@echo "run: to run all the executables"')
            runall.append('# run all')
            runall.append('run: build')
            runall.append(f'\t@echo "{"*"*50}"')
            runall.append(f'\t@echo "Running all executables..."')
            runall.append(f'\t@echo "{"*"*50}"')
            execs.append("# executables")

        for i, file in enumerate(self._execs):
            stem = Path(file).stem
            exeFileName = stem + cfg.exec_extension
            if len(self._execs)==1:
                exeN = "EXEC"
                srcN = "SRCS"
                objN = "OBJS"
            else:
                i += 1
                exeN = f"EXEC{i}"
                srcN = f"SRC{i}"
                objN = f"OBJ{i}"

            # path of each executable
            if cfg.keep_folder_structure:
                file = self._paths[file].relative_to(self._origin)
                execp = f"$(BUILDDIR)/{file.parent}/{exeFileName}"
            else:
                execp = f"$(BUILDDIR)/{exeFileName}"

            # variables for the path of each executable
            execs.append(f"{exeN} := {execp}")
            exeN = f"$({exeN})"

            # source files
            if len(self._execs)>1:
                
                if cfg.use_explicit_source_list:
                    # explicit list of files
                    sources.append(getAsMultiline(f"{srcN} :=", getSourceList(self._deps[exeFileName])).strip())
                else:
                    # FIXME
                    # command to find the files
                    sources.append("# FIXME HERE -> place the corresponding filters")
                    command = "$(shell find $(SRCDIR) -name '*.c')"
                    sources.append(f"{srcN} := {command}")

                # the transformation from .c to .o, is also creating the folder structure
                if cfg.keep_folder_structure:
                    objects.append(f"{objN} := $({srcN}:%.c=$(BUILDDIR)/%.o)")
                else:
                    objects.append(f"{objN} := $(addprefix $(BUILDDIR)/, $(notdir $({srcN}:%.c=%.o)))")

                # the sum of all objects (to use later for .d files)
                objx.append(f"$({objN})")

            # the dependencies for the big "build"
            build.append(exeN)
            # the executables for the big "run"
            runall.append(f'\t@echo ""')
            runall.append(f"\t{q}./{exeN}")
            # targets for executables
            tgtexes.append(f"# compile/link: {stem}")
            tgtexes.append(f"{exeN}: $({objN})")
            tgtexes.append(f"\t{q}$(CC) $^ $(LDFLAGS) -o $@\n")
            # targets from the "menu"
            stemFix = safePath1(stem)
            tgtmenu.append(f"# run: {stem}")
            tgtmenu.append(f'{stemFix}: {exeN}')
            tgtmenu.append(f'\t@echo ""')
            tgtmenu.append(f'\t@echo "{"*"*50}"')
            tgtmenu.append(f'\t@echo "Running {stem}..."')
            tgtmenu.append(f'\t@echo "{"*"*50}"')
            tgtmenu.append(f'\t@echo ""')
            tgtmenu.append(f'\t{q}./{exeN}\n')
            # items for the help
            stemFix = safePath2(stem,"\'")
            help.append(f'\t@echo "{stemFix}: to run {stem}"')
            # add menu items to phony
            stemFix = safePath2(stem, '"')
            phony.append(stemFix)
        
        phony.append("clean")
        help.append(f'\t@echo "clean: to remove the {pathBuild} folder"')
        help.append(f'\t@echo "{"*"*50}"')
        help.append(f'\t@echo ""')

        if len(objx)>1:
            objects.append(getAsMultiline(f"OBJS :=", objx))
            
        if cfg.keep_folder_structure:
            # if we replicate the folder structure then we can 
            # use the generic target matching .o and .c files
            tgtobjs.append(f"# targets for each object")
            tgtobjs.append(f"$(BUILDDIR)/%.o: %.c")
            tgtobjs.append(f"\t{q}mkdir -p $(dir $@)")
            tgtobjs.append(f"\t{q}$(CC) -c $< -o $@ $(CFLAGS) $(INCS)\n")
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
                tgtobjs.append(f"# target for files inside of '{dir}' (level {level})")
                tgtobjs.append(f"$(BUILDDIR)/%.o: {dir}/%.c")
                tgtobjs.append(f"\t{q}mkdir -p $(dir $@)")
                tgtobjs.append(f"\t{q}$(CC) -c $< -o $@ $(CFLAGS) $(INCS)\n")

        # stringify all lists
        execs = "\n".join(execs)
        sources = "\n".join(sources)
        objects = "\n".join(objects)
        help = "\n".join(help)
        tgtmenu = "\n".join(tgtmenu)
        runall = "\n".join(runall)
        tgtexes = "\n".join(tgtexes)
        tgtobjs = "\n".join(tgtobjs)

        # the make template
        make = f"""#{'-'*50}>
# makefile autogenerated by python script
# customize it following your own needs <3
#{'-'*50}>

# compiler / linker
CC := {cfg.compiler}

# flags for compilation & linking
CFLAGS := {cfg.cflags}
LDFLAGS := {cfg.ldflags}

# folders
SRCDIR := .
BUILDDIR := {pathBuild}

{execs}

# folders to include on compilation time
INCS := $(addprefix -I,$(shell find $(SRCDIR) -type f -name "*.h" | xargs dirname | sort | uniq))

{sources}

{objects}

# targets ########################

# build all
{getAsMultiline(f"build:", build)}

{runall}

{tgtexes}

{tgtobjs}

{tgtmenu}

{help}

clean:
\t{q}rm -rf $(BUILDDIR)

{getAsMultiline(f".PHONY:", phony)}

-include $(OBJS:.o=.d)\n"""

        # replace extra formatting 
        make = fullReplace(make, " \n", "\n")
        make = fullReplace(make, "\t\n", "\n")
        make = fullReplace(make, "  ", " ")
        make = fullReplace(make, "\n\n\n", "\n\n")

        with open(Path(self._origin, "Makefile"), "w") as f:
            f.write(make)

        if runMakeClean:
            os.system(f"cd {self._origin} && make clean")

        if runMake:
            os.system(f"cd {self._origin} && make")



# in case it is executed from the command line or directly with an IDE
if __name__ == "__main__":
    mkr = Maker()
    mkr.load()
    mkr.createMakefile()
