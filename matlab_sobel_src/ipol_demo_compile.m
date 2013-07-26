%% para generar la biblioteca
mcc -d lib -B cpplib:libmatrixp ./src/processing.m -a ./src/toolbox -v
%% para compilar el  ejecutable
mbuild ./src/matrixdriver.cpp -outdir ./out -L./lib  -lmatrixp -I./lib

% borrar los mcr's
% system('rmdir /S /Q "C:\Program Files\3DVIA\Virtools 5.0\BuildingBlocks\libbones_preprocessing_mcr"');
% system('rmdir /S /Q "C:\Program Files\3DVIA\Virtools 5.0\BuildingBlocks\libbones_radio_mcr"');
