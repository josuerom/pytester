# pytester
Testeador, parseador y generador de plantillas para programas escritos en los lenguajes de programación C++, Java y Python. Estas herramientas están especialmente diseñadas para abordar problemas directos en la plataforma [codeforces](https://codeforces.com/problemset) de manera ligera.

Para que estas automatizaciones funcionen correctamente, se necesita de: `pip install requests beautifulsoup4 termcolor`

Solo debe modificar las líneas `29`, `55`, `59`, `168` y `156`.

Luego de haber modificado el programa y te esté funcionando correctamente, entonces ⤵️

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

Ahora, debes agregar la ruta en donde se encuentre el ejecutable `build\wi_tester.exe` al PATH (Variables de entorno), para que cuando escribas el nombre del ejecutable desde cualquier
ubicación en la terminal lo pueda reconocer como un comando, y así mantener mayor velocidad.

### En Linux
Ejecuta todas estas instrucciones dentro de la carpeta que contiene el modulo.py

Primero se crea un entorno virtual para poder instalar el paquete, luego se instala el paquete para el proyecto
```python
python3 -m venv venv
source venv/bin/activate
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
Una vez haya hecho esto y haya salido bien, entonces puede invocar al ejecutable desde cualquier parte de la terminal con el nombre que le haya dejado al binario.
