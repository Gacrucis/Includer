from AcademicObjects import Subject
from IncludingObjects import Schedule
import pickle

cache_subjects = True
subject_path = 'subjects.data'

horario = Schedule()

if not cache_subjects:
    stats = Subject(21857)
    web_1 = Subject(22965)
    architecture = Subject(22966)
    web_programming = Subject(22967)
    info_systems = Subject(22968)
    english = Subject(23057)

else:
    try:
        file = open(subject_path, 'rb')
        data = pickle.load(file)
        stats = data[0]
        web_1 = data[1]
        architecture = data[2]
        web_programming = data[3]
        info_systems = data[4]
        english = data[5]

    except:
        stats = Subject(21857)
        web_1 = Subject(22965)
        architecture = Subject(22966)
        web_programming = Subject(22967)
        info_systems = Subject(22968)
        english = Subject(23057)
        file = open(subject_path, 'wb')
        pickle.dump([stats, web_1, architecture, web_programming, info_systems, english], file)
        
horario.add_group(stats.import_group("J1"))
horario.add_group(web_1.import_group("J1"))
horario.add_group(architecture.import_group("A2"))
horario.add_group(web_programming.import_group("H1"))
horario.add_group(info_systems.import_group("H1"))

# horario.add_group(english.import_group("A02"))

horario.pretty_print()

alt_groups = horario.get_compatible_groups(english, allow_full=True)


for group in alt_groups:
    group.pretty_print()
    print(group.schedule)
