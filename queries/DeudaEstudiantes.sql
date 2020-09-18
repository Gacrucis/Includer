-- Obtiene la deuda total por estudiante
SELECT p.nombre AS estudiante,
    SUM(d.cantidad) AS deuda
FROM persona AS p,
    estudiante AS e,
    deuda AS d
WHERE p.persona_id = e.persona_fk
    AND d.estudiante_fk = e.estudiante_id
GROUP BY p.nombre
ORDER BY deuda DESC