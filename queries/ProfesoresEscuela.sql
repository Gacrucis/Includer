-- Obtiene la cantidad de profesores por escuela
SELECT esc.nombre AS Escuela,
    COUNT(*) AS cantidad_profesores
FROM profesor AS prof,
    escuela AS esc
WHERE prof.escuela_fk = esc.escuela_id
GROUP BY esc.escuela_id
ORDER BY cantidad_profesores DESC