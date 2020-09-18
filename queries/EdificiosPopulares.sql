-- Obtiene la cantidad de franjas por edificio, indicando los edificios con mas clases
SELECT ed.nombre AS edificio,
    COUNT(*) AS cantidad
FROM franja AS f,
    edificio AS ed,
    salon AS sal
WHERE sal.salon_id = f.salon_fk
    AND sal.edificio_fk = ed.edificio_id
GROUP BY ed.edificio_id
ORDER BY cantidad DESC