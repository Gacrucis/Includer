import os
import sys
import time
import threading
import configparser as cp
import traceback


class Logger:
    # Esta carpeta almacena los parametros de logging en consola para propositos
    # de debug, de la misma manera permite un facil apagado de este logging si se
    # reemplazan las funciones con la keyword pass

    tags = ["[INFO]", "[IN PROGRESS]", "[ERROR]"]

    # Encuentra el tag mas largo y cuenta su largo para alinear el logging
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

        try:
            error_state = 0
            return_value = callback(*args, **kwargs)
        except Exception as e:
            exception = e
            error_state = 1

        spinner.stop(error_state=error_state)

        if error_state:
            print()
            raise exception.with_traceback(exception.__traceback__)

        print()

        return return_value


class SpinnerThread(threading.Thread):

    def __init__(self):
        super().__init__(target=self._spin)
        self._stopevent = threading.Event()

    def stop(self, error_state=0):
        self._stopevent.set()

        sys.stdout.write('\b')

        if not error_state:
            sys.stdout.write('Hecho!')
        else:
            sys.stdout.write('Error!')

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
                i = 0


class AppConfig(cp.ConfigParser):

    default_path = 'config.ini'

    default_db_folder = 'databases'
    default_logging_mode = '1'
    default_caching_mode = '1'

    def __init__(self, path=default_path):
        super().__init__()

        if os.path.exists(path):
            self.read(path)
        else:
            self.set_defaults()
            with open(path, 'w') as f:
                self.write(f)

    def set_defaults(self):

        self['PATHS'] = {}
        self['PATHS']['database_folder'] = AppConfig.default_db_folder

        self['PREFERENCES'] = {}
        self['PREFERENCES']['logging_mode'] = AppConfig.default_logging_mode
        self['PREFERENCES']['caching_mode'] = AppConfig.default_caching_mode


def check_table_exists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False
