from distutils.core import setup, Extension
from Cython.Build import cythonize

# extensions = [Extension("query_engine", ["sage_engine.pyx", "filter/*.pyx", "iterators/*.pyx", "optimizer/*.pyx"])]
extensions = [Extension("query_engine", ["sage_engine.pyx"])]

setup(
    ext_modules=cythonize(extensions, annotate=True),
)
