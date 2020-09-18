SELECT p.nombre,
    AVG(ca.nota)
FROM persona AS p,
    estudiante AS e,
    calificacionasignatura AS ca
WHERE p.persona_id = e.estudiante_id
    AND ca.estudiante_fk = e.estudiante_id
GROUP BY p.nombre -- ORDER BY DESC