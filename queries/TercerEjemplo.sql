SELECT p.nombre,
    SUM(deuda.cantidad)
FROM personas AS p,
    estudiante AS e,
    deuda AS d
WHERE p.persona_id = e.persona_fk
    AND d.estudiante_fk = e.estudiante_id
GROUP BY p.nombre