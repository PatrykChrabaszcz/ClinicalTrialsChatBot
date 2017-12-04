import os
import sys

from cx_Freeze import setup, Executable

interpreter_path = os.path.dirname(sys.executable)

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages=[
        'numpy',
        'pyqt5',
        'idna',
        # 'PyQtChart',
        'psycopg2',
        'apiai'
    ],
    excludes=[],
    include_files=['resources/']
)

base = 'Win32GUI' if sys.platform == 'win32' else None
# base = 'console'

executables = [
    Executable('main.py', base=base, targetName='SimpleTrial.exe', icon='resources/icon.ico')
]

setup(name='SimpleTrial',
      version='1.0',
      description='A solution for human-like interaction with https://clinicaltrials.gov/',
      author='TeamName',
      maintainer='Oleksii Zhelo',
      maintainer_email='aleks.zhelo@gmail.com',
      options=dict(build_exe=buildOptions),
      executables=executables)
