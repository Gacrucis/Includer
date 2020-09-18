SELECT dir.departamento AS departamento,
    COUNT(*) AS cantidad_personas
FROM persona AS p,
    direccion AS dir
WHERE p.direccion_fk = dir.direccion_id
GROUP BY departamento
ORDER BY cantidad_personas DESC