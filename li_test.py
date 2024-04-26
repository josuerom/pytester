"""
   author: josuerom
   created: 25/04/24 10:45:39
"""
import sys
import os
import shutil
import subprocess
import requests
from termcolor import colored
from bs4 import BeautifulSoup


def probar_solucion(programa):
   if programa.strip().endswith(".py"):
      ejecutar_python(programa)
   elif programa.strip().endswith(".cpp"):
      compilar_y_ejecutar_cpp(programa)
   elif programa.strip().endswith(".java"):
      ejecutar_java(programa)
   else:
      extension = programa.split(".")[-1]
      print(colored(f"No hay soporte para programas .{extension}", "magenta"))
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
   ruta_destino = os.path.join(destino, nombre)
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
   ruta_por_defecto = f"/home/josuerom/Workspace/codeforces/src/samples"
   return ruta_por_defecto


def eliminar_archivos_de_entrada():
   directorio_entradas_salidas = os.path.join(ruta_samples())
   if not os.path.exists(directorio_entradas_salidas):
      os.makedirs(directorio_entradas_salidas)
   else:
      archivos_txt = os.path.join(directorio_entradas_salidas, "*.txt")
      subprocess.run(["rm", "-rf", archivos_txt])


def obtener_input_output(id_contest, id_problema):
   eliminar_archivos_de_entrada()
   url = f"https://codeforces.com/contest/{id_contest}/problem/{id_problema}"
   response = requests.get(url)
   if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      input_divs = soup.find_all('div', class_='input')
      output_divs = soup.find_all('div', class_='output')

      for i, (input_div, output_div) in enumerate(zip(input_divs, output_divs), start=1):
         input_text = input_div.find('pre').get_text()
         output_text = output_div.find('pre').get_text()
         with open(f"{ruta_samples()}/in{i}.txt", "w") as input_file:
            input_file.write(input_text.strip())
         print(colored(f"Test case {i} copied ☑️", "yellow"))
         with open(f"{ruta_samples()}/ans{i}.txt", "w") as output_file:
            output_file.write(output_text.strip())
         print(colored(f"Answer {i} copied ☑️", "yellow"))
   else:
      print("Error fatal en:", colored(f"{url}", "red"))


def ejecutar_python(programa):
   for i in range(1, 11):
      entrada_estandar = f"{ruta_samples()}/in{i}.txt"
      respuesta_correcta = f"{ruta_samples()}/ans{i}.txt"
      if not os.path.exists(entrada_estandar):
         break
      with open(entrada_estandar, "r") as contenido_archivo_de_entrada:
         entrada_estandar_datos = contenido_archivo_de_entrada.read().strip()
      proceso = subprocess.Popen(["python3", programa], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
      salida_generada, _ = proceso.communicate(input=entrada_estandar_datos)
      with open(respuesta_correcta, "r") as contenido_archivo_de_entrada:
         salida_esperada = contenido_archivo_de_entrada.read().strip()
      if salida_generada.strip() == salida_esperada.strip():
         print(colored(f"Test case {i} passed ✅", "green"))
      else:
         print(colored(f"WA case {i}:", "red"))
         print(f"Output:\n{salida_generada}", end="\n")
         print(f"Answer:\n{salida_esperada}")


def compilar_y_ejecutar_cpp(programa):
   def ejecutar(programa):
      for i in range(1, 11):
         entrada_estandar = f"{ruta_samples()}/in{i}.txt"
         respuesta_correcta = f"{ruta_samples()}/ans{i}.txt"
         if not os.path.exists(entrada_estandar):
               break
         with open(entrada_estandar, "r") as contenido_archivo_de_entrada:
               entrada_estandar_datos = contenido_archivo_de_entrada.read().strip()
         proceso = subprocess.Popen(["./" + programa], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True)
         salida_generada, _ = proceso.communicate(input=entrada_estandar_datos)
         with open(respuesta_correcta, "r") as contenido_archivo_de_entrada:
               salida_esperada = contenido_archivo_de_entrada.read().strip()
         if salida_generada.strip() == salida_esperada.strip():
               print(colored(f"Test case {i} passed ✅", "green"))
         else:
               print(colored(f"WA case {i}:", "red"))
               print(f"Output:\n{salida_generada}", end="\n")
               print(f"Answer:\n{salida_esperada}")

   nombre_ejecutable = programa.replace(".cpp", "")
   proceso_compilacion = subprocess.Popen(["g++ -std=c++17 -O2", programa, "-o", nombre_ejecutable],
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
   _, errores_compilacion = proceso_compilacion.communicate()
   if proceso_compilacion.returncode == 0:
      ejecutar(nombre_ejecutable)
   else:
      print(colored("Error de compilación:", "red"))
      print(errores_compilacion)


def ejecutar_java(programa):
   for i in range(1, 11):
      entrada_estandar = f"{ruta_samples()}/in{i}.txt"
      respuesta_correcta = f"{ruta_samples()}/ans{i}.txt"
      if not os.path.exists(entrada_estandar):
         break
      with open(entrada_estandar, "r") as contenido_archivo_de_entrada:
         entrada_estandar_datos = contenido_archivo_de_entrada.read().strip()
      proceso = subprocess.Popen(["java", programa], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True)
      salida_generada, _ = proceso.communicate(input=entrada_estandar_datos)
      with open(respuesta_correcta, "r") as contenido_archivo_de_entrada:
         salida_esperada = contenido_archivo_de_entrada.read().strip()
      if salida_generada.strip() == salida_esperada.strip():
         print(colored(f"Test case {i} passed ✅", "green"))
      else:
         print(colored(f"WA case {i}:", "red"))
         print(f"Output:\n{salida_generada}", end="\n")
         print(f"Answer:\n{salida_esperada}")


if __name__ == "__main__":
   """En Linux
      Para verificar todos los caso de prueba:
      python3 li_tester.py -t <programa>
   
      Para obtener los casos de prueba del problema:
      python3 li_tester.py -p <id_contest>/<id_problema>

      Para copiar y pegar la plantilla:
      python3 li_tester.py -g <destino> <nombre_programa>.<extension>
   """
   size_args = len(sys.argv)
   if size_args > 4 or sys.argv[1] != "-p" and sys.argv[1] != "-t" and sys.argv[1] != "-g":
      print(colored("Mijito/a instrucción invalida!", "red"))
   elif size_args == 3 and sys.argv[1] == "-t":
      probar_solucion(sys.argv[2])
   elif size_args == 3 and sys.argv[1] == "-p":
      id_contest, id_problema = sys.argv[2].split("/")
      obtener_input_output(id_contest, id_problema)
   elif size_args == 4 and sys.argv[1] == "-g":
      destino = sys.argv[2]
      nombre, lenguaje = sys.argv[3].split(".")
      copiar_plantilla(destino, nombre, lenguaje.lower())
