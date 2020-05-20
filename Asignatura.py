from mechanize import Browser
import bs4 as bs
import urllib.request as ulib
from Grupo import Group
import Logger as log

class Subject:

    def __init__(self, subject_code, logging=True):

        self.code = str(subject_code)

        print()
        log.course_log(f"Detectando asignatura de codigo : {self.code}")

        self.html_lines = self.get_subjectHTML()

        log.info_log("Asignatura detectada!")

        self.name = str(self.html_lines[45]).strip()

        log.info_log(f"Nombre de la asignatura [{self.code}] : {self.name}")

        self.groups = {}

    def get_subjectHTML(self):

        br = Browser()
        br.open("https://www.uis.edu.co/estudiantes/asignaturas_programadas/buscador.html")
        br.select_form(name = "form1") # pylint: disable=no-member
        br.form['codigo'] = self.code # pylint: disable=no-member
        br.submit() # pylint: disable=no-member

        soup = bs.BeautifulSoup(br.response().read(), "html.parser") # pylint: disable=no-member
        soup = soup.prettify()
        html = soup.split("\n")

        #Se descubrio que si existe un parametro invalido, la respuesta del
        #servidor sera menor a 60 lineas de HTML
        if len(html) < 60: 
            log.error_log("Asignatura no detectada")
            raise InvalidSubjectCode()
            
        return html

    def import_all_groups(self, logging=True):

        if logging:
            log.course_log(f"Obteniendo grupos de {self.name} . . .")

        index = 0

        for line in self.html_lines:

            line = str(line).strip()

            if "Grupo" in line:
                group_code = line[7:]

                if logging:
                    log.info_log(f"Grupo de {self.name} detectado: {group_code}")
                    log.course_log(f"[{group_code}] Detectando información . . .")
                
                group_capacity = int(str(self.html_lines[index + 13]).strip())
                group_students = int(str(self.html_lines[index + 20]).strip())

                if logging:
                    log.info_log(f"[{group_code}] Capacidad : {group_capacity} -- Matriculados: {group_students}")

                group = Group(self, group_code, group_capacity, group_students, logging=logging)

                if logging:
                    print() #Deja un espacio para facilitar el logging entre grupos

                self.groups[group_code] = group

            index += 1
        
        return True
        
    
    def import_group(self, group_code, logging=False):

        if logging:
            log.course_log(f"Obteniendo grupo {group_code} de {self.name} . . .")

        index = 0
        groups = []

        for line in self.html_lines:

            line = str(line).strip()

            if "Grupo" in line:
                current_group_code = line[7:]

                if logging:
                    log.info_log(f"Grupo de {self.name} detectado: {group_code}")
                    log.course_log(f"[{group_code}] Detectando información . . .")
                
                group_capacity = int(str(self.html_lines[index + 13]).strip())
                group_students = int(str(self.html_lines[index + 20]).strip())

                if logging:
                    log.info_log(f"[{group_code}] Capacidad : {group_capacity} -- Matriculados: {group_students}")
                
                if current_group_code == group_code:
                    group = Group(self,  group_code, group_capacity, group_students, logging=logging)
                    self.groups[group_code] = group
                    return True
            
            index += 1
        
        return False
    
    def get_group_by_code(self, group_code):

        if group_code in self.groups:
            return self.groups[group_code]
        
        log.error_log(f'Grupo {group_code} no encontrado')
        return None

class InvalidSubjectCode(Exception):
    pass