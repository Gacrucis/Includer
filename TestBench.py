from AcademicObjects import Subject
from IncludingObjects import Schedule
import pickle

cache_subjects = False
subject_path = 'subjects.data'

horario = Schedule()

if not cache_subjects:
    stats = Subject(21858)
    softw = Subject(22969)
    ai = Subject(22971)
    net = Subject(22970)
    volley = Subject(27994)
    english = Subject(23057)

else:
    try:
        file = open(subject_path, 'rb')
        data = pickle.load(file)
        stats = data[0]
        softw = data[1]
        ai = data[2]
        net = data[3]
        volley = data[4]
        english = data[5]

    except:
        stats = Subject(21858)
        softw = Subject(22969)
        ai = Subject(22971)
        net = Subject(22970)
        volley = Subject(27994)
        english = Subject(23057)
        file = open(subject_path, 'wb')
        pickle.dump([stats, softw, ai, net, volley, english], file)
        
horario.add_group(stats.import_group("K1")) #-----+
horario.add_group(softw.import_group("B1")) #-----+
horario.add_group(ai.import_group("H1")) #-----+
horario.add_group(net.import_group("B1")) #-----+
# horario.add_group(volley.import_group("A01")) 
horario.add_group(english.import_group("D01"))

horario.pretty_print()
horario.print_subject_list()
print()

# alt_groups = horario.get_compatible_groups(volley, allow_full=True)
alt_groups = horario.get_alternative_groups(english, allow_full=True)


for group in alt_groups:
    group.pretty_print()
    print(group.schedule)
