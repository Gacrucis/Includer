import copy
from AcademicObjects import Group, Subject
from AppUtils import Logger


class Schedule:
    def __init__(self):

        self.days = {}
        self.days["LUNES"] = {hour: None for hour in range(0, 24)}
        self.days["MARTES"] = {hour: None for hour in range(0, 24)}
        self.days["MIERCOLES"] = {hour: None for hour in range(0, 24)}
        self.days["JUEVES"] = {hour: None for hour in range(0, 24)}
        self.days["VIERNES"] = {hour: None for hour in range(0, 24)}
        self.days["SABADO"] = {hour: None for hour in range(0, 24)}

        self.start_hour = 6
        self.finish_hour = 22

        self.subjects = {}
        self.groups = {}

    def add_group(self, group, logging=True):
        """Adds a group to the schedule instance, if the group is not compatible it returns False,
        otherwise, it returns True"""

        if logging:
            Logger.log_course(f"Agregando grupo {group.code} de {group.subject.name}")

        temp_days = copy.deepcopy(self.days)

        for day in group.schedule:

            for hour in group.schedule[day]:

                if not self.check_schedule(day, hour):

                    if logging:
                        Logger.log_error("Grupo no compatible")
                    return False

                temp_days[day][hour] = group

        self.days = temp_days
        self.subjects[group.subject.code] = group.subject
        self.groups[group.subject.code] = group

        return True

    def remove_group(self, group, logging=True):
        """Removes a given Group object from the schedule instance, if the group is not valid it returns False,
        otherwise, it returns True"""

        if not group:
            if logging:
                Logger.log_error(f"Grupo no valido")
            return False

        subject_codes = {subject.code for subject in self.subjects.values()}
        group_codes = {group.code for group in self.groups.values()}

        if group.subject.code not in subject_codes or group.code not in group_codes:

            if logging:
                Logger.log_error(
                    f"Grupo {group.code} de {group.subject.name} no encontrado"
                )
            return False

        if logging:
            Logger.log_course(f"Removiendo grupo {group.code} de {group.subject.name}")

        for day in group.schedule:

            for hour in group.schedule[day]:

                self.days[day][hour] = None

        del self.subjects[group.subject.code]
        del self.groups[group.subject.code]

        return True

    def get_teachers(self):
        """Returns a dict with subject codes as keys and teacher lists as values
        as following: {subject_code : [teacher_1, teacher_2, . . .]}"""

        teachers = {}

        for day in self.days:

            for group in self.days[day].values():

                if group is not None:
                    teachers[group.subject.code] = group.teachers

        return teachers

    def check_schedule(self, day, hour):
        """Returns True if the given day and hour are free"""

        day = day.upper()

        if self.days[day][hour]:
            return False

        return True

    def get_compatible_groups(self, subject, allow_full=False, logging=True):
        """Returns a list of Group objects which are compatible with the
        current schedule instance"""

        if str(subject).isdigit():
            subject = Subject(subject, logging=False)

        if logging:
            Logger.log_course(f"Detectando grupos compatibles de {subject.name}")
        compatible_groups = []

        for group in subject.groups.values():

            if not allow_full and group.is_full:
                continue

            is_compatible = True

            for day in group.schedule:

                for hour in group.schedule[day]:

                    if not self.check_schedule(day, hour):
                        is_compatible = False
                        break

            if is_compatible:
                compatible_groups.append(group)

        return compatible_groups

    def get_alternative_groups(self, subject, allow_full=False, logging=True):

        schedule_copy = copy.deepcopy(self)

        current_group = schedule_copy.groups[subject.code]
        current_group_code = current_group.code

        if logging:
            Logger.log_course(
                f"Detectando grupos que pueden reemplazar al {current_group_code} de {subject.name}"
            )

        schedule_copy.remove_group(current_group, logging=False)

        compatible_groups = schedule_copy.get_compatible_groups(
            subject, allow_full=allow_full, logging=False
        )
        alternative_groups = [
            group for group in compatible_groups if group.code != current_group_code
        ]
        # alternative_groups = compatible_groups

        return alternative_groups

    def pretty_print(self):
        """Prints a formatted schedule"""

        print()
        justify_length = 13

        # Lineas separadoras verticales
        print("-" * 8, end="")

        for day in self.days:
            print("-" * justify_length, end="")
        print()

        # Dias de la semana
        print("HORA".center(8), end="")

        for day in self.days:
            print("|" + f"{day}".center(justify_length - 2) + "|", end="")
        print()

        # Lineas separadoras verticales
        print("-" * 8, end="")

        for day in self.days:
            print("-" * justify_length, end="")
        print()

        # Horario
        for hour in range(self.start_hour, self.finish_hour):

            print(f"{hour} - {hour+1}".center(8), end="")
            for day in self.days:

                hour_content = self.days[day][hour]
                if hour_content is not None:
                    hour_info = hour_content.get_schedule_representation()
                else:
                    hour_info = ""

                print("|" + f"{hour_info}".center(justify_length - 2) + "|", end="")
            print()

        # Lineas separadoras horizontales
        print("-" * 8, end="")

        for day in self.days:
            print("-" * justify_length, end="")
        print("\n")

    def print_subject_list(self):
        justify_length = 13
        hlength = (justify_length-2)*9 + 8

        gc_length = justify_length - 1
        sc_length = justify_length
        sn_length = (justify_length-2)*3
        gt_length = (justify_length-2)*4

        column_names = [
            'Grupo',
            'Codigo',
            'Nombre',
            'Profesor',
        ]

        print("-" * hlength)

        print('|' + column_names[0].center(gc_length), end='')
        print('|' + column_names[1].center(sc_length), end='')
        print('|' + column_names[2].center(sn_length), end='')
        print('|' + column_names[3].center(gt_length) + '|')

        print("-" * hlength)

        # Lista de asignaturas
        for group_code in self.groups:
            subject: Subject = self.subjects[group_code]
            group: Group = self.groups[group_code]

            gc = f"{group.code}".center(gc_length)
            sc = f"{subject.code}".center(sc_length)
            sn = f"{subject.name}".center(sn_length)
            gt = f"{group.teachers[0]}".center(gt_length)

            print("|" + gc + "|" + sc + '|' + sn + '|' + gt + '|')
        
        print("-" * hlength)

