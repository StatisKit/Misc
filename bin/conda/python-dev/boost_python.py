import itertools
import os
try:
    from path import Path
except:
    from path import path as Path
    
def generate(env):
    """Add Builders and construction variables to the Environment."""
    
    if not 'boost_python' in env['TOOLS'][:-1]:
        env.Tool('system')
        env.Tool('textfile')
        env.AppendUnique(LIBS = ['boost_python'])
        env.AppendUnique(CPPDEFINES = ['BOOST_PYTHON_DYNAMIC_LIB',
                                       'BOOST_ALL_NO_LIB'])

        def BoostPythonExtension(env, target, sources):
            # Code to build "target" from "source"
            SP_DIR = env['SP_DIR']
            SYSTEM = env['SYSTEM']
            parents = []
            parent = os.path.dirname(env.File(target).srcnode().abspath)
            while os.path.exists(os.path.join(parent, '__init__.py')):
                parents.append(os.path.basename(parent))
                parent = os.path.dirname(parent)
            target = os.path.join(os.path.join(*reversed(parents)), os.path.basename(target))
            if not SYSTEM == 'win':
                target += '.so'
                target = env.File(os.path.join(SP_DIR, target))
            else:
                target += '.pyd'
                target = env.File(target)
            targets = list(itertools.chain(*[env.SharedObject(None, source) for source in sources  if source.suffix in ['.cpp', '.cxx', '.c++']]))
            sources = [source for source in sources if source.suffix == '.h']
            if len(sources) == 1 and not SYSTEM == 'win':
                env.AppendUnique(CCFLAGS=['-Wno-attributes', '-Wno-deprecated-declarations'])
                cmd = env.subst('$CXX') + ' -o $TARGET -x c++-header -c -fPIC ' + env.subst('$SHCXXFLAGS $_CCCOMCOM').replace('-x c++', '') + ' $SOURCE'
                if SYSTEM == 'linux':
                    cmd = env.Command(sources[0].target_from_source('', '.h.gch'), sources[0], cmd)
                else:
                    cmd = env.Command(sources[0].target_from_source('', '.h.pch'), sources[0], cmd)
                env.Depends(targets, cmd)
                if SYSTEM == 'osx':
                    env['CXX'] += " -include " + sources[0].target_from_source('', '.h').abspath
            env.Depends(target, targets)
            if SYSTEM == 'win':
                response = env.Textfile('response_file.rsp',
                         [tgt.abspath.replace('/','\\') for tgt in targets],
                         LINESEPARATOR=" ")
            else:
                response = env.Textfile('response_file.rsp',
                         [tgt.abspath.replace('\\','/') for tgt in targets],
                         LINESEPARATOR=" ")
            env.Append(LINKFLAGS = '@' + response[0].abspath)
            env.Depends(target, response)
            if SYSTEM == 'win':
                pyd, lib, exp = env.SharedLibrary(target, [], SHLIBPREFIX='',
                                                  SHLIBSUFFIX = '.pyd')
                return env.Install(os.path.join(SP_DIR, Path(target).parent), pyd)
            elif SYSTEM == 'osx':
                return env.LoadableModule(target, [], SHLIBPREFIX='',
                                          SHLINKFLAGS='$LINKFLAGS -bundle',
                                          FRAMEWORKSFLAGS='-flat_namespace -undefined suppress')
            else:
                return env.LoadableModule(target, [], SHLIBPREFIX='')

        env.AddMethod(BoostPythonExtension)
        env.Tool('python')

def exists(env):
    return 1