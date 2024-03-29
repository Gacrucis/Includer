import asyncio
import urllib.request as ulib
from mechanize import Browser
import bs4 as bs
from AppUtils import *
# from CustomExceptions import Exception


class Subject:
    def __init__(self, subject_code, import_groups=True, logging=1):

        self.code = str(subject_code)

        print()
        Logger.log_course(f"Detectando asignatura de codigo : {self.code}")

        self.html_lines = self.get_subjectHTML()

        Logger.log_info("Asignatura detectada!")

        self.name = str(self.html_lines[45]).strip()

        Logger.log_info(f"Nombre de la asignatura [{self.code}] : {self.name}")

        self.groups = {}

        if import_groups:
            self.import_groups()

    def get_subjectHTML(self):

        br = Browser()
        br.set_handle_robots(False)
        br.open(
            "https://www.uis.edu.co/estudiantes/asignaturas_programadas/buscador.html"
        )
        br.select_form(name="form1")  # pylint: disable=no-member
        
        br.form["codigo"] = self.code  # pylint: disable=no-member
        br.submit()  # pylint: disable=no-member

        soup = bs.BeautifulSoup(
            br.response().read(), "html.parser"
        )  # pylint: disable=no-member
        soup = soup.prettify()
        html = soup.split("\n")

        # Se descubrio que si existe un parametro invalido, la respuesta del
        # servidor sera menor a 60 lineas de HTML
        if len(html) < 60:
            Logger.log_error(f"Asignatura {self.code} no detectada")
            raise Exception()

        return html

    def import_groups(self, logging=1):

        if logging:
            Logger.log_course(f"Obteniendo grupos de {self.name} . . .")

        tasks = []
        loop = asyncio.get_event_loop()

        for index, line in enumerate(self.html_lines):

            if "Grupo" in line:
                line = line.strip()
                group_code = line[7:]

                if logging > 1:
                    Logger.log_info(f"Grupo de {self.name} detectado: {group_code}")

                group_capacity = int(str(self.html_lines[index + 13]).strip())
                group_students = int(str(self.html_lines[index + 20]).strip())

                group_creator = loop.run_in_executor(
                    None, Group, self, group_code, group_capacity, group_students, False
                )
                tasks.append(group_creator)

                index += 20
            index += 1

        if logging:
            imported_groups = Logger.log_animated_course(
                f"Importando informacion de {len(tasks)} grupos",
                loop.run_until_complete,
                asyncio.gather(*tasks),
            )

        else:
            imported_groups = loop.run_until_complete(asyncio.gather(*tasks))

        group_dict = {group.code: group for group in imported_groups}
        self.groups.update(group_dict)

        return group_dict

    def import_group(self, group_code, duplicate=False, logging=0):

        if logging:
            Logger.log_course(f"Obteniendo grupo {group_code} de {self.name} . . .")

        if not duplicate and self.groups[group_code]:
            if logging:
                Logger.log_info(f"Grupo de {self.name} duplicado: {group_code}")
            return self.groups[group_code]

        index = 0
        groups = []

        for line in self.html_lines:

            line = str(line).strip()

            if "Grupo" in line:
                current_group_code = line[7:]

                if logging:
                    Logger.log_info(f"Grupo de {self.name} detectado: {group_code}")
                    Logger.log_course(f"[{group_code}] Detectando información . . .")

                group_capacity = int(str(self.html_lines[index + 13]).strip())
                group_students = int(str(self.html_lines[index + 20]).strip())

                if logging:
                    Logger.log_info(
                        f"[{group_code}] Capacidad : {group_capacity} -- Matriculados: {group_students}"
                    )

                if current_group_code == group_code:
                    group = Group(
                        self,
                        group_code,
                        group_capacity,
                        group_students,
                        logging=logging,
                    )
                    self.groups[group_code] = group
                    return group

            index += 1

        return None

    def get_group_by_code(self, group_code):

        if group_code in self.groups:
            return self.groups[group_code]

        Logger.log_error(f"Grupo {group_code} no encontrado")
        return None


class Group:
    def __init__(
        self, subject, group_code, capacity: int, student_quantity: int, logging=1
    ):

        self.subject = subject
        self.code = group_code
        self.capacity = capacity
        self.student_quantity = student_quantity

        if student_quantity >= capacity:
            self.is_full = True
            if logging:
                Logger.log_info(f"[{self.code}] Grupo lleno!")
        else:
            self.is_full = False

        self.html = self._get_html()
        self.teachers = self._get_teachers(logging)
        self.rooms = self._get_rooms()

        try:
            self.capacity_index = round(capacity / student_quantity, 2)
        except:
            self.capacity_index = 99

        self.raw_schedule = self._get_schedule()
        self.schedule = self._parse_raw_schedule()

        if logging:
            Logger.log_info(f"[{self.code}] Horario: {self.schedule}")

    def _get_html(self):

        # El link debajo es la base para obtener la informacion del grupo.
        # Para ello se usa web scraping en el link designado para el grupo
        # obtenido con el codigo de asignatura y codigo de grupo
        custom_link = f"https://www.uis.edu.co/estudiantes/asignaturas_programadas/horario_asignatura.jsp?codigo={self.subject.code}&grupo={self.code}&nombre=Gamma"

        group_info = ulib.urlopen(custom_link).read()
        group_soup = bs.BeautifulSoup(group_info, "html.parser")

        prettified_soup = group_soup.prettify().split("\n")
        return prettified_soup

    def _get_teachers(self, logging=1):

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

            line_index += 1

        # Elimina los profesores duplicados
        teachers = list(dict.fromkeys(teachers))

        if logging:
            Logger.log_info(f"[{self.code}] Profesores: {teachers}")

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

    def _get_rooms(self):

        rooms = []

        line_index = 0

        for line in self.html:

            if "edificio" in line.lower():
                room = self.html[line_index + 3]

                # En caso de que no haya un profesor designado, aparecera el string
                # </td> en la variable room, se verifica que no este este string con
                # el if de abajo, en caso de no estar significa que existe un profesor
                # valido en la variable room

                if "<" not in room:
                    rooms.append(" ".join(room.strip().split()))

            line_index += 1

        # Elimina los salones duplicados
        rooms = list(dict.fromkeys(rooms))

        # if logging:
        #     Logger.log_info(f"[{self.code}] Profesores: {rooms}")

        return rooms

    def _parse_raw_schedule(self):

        schedule = {}

        for day in self.raw_schedule:

            schedule[day] = []

            for lesson in self.raw_schedule[day]:
                lesson_hours = lesson
                lesson_hour_data = [
                    int(hour.strip()) for hour in lesson_hours.split("-")
                ]
                lesson_start_hour = lesson_hour_data[0]
                lesson_finish_hour = lesson_hour_data[1]

                schedule[day].extend(list(range(lesson_start_hour, lesson_finish_hour)))

        return schedule

    # Este es el formato que se usa en el archivo de texto creado para la asignatura pero
    # con colores, sin embargo parece no funcionar bien en la consola de Windows
    def pretty_print(self):

        group_info = (
            f"Grupo: [{self.code}] // #: {self.student_quantity} !: {self.capacity}"
        )
        group_teachers = f"Profesores: {self.teachers} IB: {self.capacity_index}"
        formatted_string = f"{group_info}\n{group_teachers}"

        if self.is_full:
            formatted_string = bcolors.FAIL + formatted_string + bcolors.ENDC

        print(formatted_string)

    def get_schedule_representation(self):
        return f"{self.subject.code} {self.code}"

    # Este es el formato que se usa en el archivo de texto creado para la asignatura
    def __repr__(self):

        group_info = (
            f"Grupo: [{self.code}] // #: {self.student_quantity} !: {self.capacity}"
        )
        group_teachers = f"Profesores: {self.teachers} IB: {self.capacity_index}"
        group_schedule = f"Horario: {self.raw_schedule}"
        formatted_string = f"{group_info}\n{group_teachers}\n{group_schedule}\n"

        if self.is_full:
            formatted_string = (
                formatted_string + "||||||||||||||||||||||||||||||||||||||||"
            )

        return formatted_string


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
