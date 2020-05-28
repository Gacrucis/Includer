from AcademicObjects import Subject, Group
from IncludingObjects import Schedule
from AppUtils import Logger
import time
import os
import asyncio

# codigos = [22956,22957,22958,22959]
codigos = [20255,22957,22958,22959]
# codigos = [22958]

horario = Schedule()

equations = Subject(20255)

horario.add_group(equations.import_group('A4'))

physics = Subject(22956)
horario.add_group(physics.import_group('A4A'))
# physics.pretty_import_all_groups()
# physics.import_all_groups(logging=False)

electricity = Subject(22957)
horario.add_group(electricity.import_group('D1'))

automats = Subject(22958)
horario.add_group(automats.import_group('H2'))

databases = Subject(22959)
horario.add_group(databases.import_group('B1'))


# dif = Subject(22956, logging=False)
# print(f'Cantidad de grupos disponibles: {len(dif.groups)}')

# compatible_groups = horario.get_compatible_groups(dif)

# print(compatible_groups)
# print(f'Cantidad de grupos compatibles: {len(compatible_groups)}')

horario.pretty_print()

alt_physics = horario.get_alternative_groups(automats)
alt_codes = [group.code for group in alt_physics]
alt_teachers = set()

for group in alt_physics:
    for teacher in group.teachers:
        alt_teachers.add(teacher)

alt_teachers = list(alt_teachers)

print(alt_codes)
print(alt_teachers)


# teachers = horario.get_teachers()

# for subject_code in teachers:
#     print(f'{horario.subjects[subject_code].name} -> {teachers[subject_code]}')