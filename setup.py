from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'Console'

executables = [
    Executable('run.py', base=base, target_name = 'RUN')
]

setup(name='Momento_Mockup_Generator',
      version = '1.1',
      description = 'Just drop label PDFs into the DROP HERE folder and wait for the magic to happen.',
      options = {'build_exe': build_options},
      executables = executables)
