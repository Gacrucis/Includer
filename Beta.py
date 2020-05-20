from Asignatura import *
from Horario import *
import Logger as log

# codigos = [22956,22957,22958,22959]
codigos = [20255,22957,22958,22959]
# codigos = [22958]

horario = Schedule()

equations = Subject(20255)
horario.add_group(equations.import_group('A4'))
equations.import_all_groups(logging=False)

physics = Subject(22956)
horario.add_group(physics.import_group('A4A'))

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

alt = horario.get_alternative_groups(equations, allow_full=True)
alt_codes = [group.code for group in alt]

print(alt_codes)

# teachers = horario.get_teachers()

# for subject_code in teachers:
#     print(f'{horario.subjects[subject_code].name} -> {teachers[subject_code]}')