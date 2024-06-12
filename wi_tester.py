"""
   author: josuerom
   created: 25/04/24 10:45:39
"""
import os
import sys
import glob
import shutil
import webbrowser
import subprocess
import requests
from termcolor    import colored
from bs4          import BeautifulSoup
from html.parser  import HTMLParser


def probar_solucion(programa):
   if programa.strip().endswith(".py"):
      ejecutar_python(programa)
   elif programa.strip().endswith(".cpp"):
      compilar_cpp(programa)
   elif programa.strip().endswith(".java"):
      ejecutar_java(programa)
   else:
      extension = programa.split(".")[-1]
      print(colored(f"No hay soporte agregado para programas .{extension}", "red"))


def copiar_plantilla(destino, nombre, lenguaje):
   plantilla_cpp, plantilla_java, plantilla_py = "template.cpp", "template.java", "template.py"
   if lenguaje == "cpp":
      origen_plantilla = os.path.join(ubicacion_plantillas(), plantilla_cpp)
   elif lenguaje == "java":
      origen_plantilla = os.path.join(ubicacion_plantillas(), plantilla_java)
   elif lenguaje == "py":
      origen_plantilla = os.path.join(ubicacion_plantillas(), plantilla_py)
   else:
      print(colored(f"No existe soporte para plantillas .{lenguaje}", "red"))
      return
   ubicacion_destino = os.path.join(destino, f"{nombre}.{lenguaje}")
   if not os.path.exists(destino):
      os.makedirs(destino)
   shutil.copyfile(origen_plantilla, ubicacion_destino)
   if lenguaje == "java":
      with open(ubicacion_destino, 'r') as plantilla:
         contenido = plantilla.readlines()
      with open(ubicacion_destino, 'w') as plantilla:
         for linea in contenido:
            if linea.strip().startswith("public class"):
               linea = "public class " + nombre + " {\n"
            plantilla.write(linea)

   print(colored(f"Plantilla creada con éxito!", "green"))


def ubicacion_plantillas():
   return f"d:\\workspace\\contest\\templates"


def ubicacion_archivo_entrada_salida():
   return f"d:\\workspace\\codeforces\\src\\samples"


def ubicacion_nombre_ejecutable():
   return f"d:\\workspace\\bin\\pytester.exe"


def obtener_entrada_salida(concurso, problema):
   directorio_entradas_salidas = os.path.join(ubicacion_archivo_entrada_salida())
   if not os.path.exists(directorio_entradas_salidas):
      os.makedirs(directorio_entradas_salidas)
   else:
      archivos_txt = glob.glob(os.path.join(directorio_entradas_salidas, "*.txt"))
      for archivo in archivos_txt:
         os.remove(archivo)
   url = f"https://codeforces.com/contest/{concurso}/problem/{problema}"
   respuesta = requests.get(url)
   if respuesta.status_code == 200:
      soup = BeautifulSoup(respuesta.text, 'html.parser')
      input_divs = soup.find_all('div', class_='input')
      answer_divs = soup.find_all('div', class_='output')

      def formatear_captura(captura) -> str:
         captura = captura.split("\n")
         limpieza, sz = "", len(captura)
         for linea in captura:
            linea = linea.strip()
            sz += 1
            if linea.lower() == "input" or linea.lower() == "output" or (sz >= len(captura) - 2 and linea == ""):
               continue
            limpieza += linea + "\n"
         return limpieza

      for i, (input_div, answer_div) in enumerate(zip(input_divs, answer_divs), start=1):
         input_txt = formatear_captura(parsear_html(input_div))
         answer_txt = formatear_captura(parsear_html(answer_div))
         with open(f"{ubicacion_archivo_entrada_salida()}/in{i}.txt", "w") as input_file:
            input_file.write(input_txt)
         print(colored(f"Caso {i} copiado ✔️", "yellow"))
         with open(f"{ubicacion_archivo_entrada_salida()}/ans{i}.txt", "w") as answer_file:
            answer_file.write(answer_txt)
         print(colored(f"Respuesta {i} copiada ✔️", "yellow"))
   else:
      print(colored(f"Error fatal en:", "red"), url)


class HTMLContentParser(HTMLParser):
   def __init__(self):
      super().__init__()
      self.output = []

   def handle_data(self, data):
      self.output.append(data)


def parsear_html(html_content):
   parser = HTMLContentParser()
   parser.feed(str(html_content))
   content = '\n'.join(parser.output)
   return content


def enviar_posible_solucion(concurso):
   url = f"https://codeforces.com/contest/{concurso}/submit"
   try:
      webbrowser.open(url)
   except requests.RequestException as e:
      print(colored(f"Error al hacer la solicitud:", "red"), e)


def ejecutar_python(programa):
   for i in range(1, 11):
      entrada_estandar = f"{ubicacion_archivo_entrada_salida()}/in{i}.txt"
      respuesta = f"{ubicacion_archivo_entrada_salida()}/ans{i}.txt"
      if not os.path.exists(entrada_estandar):
         break
      with open(entrada_estandar, "r") as contenido_archivo_entrada:
         input_txt = "".join(contenido_archivo_entrada.readlines())
      proceso = subprocess.Popen(["python", "-OO", "-S", "-B", programa], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
      salida_generada, _ = proceso.communicate(input=input_txt)
      with open(respuesta, "r") as contenido_archivo_respuesta:
         salida_esperada = contenido_archivo_respuesta.read()
      if salida_generada.strip() == salida_esperada.strip():
         print(colored(f"Caso {i} pasado ✅", "green"))
      else:
         print(colored(f"WA en Caso {i}:", "red"))
         print(f"Respuesta:\n{salida_esperada}")
         print(f"Salida:\n{salida_generada}")


def compilar_cpp(programa):
   def ejecutar_cpp():
      for i in range(1, 11):
         entrada_estandar = f"{ubicacion_archivo_entrada_salida()}/in{i}.txt"
         respuesta = f"{ubicacion_archivo_entrada_salida()}/ans{i}.txt"
         if not os.path.exists(entrada_estandar):
            break
         with open(entrada_estandar, "r") as contenido_archivo_entrada:
            input_txt = "".join(contenido_archivo_entrada.readlines())
         proceso = subprocess.Popen([ubicacion_nombre_ejecutable()], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
         salida_generada, _ = proceso.communicate(input=input_txt)
         with open(respuesta, "r") as contenido_archivo_respuesta:
            salida_esperada = contenido_archivo_respuesta.read()
         if salida_generada.strip() == salida_esperada.strip():
            print(colored(f"Caso {i} pasado ✅", "green"))
         else:
            print(colored(f"WA en Caso {i}:", "red"))
            print(f"Respuesta:\n{salida_esperada}")
            print(f"Salida:\n{salida_generada}")

   proceso_compilacion = subprocess.Popen(["g++", "-std=c++17", "-O2", "-DDEGUB", programa, "-o", ubicacion_nombre_ejecutable()],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   _, salida_compilacion = proceso_compilacion.communicate()
   if proceso_compilacion.returncode == 0:
      ejecutar_cpp()
   else:
      print(colored(f"Error de compilación:", "red"), salida_compilacion, end="\n")


def ejecutar_java(programa):
   """
      Función especifica para versiones de Java mayores a la 8
   """
   for i in range(1, 11):
      entrada_estandar = f"{ubicacion_archivo_entrada_salida()}/in{i}.txt"
      respuesta = f"{ubicacion_archivo_entrada_salida()}/ans{i}.txt"
      if not os.path.exists(entrada_estandar):
         break
      with open(entrada_estandar, "r") as contenido_archivo_entrada:
         input_txt = "".join(contenido_archivo_entrada.readlines())
      proceso = subprocess.Popen(["java", programa], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
      salida_generada, _ = proceso.communicate(input=input_txt)
      with open(respuesta, "r") as contenido_archivo_respuesta:
         salida_esperada = contenido_archivo_respuesta.read()
      if salida_generada.strip() == salida_esperada.strip():
         print(colored(f"Caso {i} pasao ✅", "green"))
      else:
         print(colored(f"WA en Caso {i}:", "red"))
         print(f"Respuesta:\n{salida_esperada}")
         print(f"Salida:\n{salida_generada}")


if __name__ == "__main__":
   """En Windows
      Para copiar y pegar una plantilla:
      python wi_tester.py -g <destino> <nombre programa>.<extension>

      Para obtener los casos de prueba con las salidas:
      python wi_tester.py -p <id concurso>/<id problema>

      Para verificar solución con todos los casos de prueba:
      python wi_tester.py -t <programa>

      Para pegar la posible solución en el navegador:
      python wi_tester.py -s <id concurso>
   """
   size_args = len(sys.argv)
   if size_args > 4 or sys.argv[1] != "-p" and sys.argv[1] != "-t" and sys.argv[1] != "-g" and sys.argv[1] != "-s":
      print(colored("Mijito/a hay un error en ->", "red"), sys.argv)
   elif size_args == 3 and sys.argv[1] == "-t":
      probar_solucion(sys.argv[2])
   elif size_args == 3 and sys.argv[1] == "-p":
      concurso, problema = sys.argv[2].split("/")
      obtener_entrada_salida(concurso, problema)
   elif size_args == 4 and sys.argv[1] == "-g":
      destino = sys.argv[2]
      nombre, lenguaje = sys.argv[3].split(".")
      copiar_plantilla(destino, nombre, lenguaje.lower())
   elif size_args == 3 and sys.argv[1] == "-s":
      concurso = sys.argv[2]
      enviar_posible_solucion(concurso)
   else:
      print(colored(f"Error fatal en:", "red"), sys.argv)
