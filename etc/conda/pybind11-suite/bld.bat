echo ON

%PYTHON% %RECIPE_DIR%\\filter.py --src=%PREFIX%\\Library --dst=filtered.pkl
if errorlevel 1 exit 1

rem mkdir build
rem if errorlevel 1 exit 1
rem cd build
rem if errorlevel 1 exit 1

rem set PATH="c:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0\x64\";%PATH%
rem if errorlevel 1 exit 1

rem cmake -G "%CMAKE_GENERATOR%" ^
rem       -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON ^
rem       -D CMAKE_INSTALL_PREFIX=%PREFIX% ^
rem       -D USE_PYTHON_INCLUDE_DIR=ON ^
rem       -D PYBIND11_TEST=OFF ^
rem       ..
rem more CMakeFiles\CMakeOutput.log
rem if errorlevel 1 exit 1

rem nmake
rem if errorlevel 1 exit 1

rem nmake install
rem if errorlevel 1 exit 1

rem set PYBIND11_USE_CMAKE=1
rem cd ..
%PYTHON% setup.py install --single-version-externally-managed --record record.txt
if errorlevel 1 exit 1

%PYTHON% %RECIPE_DIR%\\move.py --src=%PREFIX%\\include --dst=%SRC_DIR%\\Library\\include --filtered=filtered.pkl
%PYTHON% %RECIPE_DIR%\\move.py --src=%PREFIX%\\Lib --dst=%SRC_DIR%\\Library\\Lib --filtered=filtered.pkl

echo OFF