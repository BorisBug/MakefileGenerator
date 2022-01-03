#!python

import os
import shutil
from pathlib import Path
from configparser import ConfigParser

def getPathAs(path, ext):
    return Path(path.parent, path.stem + ext)

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

    def printListSources(self):
        for path in self._srcs:
            print(path.name)
        print()

    def printListExecs(self):
        for path in self._execs:
            print(path.name)
        print()

    def printListIncludeFolders(self):
        for path in self._folders:
            print(path)
        print()

    def printListDependencies(self):
        for dep in self._deps:
            depNames = ""
            for path in self._deps[dep]:
                depNames += path.name + " "
            print(f"{dep.name} -> {depNames}")
        print()
            
    def load(self, path="."):
        self._origin = Path(path)
        self._srcs.clear()
        self._execs.clear()
        self._folders.clear()
        self._deps.clear()
        headers = []

        # scan recursively the complete folder tree
        def scanOriginFolder():
            for path in self._origin.rglob("*"):
                # if is a file...
                if path.is_file():
                    # collect all the .c files
                    if path.suffix==".c": 
                        self._srcs.append(path)
                    # collect all the .h files
                    elif path.suffix==".h": 
                        headers.append(path)
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
            def getIncludedDeps(pathSrc, depList=[]):
                def getPathFromName(name):
                    for path in headers:
                        if name == path.name:
                            return path
                    return None                  
                def getContentFromFile(pathSrc):
                    content = ""
                    with open(pathSrc, "r") as f:
                        content = f.read()
                    return content
                def getIncludeListFromContent(content):
                    def getPos1(startPos):
                        include = "#include"
                        pos1 = content.find(include, startPos)
                        if pos1>=0:
                            pos1 += len(include)
                            while pos1<len(content) and content[pos1] == " ":
                                pos1 += 1
                        return pos1    
                    def getPos2(startPos, delim):
                        return content.find(delim, startPos)
                    includes = []
                    pos1 = getPos1(0)
                    while pos1>=0:
                        delim = content[pos1]
                        pos1 += 1
                        pos2 = -1
                        if delim=='"':
                            pos2 = getPos2(pos1, '"')
                        elif delim=="<":
                            pos2 = getPos2(pos1, '>')
                        if pos2<0:
                            # something wrong with the syntax
                            break
                        name = content[pos1:pos2]
                        includes.append(name)
                        pos1 = getPos1(pos2+1)
                    return includes
                def getDepsFromIncludeList(names):
                    nonlocal depList
                    # check if the file exist in the structure using "name" only
                    for name in names:
                        path = getPathFromName(name)
                        if not path:
                            # include out of the structure
                            continue
                        if not path in depList:
                            depList.append(path)
                            getIncludedDeps(path, depList)
                    return depList

                content = getContentFromFile(pathSrc)
                includes = getIncludeListFromContent(content)
                depList = getDepsFromIncludeList(includes)
                return depList
        
            # deps for source files
            for pathSrc in self._srcs:
                # if it will become executable, save it for the linking process
                if isExe(pathSrc):
                    self._execs.append(pathSrc)

                # every source file generates an .o file
                pathObj = getPathAs(pathSrc, ".o")
                # each .o file depends on the source and it's included headers
                depList = getIncludedDeps(pathSrc, [])
                self._deps[pathObj] = [pathSrc] + depList

            # deps for exe files
            for path in self._execs:
                deps = []
                def getObjDeps(path):
                    nonlocal deps
                    for path in self._deps[path]:
                        path = getPathAs(path, ".o")
                        if path in self._deps and path not in deps:
                            deps.append(path)
                            for path in getObjDeps(path):
                                if path not in deps:
                                    deps.append(path)
                    return deps
                pathObj = getPathAs(path, ".o")
                pathExe = getPathAs(path, cfg.exec_extension)
                self._deps[pathExe] = getObjDeps(pathObj)
    
        scanOriginFolder()
        loadDependencies()
    
    def build(self, pathBuild="build", clean=False, run=False):
        # ensure a type Path
        pathBuild = Path(pathBuild)

        # temp variables for the build process
        incFlag = ""
        relPaths = {}
        timeStamps = {}
        fileCounter = 0

        def getBuildRelativePath(path, newSuffix=""):
            nonlocal pathBuild
            newName = path.stem + newSuffix
            pathKey = Path(path.parent, newName)

            if pathKey in relPaths:
                path = relPaths[pathKey]
            else:
                if cfg.keep_folder_structure:
                    path = path.relative_to(self._origin)
                    if pathBuild.is_relative_to(self._origin):
                        path = Path(self._origin, pathBuild.relative_to(self._origin), path.parent, newName)
                    else:
                        path = Path(pathBuild, path.parent, newName)
                else:
                    path = Path(pathBuild, newName)
                # create folder structure
                if not os.path.isdir(path.parent):
                    os.makedirs(path.parent)
                
                relPaths[pathKey] = path
            
            return path

        def getCmdCompile(pathSrc):
            def getIncludeFlag():
                nonlocal incFlag
                if incFlag !="":
                    return incFlag

                for dir in self._folders: 
                    incFlag += " -I./" + dir
                return incFlag
                
            inc = getIncludeFlag()            
            pathObj = getBuildRelativePath(pathSrc, ".o")
            return f"{cfg.compiler} -c {pathSrc} {cfg.cflags} {inc} -o {pathObj}".replace("  ", " ")

        def getCmdLink(pathSrc):
            def getBuildObjs(pathExe):
                objs = ""
                for pathObj in self._deps[pathExe]:
                    objs += str(getBuildRelativePath(pathObj, ".o")) + " "
                return objs

            pathExe = getPathAs(pathSrc, cfg.exec_extension)
            pathOut = getBuildRelativePath(pathSrc, cfg.exec_extension)
            objs = getBuildObjs(pathExe)
            return f"{cfg.compiler} {objs} {cfg.ldflags} -o {pathOut}".replace("  ", " ")

        def getTimestamp(path):
            stamp = 0.0
            if path in timeStamps:
                stamp = float(timeStamps[path])
            if stamp == 0.0:
                stamp = 0.0 if not os.path.isfile(path) else os.path.getmtime(path)
                timeStamps[path] = stamp
            return stamp

        def executeCmd(cmd):
            if not cfg.be_quiet:
                print(cmd)
            errCode = os.system(cmd)
            if errCode!=0:
                raise Exception(f"Error during building process (code:{errCode})")

        # remove build folder
        if clean and pathBuild.is_dir() and pathBuild.cwd()!=pathBuild.absolute():
            shutil.rmtree(pathBuild, ignore_errors = True)

        # compile
        # -> check timestamps
        # -> create object files
        for pathSrc in self._srcs:
            assert pathSrc.suffix==".c"
            pathObj = getPathAs(pathSrc, ".o")
            pathObjRel = getBuildRelativePath(pathSrc, ".o")
            stampObjRel = getTimestamp(pathObjRel)
            # check the timestamp of all dependencies
            for pathDep in self._deps[pathObj]:
                assert pathDep.suffix==".c" or pathDep.suffix==".h"
                stampDep = getTimestamp(pathDep)
                if stampObjRel<stampDep:
                    executeCmd(getCmdCompile(pathSrc))
                    fileCounter += 1
                    break

        # link 
        # -> check timestamps
        # -> create executable files
        for pathSrc in self._execs:
            assert pathSrc.suffix==".c"
            pathExe = getPathAs(pathSrc, cfg.exec_extension)
            pathExeRel = getBuildRelativePath(pathSrc, cfg.exec_extension)
            stampExeRel = getTimestamp(pathExeRel)
            # check the timestamp of all dependencies
            for pathObj in self._deps[pathExe]:
                assert pathObj.suffix==".o"
                pathObjRel = getBuildRelativePath(pathObj, ".o")
                stampObjRel = getTimestamp(pathObjRel)
                if stampExeRel<stampObjRel:
                    executeCmd(getCmdLink(pathSrc))
                    fileCounter += 1
                    break
        
        if fileCounter<=0 and not cfg.be_quiet:
            print("Nothing to build, all dependencies are up-to-date.")
        
        # run all executables
        if run:
            for pathSrc in self._execs:
                pathExe = getBuildRelativePath(pathSrc, cfg.exec_extension)
                if not cfg.be_quiet:
                    print()
                    print(f"Running {pathExe.name}...")
                errCode = os.system(f"./{pathExe}")
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
                item = str(item)
                if len(line + " " + item)>70:
                    multi += line + " \\\n"
                    line = "\t" + item
                else:
                    line += " " + item
            multi += line + "\n"
            return multi
        #def safePath1(path:str):
            # GNU make is not prepared to have spaces in file names...
            # no meaning in trying to fix the stupid make
            #return str(path).replace(" ","\\ ")
        #def safePath2(path:str, quot="'"):
            # GNU make is not prepared to have spaces in file names...
            # no meaning in trying to fix the stupid make
            #path = str(path)
            #if path.find(" ")>=0:
            #    path = quot+path+quot
            #return path
        def getSourceList(files):
            sort = []
            for path in files:
                path = path.relative_to(self._origin)
                sort.append(getPathAs(path, '.c'))
            sort.sort()
            return sort
        
        pathBuild = Path(pathBuild)
        if pathBuild.is_relative_to(self._origin):
            pathBuild = pathBuild.relative_to(self._origin)
        #pathBuild = safePath2(pathBuild)

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
                    # if there is no executables then use all the source files in the structure
                    sources.append(getAsMultiline(f"SRCS :=", getSourceList(self._srcs)).strip())
                else:
                    # use the files to create the only executable (exec[0])
                    nameExe = getPathAs(self._execs[0], cfg.exec_extension)
                    sources.append(getAsMultiline(f"SRCS :=", getSourceList(self._deps[nameExe])).strip())
            else:
                # for one or none executables, we can use all the source files in the structure
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

        stemExeUnique = {}
        for i, pathSrc in enumerate(self._execs):
            if pathSrc.stem in stemExeUnique:
                stemExeUnique[pathSrc.stem] += 1
                stem = pathSrc.stem + f"{stemExeUnique[stem]}"
            else:
                stemExeUnique[pathSrc.stem] = 1
                stem = pathSrc.stem
            nameExe = pathSrc.stem + cfg.exec_extension
            pathExe = getPathAs(pathSrc, cfg.exec_extension)
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
                execp = f"$(BUILDDIR)/{pathSrc.relative_to(self._origin).parent}/{nameExe}"
            else:
                execp = f"$(BUILDDIR)/{nameExe}"

            # variables for the path of each executable
            execs.append(f"{exeN} := {execp}")
            exeN = f"$({exeN})"

            # source files
            if len(self._execs)>1:
                
                if cfg.use_explicit_source_list:
                    # explicit list of files
                    sources.append(getAsMultiline(f"{srcN} :=", getSourceList(self._deps[pathExe])).strip())
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
            tgtmenu.append(f"# run: {stem}")
            tgtmenu.append(f'{stem}: {exeN}')
            tgtmenu.append(f'\t@echo ""')
            tgtmenu.append(f'\t@echo "{"*"*50}"')
            tgtmenu.append(f'\t@echo "Running {stem}..."')
            tgtmenu.append(f'\t@echo "{"*"*50}"')
            tgtmenu.append(f'\t@echo ""')
            tgtmenu.append(f'\t{q}./{exeN}\n')
            # items for the help
            help.append(f'\t@echo "{stem}: to run {stem}"')
            # add menu items to phony
            phony.append(stem)
        
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
            for path in self._srcs:
                path = path.relative_to(self._origin)
                if levels < len(path.parts):
                    levels = len(path.parts)
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
