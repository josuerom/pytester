"""
   author: josuerom
   created: 25/04/24 10:45:39
"""
import os
import sys
import shutil
import webbrowser
import subprocess
import requests
from termcolor import colored
from bs4 import BeautifulSoup
from html.parser import HTMLParser


def probar_solucion(programa):
   if programa.strip().endswith(".py"):
      ejecutar_python(programa)
   elif programa.strip().endswith(".cpp"):
      compilar_ejecutar_cpp(programa)
   elif programa.strip().endswith(".java"):
      ejecutar_java(programa)
   else:
      extension = programa.split(".")[-1]
      print(colored(f"No hay soporte para programas [.{extension}]", "red"))


def copiar_plantilla(destino, nombre, lenguaje):
   plantilla_cpp, plantilla_java, plantilla_py = "template.cpp", "template.java", "template.py"
   if lenguaje == "cpp":
      origen_plantilla = os.path.join(ruta_plantillas(), plantilla_cpp)
   elif lenguaje == "java":
      origen_plantilla = os.path.join(ruta_plantillas(), plantilla_java)
   elif lenguaje == "py":
      origen_plantilla = os.path.join(ruta_plantillas(), plantilla_py)
   else:
      print(colored(f"No existe plantilla para [.{lenguaje}]", "red"))
      return
   ubicacion_destino = os.path.join(destino, f"{nombre}.{lenguaje}")
   if not os.path.exists(destino):
      os.makedirs(destino)
   shutil.copyfile(origen_plantilla, ubicacion_destino)
   if lenguaje == "java":
      with open(ubicacion_destino, 'r') as plantilla:
         lineas = plantilla.readlines()
      with open(ubicacion_destino, 'w') as plantilla:
         for linea in lineas:
            if linea.strip().startswith("public class"):
               linea = "public class " + nombre + " {\n"
            plantilla.write(linea)
   print(colored(f"Plantilla creada con éxito.", "green"))


def ruta_plantillas():
   return f"/home/josuerom/Workspace/contest/templates"


def ruta_archivos_de_entrada():
   return f"/home/josuerom/Workspace/codeforces/src/samples"


def obtener_input_answer(concurso, problema):
   directorio_entradas_respuestas = os.path.join(ruta_archivos_de_entrada())
   if not os.path.exists(directorio_entradas_respuestas):
      os.makedirs(directorio_entradas_respuestas)
   else:
      archivos_txt = os.path.join(directorio_entradas_respuestas, "*.txt")
      subprocess.run(["rm", "-rf", archivos_txt])    url = f"https://codeforces.com/contest/{concurso}/problem/{problema}"
   respuesta = requests.get(url)
   if respuesta.status_code == 200:
      soup = BeautifulSoup(respuesta.text, 'html.parser')
      input_divs = soup.find_all('div', class_='input')
      answer_divs = soup.find_all('div', class_='output')
      for i, (input_div, answer_div) in enumerate(zip(input_divs, answer_divs), start=1):
         input_txt = formatear_captura(parsear_html(input_div))
         answer_txt = formatear_captura(parsear_html(answer_div))
         with open(f"{ruta_archivos_de_entrada()}/in{i}.txt", "w") as input_file:
            input_file.write(input_txt.strip())
         print(colored(f"Test case {i} copiado ☑️", "yellow"))
         with open(f"{ruta_archivos_de_entrada()}/ans{i}.txt", "w") as answer_file:
            answer_file.write(answer_txt.strip())
         print(colored(f"Answer {i} copiado ☑️", "yellow"))
   else:
      print("Error fatal en:", colored(f"{url}", "red"))


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


def formatear_captura(captura):
   captura = captura.split("\n")
   limpieza = []
   for i in range(len(captura) - 1):
      linea = captura[i].strip()
      if len(limpieza) > 0 and linea == "":
         limpieza.append(linea)
         continue
      if linea != "Input" and linea != "Output" and linea == True:
         limpieza.append(linea)
   return '\n'.join(limpieza)


def pegar_posible_solucion(concurso, problema):
   url = f"https://codeforces.com/contest/{concurso}/submit/{problema}"
   respuesta = requests.head(url)
   if respuesta.status_code == 200:
      webbrowser.get('firefox').open_new_tab(url)
   else:
      print(colored(f"La URL no existe:", "red"), url)


def ejecutar_python(programa):
   for i in range(1, 11):
      entrada_estandar = f"{ruta_archivos_de_entrada()}/in{i}.txt"
      respuesta = f"{ruta_archivos_de_entrada()}/ans{i}.txt"
      if not os.path.exists(entrada_estandar):
         break
      with open(entrada_estandar, "r") as contenido_archivo_entrada:
         input_txt = "".join(contenido_archivo_entrada.readlines())
      proceso = subprocess.Popen(["python3", "-OO", "-S", "-B", programa], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
      salida_generada, _ = proceso.communicate(input=input_txt)
      with open(respuesta, "r") as contenido_archivo_respuesta:
         salida_esperada = contenido_archivo_respuesta.read()
      if salida_generada.strip() == salida_esperada.strip():
         print(colored(f"Test case {i} passed ✅", "green"))
      else:
         print(colored(f"WA case {i}:", "red"))
         print(f"Output:\n{salida_generada}")
         print(f"Answer:\n{salida_esperada}")


def compilar_ejecutar_cpp(programa):
   def ejecutar():
      for i in range(1, 11):
         entrada_estandar = f"{ruta_archivos_de_entrada()}/in{i}.txt"
         respuesta = f"{ruta_archivos_de_entrada()}/ans{i}.txt"
         if not os.path.exists(entrada_estandar):
            break
         with open(entrada_estandar, "r") as contenido_archivo_entrada:
            input_txt = "".join(contenido_archivo_entrada.readlines())
         proceso = subprocess.Popen(["/home/josuerom/Workspace/bin/test.out"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
         salida_generada, _ = proceso.communicate(input=input_txt)
         with open(respuesta, "r") as contenido_archivo_respuesta:
            salida_esperada = contenido_archivo_respuesta.read()
         if salida_generada.strip() == salida_esperada.strip():
            print(colored(f"Test case {i} passed ✅", "green"))
         else:
            print(colored(f"WA case {i}:", "red"))
            print(f"Output:\n{salida_generada}")
            print(f"Answer:\n{salida_esperada}")


   proceso_compilacion = subprocess.Popen(["g++", "-std=c++17", "-O2", programa, "-o", "/home/josuerom/Workspace/bin/test.out"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   _, salida_compilacion = proceso_compilacion.communicate()
   if proceso_compilacion.returncode == 0:
      ejecutar()
   else:
      print(colored(f"Error de compilación:", "red"), salida_compilacion, end="\n")


def ejecutar_java(programa):
   for i in range(1, 11):
      entrada_estandar = f"{ruta_archivos_de_entrada()}/in{i}.txt"
      respuesta = f"{ruta_archivos_de_entrada()}/ans{i}.txt"
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
         print(colored(f"Test case {i} passed ✅", "green"))
      else:
         print(colored(f"WA case {i}:", "red"))
         print(f"Output:\n{salida_generada}")
         print(f"Answer:\n{salida_esperada}")


if __name__ == "__main__":
   """En (MacOS & Linux)
      Para copiar y pegar una plantilla:
      python3 un_tester.py -g <destino> <nombre programa>.<extension>

      Para obtener los casos de prueba con las salidas:
      python3 un_tester.py -p <id concurso>/<id problema>

      Para verificar solución con todos los casos de prueba:
      python3 un_tester.py -t <programa>

      Para pegar la posible solución en la página:
      python3 un_tester.py -s <id concurso>/<id problema>
   """
   size_args = len(sys.argv)
   if size_args > 4 or sys.argv[1] != "-p" and sys.argv[1] != "-t" and sys.argv[1] != "-g" and sys.argv[1] != "-s":
      print(colored("Mijito/a instrucción invalida!", "red"), str(sys.argv))
   elif size_args == 3 and sys.argv[1] == "-t":
      probar_solucion(sys.argv[2])
   elif size_args == 3 and sys.argv[1] == "-p":
      concurso, problema = sys.argv[2].split("/")
      obtener_input_answer(concurso, problema)
   elif size_args == 4 and sys.argv[1] == "-g":
      destino = sys.argv[2]
      nombre, lenguaje = sys.argv[3].split(".")
      copiar_plantilla(destino, nombre, lenguaje.lower())
   elif size_args == 3 and sys.argv[1] == "-s":
      concurso, problema = sys.argv[2].split("/")
      pegar_posible_solucion(concurso, problema.lower())
   else:
      print(colored(f"Error fatal en:", "red"), sys.argv)
