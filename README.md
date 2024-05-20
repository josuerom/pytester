# pytester
Testeador, parseador y generador de plantillas para programas escritos en los lenguajes de programación C++, Java y Python. Estas herramientas están especialmente diseñadas para abordar problemas directos en la plataforma [codeforces](https://codeforces.com/problemset) de manera ágil.

Para que estas automatizaciones funcionen correctamente, debe instalar los tres paquetes de terceros: `pip install requests beautifulsoup4 termcolor`

## Lo que debe hacer
Modifique las líneas `29`, `55`, `59`, `168` y `156` según sus necesidades. Además, si es que no tiene una carpeta en donde tenga las plantillas, entonces deberá crearla.

Luego de haber modificado el programa y le esté funcionando el programa correctamente, entonces ⤵️

## Convierte el modulo a un ejecutable
### En Windows
Instala el paquete
```python
pip install pyinstaller
```
Ejecuta la instrucción con el nombre del modulo.py, en la misma ubicación que se encuentre el archivo
```python
pyinstaller --onefile wi_tester.py
```

Ahora, debes agregar la ruta en donde se encuentre el ejecutable `build\wi_tester.exe` al PATH (Variables de entorno), por ejemplo al PATH: `%HOMEPATH%\pytester\build`, para que cuando escribas el nombre del ejecutable desde cualquier parte dentro de la terminal lo pueda reconocer como un comando, y así mantener una mayor velocidad.

### En Linux
Ejecuta todas estas instrucciones dentro de la carpeta que contiene el modulo.py

Primero se crea un entorno virtual para poder instalar el paquete, luego se instala el paquete para el proyecto
```python
python3 -m venv env
source env/bin/activate
pip install pyinstaller
```
Ahora se realiza la conversión a ejecutable para linux `/build/un_tester`
```python
pyinstaller --onefile un_tester.py
```

Ahora, debes mover el archivo ejecutable al directorio de binarios y concederle los permisos de ejecución
```bash
sudo mv build/un_tester /usr/bin
sudo chmod +x /usr/bin/un_tester
```
Una vez haya hecho esto y haya salido bien, entonces puede invocar al ejecutable desde cualquier parte de la terminal con el nombre que le haya dejado al binario
añadido a la ruta `/usr/bin/` como `un_tester`, renombre con el comando `sudo mv /usr/bin/un_tester /usr/bin/pytester`.
