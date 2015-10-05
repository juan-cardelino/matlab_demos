matlab_demos
============

1. Sobre el proceso
1.1- Compilación
Se compila con un makefile trivial que invoca al compilador de matlab
mcc. Al considerarlo un compilador, asumimos razonable que este en el
path (en purple estará, el usuario deberá cambiarlo en su máquina).
El método build debe copiar ejecutable y script al bin

1.2-Ejecución
Se ejecuta mediante el script llamando al run_proc modificado
(re-agrega el path del sistema)
Se sugiere usar una variable self.matlab_path que tiene precargada la
ruta al matlab.

2.- Modificación al sistema de demos
demo.conf tiene que tener una variable matlab.path que va a un default
si no está
se cambia una línea en el init de empty_app que setea matlab.path a lo
leido del demo.conf.
Es decir que el cambio en el sistema de demos es una línea.
Miguel, te parece bien este lugar para leerlo o tenés otra sugerencia?

3.- Sobre documentación y ejemplos
Armé un repo en github con todo: https://github.com/juan-cardelino/matlab_demos/
Lo hice todo sobre el ipol_demo-light-1025b85
Ahi encontrarán varias cosas:

3.1- matlab.patch: patch para aplicar al sistema de demos
cd ipol_demo-light-1025b85
patch -p0<matlab.patch

3.2 ipol_demo-light-1025b85
lighweight demo server already patched and configured

3.3 demos/matlab_gauss
Demo matlab de José que hace Gaussian Blur con matlab. modificado por
mi para cumplir con el nuevo estandar.

Actualicé minimamente el documento técnico:
https://github.com/juan-cardelino/matlab_demos/blob/master/doc/matlab_complete_header.pdf
Les pido que miren el compilation how to en sección 2.8 que escribió
José y el demo how to que escribí ahora en la 2.9

3.4 demos/matlab_sobel
Primer demo matlab hecho por mi, todavía no lo actualicé a la nueva versión.

Espero vuestros comentarios, pero creo que esto recoge bastante bien
todo lo que discutimos.
