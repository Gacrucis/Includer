-- Obtiene el promedio por estudiante
SELECT p.persona_id AS id,
    p.nombre,
    AVG(ca.nota) AS promedio
FROM persona AS p,
    estudiante AS e,
    calificacionasignatura AS ca
WHERE p.persona_id = e.estudiante_id
    AND ca.estudiante_fk = e.estudiante_id
GROUP BY id
ORDER BY promedio DESC