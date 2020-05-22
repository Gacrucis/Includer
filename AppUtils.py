import sys
import time
import threading

class Logger:
# Esta carpeta almacena los parametros de logging en consola para propositos
# de debug, de la misma manera permite un facil apagado de este logging si se
# reemplazan las funciones con la keyword pass

    tags = ["[INFO]","[IN PROGRESS]","[ERROR]"]

    #Encuentra el tag mas largo y cuenta su largo para alinear el logging
    longest_tag_lenght = len(max(tags, key=len))
    # Alinea las tags para que el logging se vea organizado y legible

    for i, tag in enumerate(tags):
        tags[i] = tag.rjust(longest_tag_lenght)    
    
    infoTag = tags[0]
    courseTag = tags[1]
    errorTag = tags[2]

    @staticmethod
    def info_log(string):
        print(f"{Logger.infoTag} {string}")

    @staticmethod
    def course_log(string):
        print(f"{Logger.courseTag} {string} . . .")

    @staticmethod
    def error_log(string):
        print(f"{Logger.errorTag} {string}")
    
    @staticmethod
    def custom_log(tag, string):
        tag = tag.rjust(Logger.longest_tag_lenght)
        print(f"{tag} {string}")

    @staticmethod
    def animated_course_log(string, callback, *args, **kwargs):

        print(f"{Logger.courseTag} {string} . . . ", end=' ')
        spinner = SpinnerThread()
        spinner.start()
        
        callback(*args, **kwargs)

        spinner.stop()

        print()


class SpinnerThread(threading.Thread):

    def __init__(self):
        super().__init__(target=self._spin)
        self._stopevent = threading.Event()

    def stop(self):
        self._stopevent.set()

        sys.stdout.write('\b')
        sys.stdout.write('Hecho!')

    def _spin(self):

        i = 0
        spinner = '|/-\\'

        while not self._stopevent.isSet():
            t = spinner[i]
            sys.stdout.write(t)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')
            i += 1
            if i > 3:
                i=  0