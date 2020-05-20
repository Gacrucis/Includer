from Asignatura import *
import Logger as log

class Horario:

    def __init__(self):
        
        self.days = {}
        self.days['LUNES'] = {hour : None for hour in range(0,24)}
        self.days['MARTES'] = {hour : None for hour in range(0,24)}
        self.days['MIERCOLES'] = {hour : None for hour in range(0,24)}
        self.days['JUEVES'] = {hour : None for hour in range(0,24)}
        self.days['VIERNES'] = {hour : None for hour in range(0,24)}
        self.days['SABADO'] = {hour : None for hour in range(0,24)}

        self.start_hour = 6
        self.finish_hour = 22

        self.teachers = {}
        self.subjects = {}
        self.groups = {}
    
    def add_group(self, group):

        log.course_log(f'Agregando grupo {group.code} de {group.subject.name}')

        temp_days = self.days.copy()
        
        for day in group.schedule:

            for hour in group.schedule[day]:

                if not self.check_schedule(day, hour):
                    log.error_log('Grupo no compatible')
                    return False

                temp_days[day][hour] = group                
        
        self.days = temp_days
        self.teachers[group.subject.code] = []
        self.subjects[group.subject.code] = group.subject.name
        self.groups[group.subject.code] = group.code
        
        for teacher in group.teachers:
            if teacher != 'Sin profesor':
                self.teachers[group.subject.code].append(teacher)   

        return True
    
    def check_schedule(self, day, hour):

        day = day.upper()

        if self.days[day][hour]:
            return False
        
        return True

    def get_compatible_groups(self, subject):
        
        if str(subject).isdigit():
            subject = Subject(subject, logging=False)

        log.course_log(f'Detectando horarios compatibles de {subject.name}')
        compatible_groups = []

        for group in subject.groups.values():

            is_compatible = True
            
            for day in group.schedule:

                for hour in group.schedule[day]:

                    if not self.check_schedule(day, hour):
                        is_compatible = False
                        break
            
            if is_compatible:
                compatible_groups.append(group.code)
        
        return compatible_groups

    def pretty_print(self):

        print()
        justify_length = 13

        # Lineas separadoras verticales
        print('-'*3, end='')

        for day in self.days:
            print('-'*justify_length , end='')
        print()

        # Dias de la semana
        print('H'.ljust(3), end='')

        for day in self.days:
            print('|' + f'{day}'.center(justify_length-2) + '|' , end='')
        print()

        # Lineas separadoras verticales
        print('-'*3, end='')

        for day in self.days:
            print('-'*justify_length , end='')
        print()

        # Horario
        for hour in range(self.start_hour, self.finish_hour):

            print(f'{hour}'.ljust(3), end='')
            for day in self.days:

                hour_content = self.days[day][hour]
                if  hour_content is not None:
                    hour_info = hour_content.get_schedule_representation()
                else:
                    hour_info = ''

                print('|' + f'{hour_info}'.center(justify_length-2) + '|', end='')   
            print()
        
        # Lineas separadoras verticales
        print('-'*3, end='')

        for day in self.days:
            print('-'*justify_length , end='')
        print()

        
        print()