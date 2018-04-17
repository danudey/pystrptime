from distutils.core import setup, Extension

strptime = Extension('strptime',
                    sources = ['src/strptime.c'])

setup (name = 'strptime',
       version = '1.0',
       description = 'Parse a string in C',
       ext_modules = [strptime])
