from ast import Sub
from AcademicObjects import Subject
from IncludingObjects import Schedule
import pickle

cache_subjects = False
subject_path = 'subjects.data'

horario = Schedule()

# if not cache_subjects:
software = Subject(22973)
operacionales = Subject(22972)
simulacion = Subject(22974)
# innova = Subject(28664)
english = Subject(23058)
econ = Subject(22976)

# else:
#     try:
#         file = open(subject_path, 'rb')
#         data = pickle.load(file)
#         stats = data[0]
#         softw = data[1]
#         ai = data[2]
#         net = data[3]
#         volley = data[4]
#         english = data[5]

#     except:
#         softw = Subject(22973)
#         operacionales = Subject(22972)
#         digital = Subject(22974)
#         innova = Subject(28664)
#         file = open(subject_path, 'wb')
#         pickle.dump([stats, softw, ai, net, volley, english], file)
        
# horario.add_group(software.import_group("B1"))
horario.add_group(operacionales.import_group("D1"))
horario.add_group(simulacion.import_group("J1"))
# horario.add_group(innova.import_group("B1"))


# horario.add_group(software.import_group("D1"))
# horario.add_group(operacionales.import_group("D1"))
# horario.add_group(simulacion.import_group("H1"))
# horario.add_group(innova.import_group("B1"))


horario.pretty_print()
horario.print_subject_list()
print()

alt_groups = horario.get_compatible_groups(english, allow_full=True)
# alt_groups = horario.get_alternative_groups(english, allow_full=True)


for group in alt_groups:
    group.pretty_print()
    print(group.schedule)
