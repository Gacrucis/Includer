SELECT car.nombre AS carrera,
    AVG(calif.nota) AS Promedio
FROM estudiante AS est,
    calificacionasignatura AS calif,
    administradorcarrera AS ac,
    carrera AS car
WHERE