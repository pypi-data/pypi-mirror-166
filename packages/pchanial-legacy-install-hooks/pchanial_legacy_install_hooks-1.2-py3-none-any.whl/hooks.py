"""Hooks to ease building of fortran or cython extensions.
"""
import os
import sys
from pathlib import Path

# we disable setuptools sdist see numpy github issue #7127
if 'sdist' not in sys.argv:
    import setuptools

import numpy
import re
from numpy.distutils.command.build_clib import build_clib
from numpy.distutils.command.build_ext import build_ext
from numpy.distutils.command.build_src import build_src
from numpy.distutils.command.sdist import sdist
from distutils.cmd import Command
from numpy.distutils.exec_command import find_executable
from numpy.distutils.fcompiler import new_fcompiler
from numpy.distutils.fcompiler.gnu import Gnu95FCompiler
from numpy.distutils.fcompiler.intel import IntelEM64TFCompiler
from numpy.distutils.misc_util import f90_ext_match, has_f_sources
from pkg_resources import parse_version
from subprocess import call

# These variables can be changed by the hooks importer
F77_OPENMP = True
F90_OPENMP = True
F77_COMPILE_ARGS_GFORTRAN = []
F77_COMPILE_DEBUG_GFORTRAN = ['-fcheck=all', '-Og']
F77_COMPILE_OPT_GFORTRAN = ['-Ofast','-march=native']
F90_COMPILE_ARGS_GFORTRAN = ['-cpp']
F90_COMPILE_DEBUG_GFORTRAN = ['-fcheck=all', '-Og']
F90_COMPILE_OPT_GFORTRAN = ['-Ofast', '-march=native']
F77_COMPILE_ARGS_IFORT = []
F77_COMPILE_DEBUG_IFORT = ['-check all']
F77_COMPILE_OPT_IFORT = ['-fast']
F90_COMPILE_ARGS_IFORT = ['-fpp','-ftz','-fp-model precise','-ftrapuv','-warn all']
F90_COMPILE_DEBUG_IFORT = ['-check all']
F90_COMPILE_OPT_IFORT = ['-fast']
F2PY_TABLE = {'integer': {'int8': 'char',
                          'int16': 'short',
                          'int32': 'int',
                          'int64': 'long_long'},
              'real': {'real32': 'float',
                       'real64': 'double'},
              'complex': {'real32': 'complex_float',
                          'real64': 'complex_double'}}
FCOMPILERS_DEFAULT = 'ifort', 'gfortran'
FLAGS_OPENMP = {
    'ifort': ['-qopenmp'],
    'gfortran': ['-openmp'],
}
LIBRARY_OPENMP = {
    'ifort': 'iomp5',
    'gfortran': 'gomp',
}
USE_CYTHON = bool(int(os.getenv('SETUPHOOKS_USE_CYTHON', '1') or '0'))
MIN_VERSION_CYTHON = '0.13'

numpy.distutils.log.set_verbosity(numpy.distutils.log.DEBUG)

# monkey patch to allow pure and elemental routines in preprocessed
# Fortran libraries
numpy.distutils.from_template.routine_start_re = re.compile(
    r'(\n|\A)((     (\$|\*))|)\s*((im)?pure\s+|elemental\s+)*(subroutine|funct'
    r'ion)\b', re.I)
numpy.distutils.from_template.function_start_re = re.compile(
    r'\n     (\$|\*)\s*((im)?pure\s+|elemental\s+)*function\b', re.I)

# monkey patch compilers
Gnu95FCompiler.get_flags_debug = lambda self: []
Gnu95FCompiler.get_flags_opt = lambda self: []
IntelEM64TFCompiler.get_flags_debug = lambda self: []
IntelEM64TFCompiler.get_flags_opt = lambda self: []

# monkey patch the default Fortran compiler
if sys.platform.startswith('linux'):
    _id = 'linux.*'
elif sys.platform.startswith('darwin'):
    _id = 'darwin.*'
else:
    _id = None
if _id is not None:
    table = {'ifort': 'intelem', 'gfortran': 'gnu95'}
    _df = (_id, tuple(table[f] for f in FCOMPILERS_DEFAULT)),
    numpy.distutils.fcompiler._default_compilers = _df


class BuildClibCommand(build_clib):
    def build_libraries(self, libraries):
        fcompiler = self._f_compiler
        if fcompiler is None:
            raise ValueError('build_clib._f_compiler is None.')

        if isinstance(fcompiler, numpy.distutils.fcompiler.gnu.Gnu95FCompiler):
            flags = F77_COMPILE_ARGS_GFORTRAN + F77_COMPILE_OPT_GFORTRAN
            if self.debug:
                flags += F77_COMPILE_DEBUG_GFORTRAN
            if F77_OPENMP:
                flags += FLAGS_OPENMP['gfortran']
            fcompiler.executables['compiler_f77'] += flags
            flags = F90_COMPILE_ARGS_GFORTRAN + F90_COMPILE_OPT_GFORTRAN
            if self.debug:
                flags += F90_COMPILE_DEBUG_GFORTRAN
            if F90_OPENMP:
                flags += FLAGS_OPENMP['gfortran']
            fcompiler.executables['compiler_f90'] += flags
            fcompiler.libraries += [LIBRARY_OPENMP['gfortran']]

        elif isinstance(fcompiler, numpy.distutils.fcompiler.intel.IntelFCompiler):
            self.compiler.archiver[0] = find_executable('xiar')
            flags = F77_COMPILE_ARGS_IFORT + F77_COMPILE_OPT_IFORT
            if self.debug:
                flags += F77_COMPILE_DEBUG_IFORT
            if F77_OPENMP:
                flags += FLAGS_OPENMP['ifort']
            fcompiler.executables['compiler_f77'] += flags
            flags = F90_COMPILE_ARGS_IFORT + F90_COMPILE_OPT_IFORT
            if self.debug:
                flags += F90_COMPILE_DEBUG_IFORT
            if F90_OPENMP:
                flags += FLAGS_OPENMP['ifort']
            fcompiler.executables['compiler_f90'] += flags
            fcompiler.libraries += [LIBRARY_OPENMP['ifort']]

        elif fcompiler is not None:
            raise RuntimeError("Unhandled compiler: '{}'.".format(fcompiler))

        try:
            super().build_libraries(libraries)
        except Exception as exc:
            print(f'Build library: an exception occurred: {exc}')
            raise
        finally:
            print(f'_f_compiler: {fcompiler.executables}')
            print(f'archiver: {self.compiler.archiver}')


class BuildCyCommand(Command):
    description = 'cythonize files'
    user_options = []

    def run(self):
        extensions = self.distribution.ext_modules
        if self._has_cython():
            from Cython.Build import cythonize
            new_extensions = cythonize(extensions)
            for i, ext in enumerate(new_extensions):
                for source in extensions[i].sources:
                    if source.endswith('.pyx'):
                        # include cython file in the MANIFEST
                        ext.depends.append(source)
                extensions[i] = ext
            return

        for ext in extensions:
            for isource, source in enumerate(ext.sources):
                if source.endswith('.pyx'):
                    suf = 'cpp' if ext.language == 'c++' else 'c'
                    new_source = source[:-3] + suf
                    ext.sources[isource] = new_source
                    if not os.path.exists(new_source):
                        print("Aborting: cythonized file '{}' is missing.".
                              format(new_source))
                        sys.exit()

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _has_cython(self):
        extensions = self.distribution.ext_modules
        if not USE_CYTHON or not any(_.endswith('.pyx')
                                     for ext in extensions
                                     for _ in ext.sources):
            return False
        try:
            import Cython
        except ImportError:
            print('Cython is not installed, defaulting to C/C++ files.')
            return False
        if parse_version(Cython.__version__) < \
           parse_version(MIN_VERSION_CYTHON):
            print("The Cython version is older than that required ('{0}' < '{1"
                  "}'). Defaulting to C/C++ files."
                  .format(Cython.__version__, MIN_VERSION_CYTHON))
            return False
        return True


class BuildExtCommand(build_ext):
    def build_extensions(self):
        # Numpy bug: if an extension has a library only consisting of f77
        # files, the extension language will always be f77 and no f90
        # compiler will be initialized
        need_f90_compiler = self._f90_compiler is None and \
            any(any(f90_ext_match(s) for s in _.sources)
                for _ in self.extensions)
        if need_f90_compiler:
            print('WARNING: mixed f90/f77 files HACK still required.')
            self._f90_compiler = new_fcompiler(compiler=self.fcompiler,
                                               verbose=self.verbose,
                                               dry_run=self.dry_run,
                                               force=self.force,
                                               requiref90=True,
                                               c_compiler=self.compiler)
            fcompiler = self._f90_compiler
            if fcompiler:
                fcompiler.customize(self.distribution)
            if fcompiler and fcompiler.get_version():
                fcompiler.customize_cmd(self)
                fcompiler.show_customization()
            else:
                ctype = fcompiler.compiler_type if fcompiler \
                    else self.fcompiler
                self.warn('f90_compiler=%s is not available.' % ctype)

        for fc in self._f77_compiler, self._f90_compiler:

            if isinstance(fc, numpy.distutils.fcompiler.gnu.Gnu95FCompiler):
                assert fc is not None
                flags = F77_COMPILE_ARGS_GFORTRAN + F77_COMPILE_OPT_GFORTRAN
                if self.debug:
                    flags += F77_COMPILE_DEBUG_GFORTRAN
                if F77_OPENMP:
                    flags += FLAGS_OPENMP['gfortran']
                fc.executables['compiler_f77'] += flags
                flags = F90_COMPILE_ARGS_GFORTRAN + F90_COMPILE_OPT_GFORTRAN
                if self.debug:
                    flags += F90_COMPILE_DEBUG_GFORTRAN
                if F90_OPENMP:
                    flags += FLAGS_OPENMP['gfortran']
                fc.executables['compiler_f90'] += flags
                fc.libraries += [LIBRARY_OPENMP['gfortran']]

            elif isinstance(fc, numpy.distutils.fcompiler.intel.IntelFCompiler):
                assert fc is not None
                flags = F77_COMPILE_ARGS_IFORT + F77_COMPILE_OPT_IFORT
                if self.debug:
                    flags += F77_COMPILE_DEBUG_IFORT
                if F77_OPENMP:
                    flags += FLAGS_OPENMP['ifort']
                fc.executables['compiler_f77'] += flags
                flags = F90_COMPILE_ARGS_IFORT + F90_COMPILE_OPT_IFORT
                if self.debug:
                    flags += F90_COMPILE_DEBUG_IFORT
                if F90_OPENMP:
                    flags += FLAGS_OPENMP['ifort']
                fc.executables['compiler_f90'] += flags
                fc.libraries += [LIBRARY_OPENMP['ifort']]

            elif fc is not None:
                raise RuntimeError(f"Unhandled compiler: '{fc}'.")

        try:
            super().build_extensions()
        except Exception as exc:
            print(f'Build extensions: an exception occurred: {exc}')
            raise
        finally:
            print(f'_f77_compiler: {self._f77_compiler}')
            if self._f77_compiler:
                print(f'_f77_compiler: {self._f77_compiler.executables}')
            print(f'_f90_compiler: {self._f90_compiler}')
            if self._f90_compiler:
                print(f'_f90_compiler: {self._f90_compiler.executables}')


class BuildSrcCommand(build_src):
    def initialize_options(self):
        super().initialize_options()
        self.f2py_opts = '--quiet'

    def run(self):
        self.run_command('build_cy')
        if self._has_fortran():
            Path.cwd().joinpath('.f2py_f2cmap').write_text(repr(F2PY_TABLE))
        super().run()

    def pyrex_sources(self, sources, extension):
        return sources

    def _has_fortran(self):
        return any(has_f_sources(ext.sources) for ext in self.extensions)


class SDistCommand(sdist):
    def run(self):
        self.run_command('build_cy')
        super().run()

    def get_file_list(self):
        super().get_file_list()
        self.filelist.append('hooks.py')


cmdclass = {
    'build_clib': BuildClibCommand,
    'build_cy': BuildCyCommand,
    'build_ext': BuildExtCommand,
    'build_src': BuildSrcCommand,
    'sdist': SDistCommand,
}
