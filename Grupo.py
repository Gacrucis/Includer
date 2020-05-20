import bs4 as bs
import urllib.request as ulib
import Logger as log
import os

class Group:

    def __init__(self, subject, group_code, capacity: int, student_quantity: int, logging=True):

        self.subject = subject
        self.code = group_code
        self.capacity = capacity
        self.student_quantity = student_quantity

        if student_quantity >= capacity:
            self.is_full = True
            if logging:
                log.info_log(f"[{self.code}] Grupo lleno!")
        else:
            self.is_full = False
        
        self.html = self._get_html()
        self.teachers = self._get_teachers(logging)

        try:
            self.capacity_index = round(capacity/student_quantity, 2) 
        except:
            self.capacity_index = 99

        self.raw_schedule = self._get_schedule()
        self.schedule = self._parse_raw_schedule()
        
        if logging:        
            log.info_log(f"[{self.code}] Horario: {self.schedule}")
    

    def _get_html(self):

        # El link debajo es la base para obtener la informacion del grupo.
        # Para ello se usa web scraping en el link designado para el grupo
        # obtenido con el codigo de asignatura y codigo de grupo
        custom_link = f'https://www.uis.edu.co/estudiantes/asignaturas_programadas/horario_asignatura.jsp?codigo={self.subject.code}&grupo={self.code}&nombre=Gamma' 

        group_info = ulib.urlopen(custom_link).read()
        group_soup = bs.BeautifulSoup(group_info, "html.parser")

        prettified_soup = group_soup.prettify().split("\n")
        return prettified_soup


    def _get_teachers(self, logging=True):

        teachers = []

        line_index = 0

        for line in self.html:

            if "profesor" in line.lower():
                teacher = self.html[line_index + 3]

                # En caso de que no haya un profesor designado, aparecera el string
                # </td> en la variable teacher, se verifica que no este este string con 
                # el if de abajo, en caso de no estar significa que existe un profesor
                # valido en la variable teacher

                if "<" not in teacher:
                    teachers.append(teacher.strip())       
                else:
                    if not teachers:
                        teachers.append("Sin profesor")

            line_index += 1

        teachers = list(dict.fromkeys(teachers)) #Elimina los profesores duplicados

        if logging:
            log.info_log(f"[{self.code}] Profesores: {teachers}")

        return teachers
    
    def _get_schedule(self):

        schedule = {}

        line_index = 0

        for line in self.html:

            if "día" in line.lower():

                day = self.html[line_index + 4].strip()
                schedule.setdefault(day, [])

                hours = self.html[line_index + 14].strip()

                schedule[day].append(hours)

            line_index += 1

        return schedule
    
    def _parse_raw_schedule(self):

        schedule = {}

        for day in self.raw_schedule:

            schedule[day] = []
            
            for lesson in self.raw_schedule[day]:
                lesson_hours = lesson
                lesson_hour_data = [int(hour.strip()) for hour in lesson_hours.split('-')]
                lesson_start_hour = lesson_hour_data[0]
                lesson_finish_hour = lesson_hour_data[1]

                schedule[day].extend(list(range(lesson_start_hour, lesson_finish_hour)))
        
        return schedule

    # Este es el formato que se usa en el archivo de texto creado para la asignatura pero
    # con colores, sin embargo parece no funcionar bien en la consola de Windows
    def pretty_print(self):
        
        group_info = F"Grupo: [{self.code}] // #: {self.student_quantity} !: {self.capacity}"
        group_teachers = F"Profesores: {self.teachers} IB: {self.capacity_index}"
        formatted_string = F"{group_info}\n{group_teachers}"

        if self.is_full:
            formatted_string = bcolors.FAIL + formatted_string + bcolors.ENDC

        print(formatted_string)
    
    def get_schedule_representation(self):
        return f'{self.subject.code} {self.code}'

    # Este es el formato que se usa en el archivo de texto creado para la asignatura
    def __repr__(self):
        
        group_info = F"Grupo: [{self.code}] // #: {self.student_quantity} !: {self.capacity}"
        group_teachers = F"Profesores: {self.teachers} IB: {self.capacity_index}"
        group_schedule = F"Horario: {self.raw_schedule}"
        formatted_string = F"{group_info}\n{group_teachers}\n{group_schedule}\n"

        if self.is_full:
            formatted_string = formatted_string + "||||||||||||||||||||||||||||||||||||||||"

        return formatted_string

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'