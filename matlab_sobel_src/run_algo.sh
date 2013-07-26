#!/bin/bash

#export DYLD_LIBRARY_PATH=$DYLIB_LIBRARY_PATH:./lib:/Applications/MATLAB_R2012a.app/runtime/maci64:/Applications/MATLAB_R2012a.app/sys/os/maci64

export MATLAB_ROOT=/usr/local/MATLAB/MATLAB_Compiler_Runtime/v715
#export ARCH=maci64
export ARCH=glnxa64
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/:$LD_LIBRARY_PATH:$PATH:$MATLAB_ROOT/runtime/$ARCH:$MATLAB_ROOT/sys/os/$ARCH

#./out/matrixdriver.app/Contents/MacOS/matrixdriver ./examples/lena.pgm ./examples/lena.out.png
#./out/matrixdriver.app/Contents/MacOS/matrixdriver $1 $2 
matrixdriver $1 $2 
