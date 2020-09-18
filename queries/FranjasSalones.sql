-- Obtiene las franjas o lecciones por salones
SELECT CONCAT(ed.nombre, '-', sal.codigo),
    f.hora_inicio,
    f.hora_fin,
    dia.nombre AS diasemana
FROM franja AS f,
    edificio AS ed,
    diasemana AS dia,
    salon AS sal
WHERE sal.salon_id = f.salon_fk
    AND sal.edificio_fk = ed.edificio_id
    AND f.dia_semana_fk = dia.dia_semana_id