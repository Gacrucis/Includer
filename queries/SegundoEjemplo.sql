SELECT p.nombre,
    a.nombre
FROM persona AS p,
    profesor AS prof,
    grupo AS g,
    asignatura AS a
WHERE p.profesor_id = prof.persona_fk
    AND g.profesor_fk = prof.profesor_id
    AND grupo.codigo_asignatura = a.codigo