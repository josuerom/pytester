"""
   author: josuerom
   created: 25/04/24 10:45:39
"""
import os
import sys
import shutil
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
      print(colored(f"No hay soporte para programas .{extension}", "red"))
      return


def copiar_plantilla(destino, nombre, lenguaje):
   origen = f"/home/josuerom/Workspace/contest/TEMPLATES"
   if lenguaje == "cpp":
      ruta_origen = os.path.join(origen, "template.cpp")
   elif lenguaje == "java":
      ruta_origen = os.path.join(origen, "template.java")
   elif lenguaje == "py":
      ruta_origen = os.path.join(origen, "template.py")
   else:
      print(colored(f"No existe plantilla para .{lenguaje}", "red"))
      return
   ruta_destino = os.path.join(destino, f"{nombre}.{lenguaje}")
   if not os.path.exists(destino):
      os.makedirs(destino)
   shutil.copyfile(ruta_origen, ruta_destino)
   if lenguaje == "java":
      with open(ruta_destino, 'r') as plantilla:
         lineas = plantilla.readlines()
      with open(ruta_destino, 'w') as plantilla:
         for linea in lineas:
            if linea.strip().startswith("public class"):
               linea = "public class " + nombre + " {\n"
            plantilla.write(linea)
   print(colored(f"Plantilla creada con éxito.", "green"))


def ruta_samples():
   colocar_en = f"/home/josuerom/Workspace/codeforces/src/samples"
   return colocar_en


def eliminar_todos_los_samples():
   directorio_entradas_salidas = os.path.join(ruta_samples())
   if not os.path.exists(directorio_entradas_salidas):
      os.makedirs(directorio_entradas_salidas)
   else:
      archivos_txt = os.path.join(directorio_entradas_salidas, "*.txt")
      subprocess.run(["rm", "-rf", archivos_txt])


def obtener_input_answer(id_contest, id_problema):
    eliminar_todos_los_samples()
    url = f"https://codeforces.com/contest/{id_contest}/problem/{id_problema}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        input_divs = soup.find_all('div', class_='input')
        answer_divs = soup.find_all('div', class_='output')
        for i, (input_div, answer_div) in enumerate(zip(input_divs, answer_divs), start=1):
            input_txt = formatear_captura(parsear_html(input_div))
            answer_txt = formatear_captura(parsear_html(answer_div))
            with open(f"{ruta_samples()}/in{i}.txt", "w") as input_file:
               input_file.write(input_txt.strip())
            print(colored(f"Test case {i} copiado ☑️", "yellow"))
            with open(f"{ruta_samples()}/ans{i}.txt", "w") as answer_file:
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
   captura = captura.strip().split("\n")
   limpieza = []
   for i in range(len(captura) - 1):
      captura[i].strip()
      if captura[i] != "Input" and captura[i] != "Output" and captura[i] == False and i < 3:
         limpieza.append(i)
   return '\n'.join(limpieza)


def ejecutar_python(programa):
   for i in range(1, 11):
      entrada_estandar = f"{ruta_samples()}/in{i}.txt"
      salida_estandar = f"{ruta_samples()}/ans{i}.txt"
      if not os.path.exists(entrada_estandar):
         break
      with open(entrada_estandar, "r") as contenido_archivo_entrada:
         input_txt = "".join(contenido_archivo_entrada.readlines())
      proceso = subprocess.Popen(["python3", programa], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
      salida_generada, _ = proceso.communicate(input=input_txt)
      with open(salida_estandar, "r") as contenido_archivo_respuesta:
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
         entrada_estandar = f"{ruta_samples()}/in{i}.txt"
         salida_estandar = f"{ruta_samples()}/ans{i}.txt"
         if not os.path.exists(entrada_estandar):
            break
         with open(entrada_estandar, "r") as contenido_archivo_entrada:
            input_txt = "".join(contenido_archivo_entrada.readlines())
         proceso = subprocess.Popen(["./sol"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
         salida_generada, _ = proceso.communicate(input=input_txt)
         with open(salida_estandar, "r") as contenido_archivo_respuesta:
            salida_esperada = contenido_archivo_respuesta.read()
         if salida_generada.strip() == salida_esperada.strip():
            print(colored(f"Test case {i} passed ✅", "green"))
         else:
            print(colored(f"WA case {i}:", "red"))
            print(f"Output:\n{salida_generada}")
            print(f"Answer:\n{salida_esperada}")

   
   proceso_compilacion = subprocess.Popen(["g++", "-std=c++17", "-O2", programa, "-o", "sol"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   _, salida_compilacion = proceso_compilacion.communicate()
   if proceso_compilacion.returncode == 0:
      ejecutar()
   else:
      print(colored(f"Error de compilación:\n{salida_compilacion}", "red"))


def ejecutar_java(programa):
   for i in range(1, 11):
      entrada_estandar = f"{ruta_samples()}/in{i}.txt"
      salida_estandar = f"{ruta_samples()}/ans{i}.txt"
      if not os.path.exists(entrada_estandar):
         break
      with open(entrada_estandar, "r") as contenido_archivo_entrada:
         input_txt = "".join(contenido_archivo_entrada.readlines())
      proceso = subprocess.Popen(["java", programa], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
      salida_generada, _ = proceso.communicate(input=input_txt)
      with open(salida_estandar, "r") as contenido_archivo_respuesta:
         salida_esperada = contenido_archivo_respuesta.read()
      if salida_generada.strip() == salida_esperada.strip():
         print(colored(f"Test case {i} passed ✅", "green"))
      else:
         print(colored(f"WA case {i}:", "red"))
         print(f"Output:\n{salida_generada}")
         print(f"Answer:\n{salida_esperada}")


if __name__ == "__main__":
   """En Unix (MacOS - Linux)
      Para verificar todos los casos de prueba:
      python wi_tester.py -t <programa>
   
      Para obtener los casos de prueba con las salidad:
      python wi_tester.py -p <id_contest>/<id_problema>

      Para copiar y pegar la plantilla:
      python wi_tester.py -g <destino> <nombre_programa>.<extension>
   """
   size_args = len(sys.argv)
   if size_args > 4 or sys.argv[1] != "-p" and sys.argv[1] != "-t" and sys.argv[1] != "-g":
      print(colored("Mijito/a instrucción invalida!", "red"), str(sys.argv))
   elif size_args == 3 and sys.argv[1] == "-t":
      probar_solucion(sys.argv[2])
   elif size_args == 3 and sys.argv[1] == "-p":
      id_contest, id_problema = sys.argv[2].split("/")
      obtener_input_answer(id_contest, id_problema)
   elif size_args == 4 and sys.argv[1] == "-g":
      destino = sys.argv[2]
      nombre, lenguaje = sys.argv[3].split(".")
      copiar_plantilla(destino, nombre, lenguaje.lower())
   else:
      print(colored("Mijito/a instrucción invalida!", "red"), str(sys.argv))
