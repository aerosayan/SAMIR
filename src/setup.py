from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

extensions = [Extension("samir",
                        sources = ["samir.pyx","main.cpp",'Node.cpp',
                        'GridGenerator.cpp'],
                        #extra_link_args = ['-static']
                        )
]
setup(
    cmdclass = {'build_ext':build_ext},
    ext_modules = cythonize(extensions)
) # end setup
