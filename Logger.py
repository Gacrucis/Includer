
# Esta carpeta almacena los parametros de logging en consola para propositos
# de debug, de la misma manera permite un facil apagado de este logging si se
# reemplazan las funciones con la keyword pass

tags = ["[INFO]","[EN CURSO]","[ERROR]"]

longestTagLenght = len(max(tags, key=len)) #Encuentra el tag mas largo y cuenta su largo para alinear el logging

# Alinea las tags para que el logging se vea organizado y legible

index = 0
for tag in tags:
    tags[index] = tag.rjust(longestTagLenght)
    index += 1

infoTag = tags[0]
courseTag = tags[1]
errorTag = tags[2]

def info_log(argument):
    print(f"{infoTag} {argument}")

def course_log(argument):
    print(f"{courseTag} {argument} . . .")

def error_log(argument):
    print(f"{errorTag} {argument}")