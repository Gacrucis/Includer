from Asignatura import *
import Logger as log
import copy

class Schedule:

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

        self.subjects = {}
        self.groups = {}
    

    def add_group(self, group, logging=True):

        '''Adds a group to the schedule instance, if the group is not compatible it returns False,
         otherwise, it returns True'''

        if logging:
            log.course_log(f'Agregando grupo {group.code} de {group.subject.name}')

        temp_days = copy.deepcopy(self.days)
        
        for day in group.schedule:

            for hour in group.schedule[day]:

                if not self.check_schedule(day, hour):

                    if logging:
                        log.error_log('Grupo no compatible')
                    return False

                temp_days[day][hour] = group                
        
        self.days = temp_days
        self.subjects[group.subject.code] = group.subject
        self.groups[group.subject.code] = group

        return True
    
    def remove_group(self, group, logging=True):

        '''Removes a given Group object from the schedule instance, if the group is not valid it returns False,
         otherwise, it returns True'''

        if not group:
            if logging:
                log.error_log(f'Grupo no valido')
            return False
        
        subject_codes = {subject.code for subject in self.subjects.values()}
        group_codes = {group.code for group in self.groups.values()}

        if group.subject not in subject_codes or group.code not in group_codes:

            if logging:
                log.error_log(f'Grupo {group.code} de {group.subject.name} no encontrado')
            return False

        if logging:
            log.course_log(f'Removiendo grupo {group.code} de {group.subject.name}')
        
        for day in group.schedule:

            for hour in group.schedule[day]:

                self.days[day][hour] = None                
        
        del self.subjects[group.subject.code]
        del self.groups[group.subject.code]

        return True

    def get_teachers(self):
        
        '''Returns a dict with subject codes as keys and teacher lists as values 
        as following: {subject_code : [teacher_1, teacher_2, . . .]}'''

        teachers = {}

        for day in self.days:

            for group in self.days[day].values():

                if  group is not None:
                    teachers[group.subject.code] = group.teachers
        
        return teachers
                    
    
    def check_schedule(self, day, hour):

        '''Returns True if the given day and hour are free'''

        day = day.upper()

        if self.days[day][hour]:
            return False
        
        return True


    def get_compatible_groups(self, subject, allow_full=False):

        '''Returns a list of Group objects which are compatible with the
        current schedule instance'''
        
        if str(subject).isdigit():
            subject = Subject(subject, logging=False)

        log.course_log(f'Detectando horarios compatibles de {subject.name}')
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
    
    def get_alternative_groups(self, subject, allow_full=False):

        schedule_copy = copy.deepcopy(self)
        schedule_copy.remove_group(schedule_copy.g)


    def pretty_print(self):

        '''Prints a formatted schedule'''

        print()
        justify_length = 13

        # Lineas separadoras verticales
        print('-'*8, end='')

        for day in self.days:
            print('-'*justify_length , end='')
        print()

        # Dias de la semana
        print('HORA'.center(8), end='')

        for day in self.days:
            print('|' + f'{day}'.center(justify_length-2) + '|' , end='')
        print()

        # Lineas separadoras verticales
        print('-'*8, end='')

        for day in self.days:
            print('-'*justify_length , end='')
        print()

        # Horario
        for hour in range(self.start_hour, self.finish_hour):

            print(f'{hour} - {hour+1}'.center(8), end='')
            for day in self.days:

                hour_content = self.days[day][hour]
                if  hour_content is not None:
                    hour_info = hour_content.get_schedule_representation()
                else:
                    hour_info = ''

                print('|' + f'{hour_info}'.center(justify_length-2) + '|', end='')   
            print()
        
        # Lineas separadoras verticales
        print('-'*8, end='')

        for day in self.days:
            print('-'*justify_length , end='')
        print('\n')