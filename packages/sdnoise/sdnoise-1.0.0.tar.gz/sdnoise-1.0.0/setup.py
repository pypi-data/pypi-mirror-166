from distutils.core import setup, Extension
from os.path import abspath

print(abspath('./deps/perlin-noise/src'))

sdnoise = Extension('sdnoise',
                    include_dirs=['deps/perlin-noise/src'],
                    sources = ['deps/perlin-noise/src/sdnoise1234.c',
                               'deps/perlin-noise/src/srdnoise23.c',
                               'src/sdnoisemodule.c'])

setup (name = 'sdnoise',
       platforms='any',
       version = '1.0.0',
       ext_modules = [sdnoise],
       include_package_data=True)
