import sys
import time
import datetime
import threading


class Logger:
    # Esta carpeta almacena los parametros de logging en consola para propositos
    # de debug, de la misma manera permite un facil apagado de este logging si se
    # reemplazan las funciones con la keyword pass

    tags = ["[INFO]", "[IN PROGRESS]", "[ERROR]", "[SUCCESS]", "[FAIL]"]

    # Encuentra el tag mas largo y cuenta su largo para alinear el logging
    longest_tag_lenght = len(max(tags, key=len))
    # Alinea las tags para que el logging se vea organizado y legible

    for i, tag in enumerate(tags):
        tags[i] = tag.rjust(longest_tag_lenght)

    info_tag = tags[0]
    course_tag = tags[1]
    error_tag = tags[2]
    success_tag = tags[3]
    fail_tag = tags[4]

    write_file = open("logger.txt", "a")

    @staticmethod
    def log_info(string):
        log_str = f"[{datetime.datetime.now()}] {Logger.info_tag} {string}"
        print(log_str)

        if Logger.write_file is not None:
            Logger.write_file.write(log_str + "\n")
            Logger.write_file.flush()

    @staticmethod
    def log_course(string):
        log_str = f"[{datetime.datetime.now()}] {Logger.course_tag} {string}"
        print(log_str)

        if Logger.write_file is not None:
            Logger.write_file.write(log_str + "\n")

    @staticmethod
    def log_error(string):
        log_str = f"[{datetime.datetime.now()}] {Logger.error_tag} {string}"
        print(log_str)

        if Logger.write_file is not None:
            Logger.write_file.write(log_str + "\n")

    @staticmethod
    def log_success(string):
        log_str = f"[{datetime.datetime.now()}] {Logger.success_tag} {string}"
        print(log_str)

        if Logger.write_file is not None:
            Logger.write_file.write(log_str + "\n")

    @staticmethod
    def log_fail(string):
        log_str = f"[{datetime.datetime.now()}] {Logger.fail_tag} {string}"
        print(log_str)

        if Logger.write_file is not None:
            Logger.write_file.write(log_str + "\n")

    @staticmethod
    def log_custom(tag, string):
        tag = tag.rjust(Logger.longest_tag_lenght)

        log_str = f"[{datetime.datetime.now()}] {tag} {string}"
        print(log_str)

        if Logger.write_file is not None:
            Logger.write_file.write(log_str + "\n")

    @staticmethod
    def log_animated_course(string, callback, *args, **kwargs):

        exception = None
        return_value = None

        log_str = f"[{datetime.datetime.now()}] {Logger.course_tag} {string} . . . "

        print(log_str, end=" ")
        spinner = SpinnerThread()
        spinner.start()

        try:
            error_state = 0
            return_value = callback(*args, **kwargs)
        except Exception as e:
            exception = e
            error_state = 1

        spinner.stop(error_state=error_state)

        if Logger.write_file is not None:
            Logger.write_file.write(log_str + "\n")
            Logger.write_file.flush()

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

        sys.stdout.write("\b")

        if not error_state:
            sys.stdout.write("Hecho!")
        else:
            sys.stdout.write("Error!")

    def _spin(self):

        i = 0
        spinner = "|/-\\"

        while not self._stopevent.isSet():
            t = spinner[i]
            sys.stdout.write(t)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b")
            i += 1
            if i > 3:
                i = 0


# def convert_to_xlsx(name, timeout=10):

#     total_time = 0

#     while not os.path.exists(f"{name}.xls") and total_time <= timeout:
#         time.sleep(0.1)
#         total_time += 0.1

#     if total_time <= timeout:
#         pyexcel.save_book_as(
#             file_name=f"{name}.xls", dest_file_name=f"{name}.xlsx")
#         return True
#     else:
#         return False


# def write_to_txt(file_name, element_list, write_mode="w"):

#     with open(file_name, write_mode) as f:

#         for element in element_list:
#             f.write(element + "\n")


# def read_from_txt(file_name):

#     with open(file_name, "r") as f:
#         student_codes = f.read().splitlines()

#     student_codes = [code for code in student_codes if code is not None]

#     return student_codes


# def format_excel_worksheet(worksheet, names, row=1):

#     for i, name in enumerate(names):

#         current_cell = worksheet.cell(row, i+1)

#         current_cell.value = name

#         worksheet.column_dimensions[openpyxl.utils.get_column_letter(
#             current_cell.column)].width = 30
#         current_cell.alignment = openpyxl.styles.Alignment(horizontal="center")
#         current_cell.font = openpyxl.styles.Font(name="consolas", bold=True)

#     return worksheet
