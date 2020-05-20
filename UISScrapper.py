from mechanize import Browser
import bs4 as bs
import urllib.request as ulib
import os
from Asignatura import Asignatura

def getTeachers(htmlCode):

    teachers = []

    for line in htmlCode:
        if "profesor" in line.lower():
            teacher = htmlCode[htmlCode.index(line) + 3]

            if "<" not in teacher:
                teachers.append(teacher)
    
    teachers = list(dict.fromkeys(teachers)) #Elimina los profesores duplicados

    return teachers

def exportToTXT(list):

    file = open("ejemplo.txt", "w")

    for line in list:
        file.write(line + "\n")
    
    file.close()

codigo = "22956"

br = Browser()
br.open("https://www.uis.edu.co/estudiantes/asignaturas_programadas/buscador.html")

br.select_form(name = "form1") # pylint: disable=no-member

br.form['codigo'] = codigo # pylint: disable=no-member
br.submit() # pylint: disable=no-member

soup = bs.BeautifulSoup(br.response().read(), "html.parser") # pylint: disable=no-member
soup = soup.prettify()

HTMLLines = soup.split("\n")
exportToTXT(HTMLLines)

asig = Asignatura(codigo)
os.system("pause")

asignatura = str(HTMLLines[45]).strip()
print(F"Asignatura detectada: {asignatura}")

grupos = []
capacidades = []
estudiantes = []

index = 0

for line in HTMLLines:

    line = str(line).strip()

    if "Grupo" in line:
        grupo = line[7:]
        grupos.append(grupo)
        
        groupCapacity = str(HTMLLines[index + 13]).strip()
        groupStudents = str(HTMLLines[index + 20]).strip()
        capacidades.append(int(groupCapacity))     
        estudiantes.append(int(groupStudents))  
    
    index += 1

print("Grupos encontrados!")

print(grupos)
print("Encontrando profesores . . .")

profesores = []

for grupo in grupos:

    customLink = F"https://www.uis.edu.co/estudiantes/asignaturas_programadas/horario_asignatura.jsp?codigo={codigo}&grupo={grupo}&nombre=CUSTOM"
    
    groupInfo = ulib.urlopen(customLink).read()
    groupSoup = bs.BeautifulSoup(groupInfo, "html.parser")
    groupSoup = groupSoup.prettify().split("\n")

    profesor = getTeachers(groupSoup)
    profesores.append(profesor)


for n in range(len(grupos)):

    print(F"Grupo {grupos[n]} con capacidad de {capacidades[n]} y {estudiantes[n]} matriculados", end=" ")
    print(F"profesor detectado: {profesores[n]}")

    if capacidades[n] <= estudiantes[n]:
        print("LLENO")
    else:
        print() 

print(profesores)

os.system("pause")

