-- Obtiene el promedio de los estudiantes por carrera
SELECT car.nombre AS carrera,
    AVG(calif.nota) AS Promedio
FROM estudiante AS est,
    calificacionasignatura AS calif,
    administradorcarrera AS ac,
    carrera AS car
WHERE calif.estudiante_fk = est.estudiante_id
    AND ac.estudiante_fk = est.estudiante_id
    AND ac.carrera_fk = car.carrera_id
GROUP BY carrera
ORDER BY promedio DESC