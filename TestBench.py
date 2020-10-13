import time
import os
import asyncio
from AcademicObjects import Subject, Group
from IncludingObjects import Schedule
from AppUtils import Logger

# codigos = [22956,22957,22958,22959]
codigos = [22960, 22961, 22962, 22963, 23426]
# codigos = [22958]

horario = Schedule()

databases = Subject(22960)
horario.add_group(databases.import_group('H1'))

digital = Subject(22961)
horario.add_group(digital.import_group('B1'))

numbers = Subject(22962)
horario.add_group(numbers.import_group('B1'))

systems = Subject(22963)
horario.add_group(systems.import_group('D1'))

english = Subject(23426)
horario.add_group(english.import_group('A02'))

horario.pretty_print()

alt_groups = horario.get_alternative_groups(english)
alt_codes = [group.code for group in alt_groups]
alt_teachers = set()

for group in alt_groups:
    for teacher in group.teachers:
        alt_teachers.add(teacher)

alt_teachers = list(alt_teachers)

print(alt_codes)
print(alt_teachers)


# teachers = horario.get_teachers()

# for subject_code in teachers:
#     print(f'{horario.subjects[subject_code].name} -> {teachers[subject_code]}')
