import time
import os
import asyncio
from AcademicObjects import Subject, Group
from IncludingObjects import Schedule
from AppUtils import Logger

# codigos = [22960, 22961, 22962, 22963, 23426]

horario = Schedule()

stats = Subject(21857)
horario.add_group(stats.import_group("D1"))

web_1 = Subject(22965)
horario.add_group(web_1.import_group("F1"))

architecture = Subject(22966)
horario.add_group(architecture.import_group("A2"))

web_programming = Subject(22967)
horario.add_group(web_programming.import_group("J1"))

info_systems = Subject(22968)
horario.add_group(info_systems.import_group("H1"))

english = Subject(23057)
horario.add_group(english.import_group("A02"))

horario.pretty_print()

alt_groups = horario.get_alternative_groups(english)
valid_groups = []

for group in alt_groups:

    for hours in group.schedule.values():
        print(hours)


alt_codes = [group.code for group in alt_groups]
alt_teachers = set()

for group in alt_groups:
    for teacher in group.teachers:
        alt_teachers.add(teacher)

alt_teachers = list(alt_teachers)

print(alt_codes)
print(alt_teachers)

for group in alt_groups:
    group.pretty_print()


# teachers = horario.get_teachers()

# for subject_code in teachers:
#     print(f'{horario.subjects[subject_code].name} -> {teachers[subject_code]}')
