SELECT DISTINCT p.nombre AS Profesor,
    a.nombre AS Asignatura
FROM persona AS p,
    profesor AS prof,
    grupo AS g,
    asignatura AS a
WHERE p.persona_id = prof.persona_fk
    AND g.profesor_fk = prof.profesor_id
    AND g.codigo_asignatura = a.codigo