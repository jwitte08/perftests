'''
Created on Mar 26, 2019

@author: jwitte
'''

import argparse
from argparse import RawTextHelpFormatter
import os
import subprocess
import shutil

def parse_args():
    parser = argparse.ArgumentParser(
        description="""Compile and link against LIKWID.""",
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        'src',
        type=str,
        help="""The C++ source to be build."""
    )
    args = parser.parse_args()
    return args

def treeup(path,n=1):
    """Moves file path tree n times up."""
    for step in range(n):
        path = os.path.dirname(path)
    return path

def compile(source):
    """Compiles the C++ file"""
    options = parse_args()
    pwd = os.path.abspath(os.curdir)
    compiler = [
        'g++',
        '-std=c++14',
        '-march=native',
        '-DLIKWID_PERFMON',
        '-fopenmp'
    ]

    def set_includes():
        """set the include directories"""
        likwid_perfctr = shutil.which('likwid-perfctr')
        likwid_dir = treeup(likwid_perfctr,2)
        likwid_include = os.path.join(likwid_dir,'include')
        yield likwid_include
    includes = list(set_includes())
    for d in includes:
        assert os.path.isdir(d),"Include directory ({}) is invalid.".format(d)
    include_flags = [str(r'-I'+path) for path in includes]

    outfile = source.rstrip(r'cc')+'o'
    subprocess.run([*compiler,*include_flags,'-o',outfile,'-c',source])
    print ('compiled: {}'.format(outfile))
    return outfile

def link(objfile):
    """Links the compiled C++ object file"""
    linker = [
        'g++',
        '-rdynamic'
    ]
    library_flags = [
        '-llikwid'
    ]

    def set_rpaths():
        """set the include directories"""
        likwid_perfctr = shutil.which('likwid-perfctr')
        likwid_dir = treeup(likwid_perfctr,2)
        likwid_include = os.path.join(likwid_dir,'lib')
        yield likwid_include
    rpaths = list(set_rpaths())
    for d in rpaths:
        assert os.path.isdir(d),"Runtime path ({}) is invalid.".format(d)
    rpath_flag = r'-Wl,-rpath,'+':'.join(rpaths)
        
    outfile = objfile.rstrip(r'o')+'out'
    subprocess.run([*linker,rpath_flag,'-o',outfile,objfile,*library_flags])
    print ('linked: {}'.format(outfile))
    return outfile

def main():
    options = parse_args()
    source = options.src
    objfile = compile(source)
    program = link(objfile)
    
if __name__ == '__main__':
    main()
