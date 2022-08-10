from cx_Freeze import setup, Executable

files=['industriasDMU.png','176A1-A4602.png','186A1-A4600.png','176A1-A4600.png','H60.png',
       '186A1-A4902.png','176A1-A4902.png','SinCorriente.png','check.png','dmu.ico']

target = Executable(
    script='switchesProgram.py',
    base = 'Win32GUI',
    icon= 'dmu.ico'
)

setup(
    name="CheckSistem",
    version="1.3",
    description="Sistema de verificacion de switches",
    author='Armando Nava Betancourt',
    options={"build_exe": {'include_files':files}},
    executables=[target]
)