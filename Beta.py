from Asignatura import *
from Horario import *
import Logger as log

# codigos = [22956,22957,22958,22959]
codigos = [20255,22957,22958,22959]
# codigos = [22958]

horario = Horario()

equations = Subject(20255)
equations.import_group('A4')
horario.add_group(equations.get_group_by_code('A4'))

physics = Subject(22956)
physics.import_group('A4A')
horario.add_group(physics.get_group_by_code('A4A'))

electricity = Subject(22957)
electricity.import_group('D1')
horario.add_group(electricity.get_group_by_code('D1'))

automats = Subject(22958)
automats.import_group('H2')
horario.add_group(automats.get_group_by_code('H2'))

databases = Subject(22959)
databases.import_group('B1')
horario.add_group(databases.get_group_by_code('B1'))

# dif = Subject(22956, logging=False)
# print(f'Cantidad de grupos disponibles: {len(dif.groups)}')

# compatible_groups = horario.get_compatible_groups(dif)

# print(compatible_groups)
# print(f'Cantidad de grupos compatibles: {len(compatible_groups)}')

horario.pretty_print()