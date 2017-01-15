import platform
from distutils.version import StrictVersion

def _boost_python_module_action(target, source, env):
    # Code to build "target" from "source"
    headers = [header for header in source if header.suffix is '.h']
    sources = [source for source in source if source.suffix in ['.cpp', '.cxx', '.c++']]
    targets = list(itertools.chain(*[env.SharedObject(None, source) for source in sources]))

    if system is 'linux' and len(headers) == 1:
        if len(header) == 1:
            cmd = env.Command(header[0].target_from_source('', '.h.gch'), header, '$CXX -o $TARGET -x c++-header -c -fPIC $SHCXXFLAGS $_CCCOMCOM $SOURCE')
            env.Depends(targets, cmd)

    source = env.File('response_file.rsp')
    with open(source.abspath, 'w') as filehandler:
        filehandler.write(' '.join(target.abspath.replace('\\','/') + ' ' for target in targets))

    env.Append(LINKFLAGS = '@' + source.abspath)

    kwargs = dict('SHLIBSUFFIX' = '.so',
                  'SHLIBPREFIX' = '')

    if system is 'darwin':
        bpm = env.LoadableModule(target, [], LDMODULESUFFIX='.so',
            FRAMEWORKSFLAGS = '-flat_namespace -undefined suppress', **kwargs)
    else:
        bpm = env.LoadableModule(target, [], **kwargs)

    return bpm

_boost_python_module_builder = SCons.Builder.Builder(action = _boost_python_module_action)

def generate(env):
    """Add Builders and construction variables to the Environment."""
    env.Append(LIBS = 'boost_python')
    env.AppendUnique(CPPDEFINES = ['BOOST_PYTHON_DYNAMIC_LIB', 'BOOST_ALL_NO_LIB'])
    env['BUILDERS']['BoostPythonModule'] = _boost_python_module_builder

def exists(env):
    return 1