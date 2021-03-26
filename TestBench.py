from AcademicObjects import Subject, Group
from IncludingObjects import Schedule
from AppUtils import Logger


horario = Schedule()

stats = Subject(21857)
horario.add_group(stats.import_group("J1"))

web_1 = Subject(22965)
horario.add_group(web_1.import_group("J1"))

architecture = Subject(22966)
horario.add_group(architecture.import_group("A2"))

web_programming = Subject(22967)
horario.add_group(web_programming.import_group("H1"))

info_systems = Subject(22968)
horario.add_group(info_systems.import_group("H1"))

english = Subject(23057)
# horario.add_group(english.import_group("A02"))

horario.pretty_print()

alt_groups = horario.get_compatible_groups(english, allow_full=True)


for group in alt_groups:
    group.pretty_print()
    print(group.schedule)
