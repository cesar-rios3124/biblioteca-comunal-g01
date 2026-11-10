
-- Proyecto Final Back End INACAP 2026
-- Grupo G01: Biblioteca comunal Letras del Sur
-- Script 02: datos de ejemplo.
-- Ejecutar despues de 01_crear_tablas.sql.
-- Oracle genera automaticamente los identificadores.

-- 1. Cinco socios.
INSERT INTO socios (rut, nombre, email, telefono, activo)
VALUES ('10000001-6', 'Ana Rojas', 'ana.rojas@example.com', '+56911110001', 1);

INSERT INTO socios (rut, nombre, email, telefono, activo)
VALUES ('10000002-4', 'Diego Muñoz', 'diego.munoz@example.com', '+56911110002', 1);

INSERT INTO socios (rut, nombre, email, telefono, activo)
VALUES ('10000003-2', 'Camila Pérez', 'camila.perez@example.com', '+56911110003', 1);

INSERT INTO socios (rut, nombre, email, telefono, activo)
VALUES ('10000004-0', 'Martín Soto', 'martin.soto@example.com', '+56911110004', 1);

INSERT INTO socios (rut, nombre, email, telefono, activo)
VALUES ('10000005-9', 'Valentina Fuentes', NULL, '+56911110005', 1);


-- 2. Cinco géneros.
INSERT INTO generos (nombre) VALUES ('Novela');
INSERT INTO generos (nombre) VALUES ('Cuento');
INSERT INTO generos (nombre) VALUES ('Literatura infantil');
INSERT INTO generos (nombre) VALUES ('Poesía');
INSERT INTO generos (nombre) VALUES ('Historia');


-- 3. Cinco libros.
INSERT INTO libros (isbn, titulo, autor, anio, id_genero, ejemplares_disponibles)
SELECT '9789560000002', 'La casa de los espíritus', 'Isabel Allende', 1982, id_genero, 4
FROM generos WHERE nombre = 'Novela';

INSERT INTO libros (isbn, titulo, autor, anio, id_genero, ejemplares_disponibles)
SELECT '9789560000019', 'Subterra', 'Baldomero Lillo', 1904, id_genero, 2
FROM generos WHERE nombre = 'Cuento';

INSERT INTO libros (isbn, titulo, autor, anio, id_genero, ejemplares_disponibles)
SELECT '9789560000026', 'Papelucho', 'Marcela Paz', 1947, id_genero, 3
FROM generos WHERE nombre = 'Literatura infantil';

INSERT INTO libros (isbn, titulo, autor, anio, id_genero, ejemplares_disponibles)
SELECT '9789560000033', 'Veinte poemas de amor y una canción desesperada',
       'Pablo Neruda', 1924, id_genero, 2
FROM generos WHERE nombre = 'Poesía';

INSERT INTO libros (isbn, titulo, autor, anio, id_genero, ejemplares_disponibles)
SELECT '9789560000040', 'Breve historia de Chile', 'Sergio Villalobos', 1980, id_genero, 2
FROM generos WHERE nombre = 'Historia';


-- 4. Cinco préstamos.
-- Todas las fechas esperadas se calculan exactamente a 14 días.

-- Socio 1: activo.
INSERT INTO prestamos (id_socio, fecha_prestamo, fecha_devolucion_esperada, estado)
SELECT id_socio, f.fecha_prestamo, f.fecha_prestamo + INTERVAL '14' DAY, 'activo'
FROM socios
CROSS JOIN (SELECT SYS_EXTRACT_UTC(SYSTIMESTAMP) - INTERVAL '4' DAY fecha_prestamo FROM dual) f
WHERE rut = '10000001-6';

-- Socio 2: atrasado.
INSERT INTO prestamos (id_socio, fecha_prestamo, fecha_devolucion_esperada, estado)
SELECT id_socio, f.fecha_prestamo, f.fecha_prestamo + INTERVAL '14' DAY, 'atrasado'
FROM socios
CROSS JOIN (SELECT SYS_EXTRACT_UTC(SYSTIMESTAMP) - INTERVAL '30' DAY fecha_prestamo FROM dual) f
WHERE rut = '10000002-4';

-- Socio 3: devuelto.
INSERT INTO prestamos (id_socio, fecha_prestamo, fecha_devolucion_esperada, estado)
SELECT id_socio, f.fecha_prestamo, f.fecha_prestamo + INTERVAL '14' DAY, 'devuelto'
FROM socios
CROSS JOIN (SELECT SYS_EXTRACT_UTC(SYSTIMESTAMP) - INTERVAL '40' DAY fecha_prestamo FROM dual) f
WHERE rut = '10000003-2';

-- Socio 4: activo.
INSERT INTO prestamos (id_socio, fecha_prestamo, fecha_devolucion_esperada, estado)
SELECT id_socio, f.fecha_prestamo, f.fecha_prestamo + INTERVAL '14' DAY, 'activo'
FROM socios
CROSS JOIN (SELECT SYS_EXTRACT_UTC(SYSTIMESTAMP) - INTERVAL '2' DAY fecha_prestamo FROM dual) f
WHERE rut = '10000004-0';

-- Socio 5: devuelto.
INSERT INTO prestamos (id_socio, fecha_prestamo, fecha_devolucion_esperada, estado)
SELECT id_socio, f.fecha_prestamo, f.fecha_prestamo + INTERVAL '14' DAY, 'devuelto'
FROM socios
CROSS JOIN (SELECT SYS_EXTRACT_UTC(SYSTIMESTAMP) - INTERVAL '24' DAY fecha_prestamo FROM dual) f
WHERE rut = '10000005-9';


-- 5. Detalles de los prestamos.
-- Las relaciones se buscan utilizando el RUT y el ISBN.

INSERT INTO detalle_prestamo (id_prestamo, id_libro, cantidad)
SELECT p.id_prestamo, l.id_libro, 1
FROM prestamos p
JOIN socios s ON s.id_socio = p.id_socio
JOIN libros l ON l.isbn = '9789560000002'
WHERE s.rut = '10000001-6';

INSERT INTO detalle_prestamo (id_prestamo, id_libro, cantidad)
SELECT p.id_prestamo, l.id_libro, 1
FROM prestamos p
JOIN socios s ON s.id_socio = p.id_socio
JOIN libros l ON l.isbn = '9789560000019'
WHERE s.rut = '10000001-6';

INSERT INTO detalle_prestamo (id_prestamo, id_libro, cantidad)
SELECT p.id_prestamo, l.id_libro, 1
FROM prestamos p
JOIN socios s ON s.id_socio = p.id_socio
JOIN libros l ON l.isbn = '9789560000026'
WHERE s.rut = '10000002-4';

INSERT INTO detalle_prestamo (id_prestamo, id_libro, cantidad)
SELECT p.id_prestamo, l.id_libro, 1
FROM prestamos p
JOIN socios s ON s.id_socio = p.id_socio
JOIN libros l ON l.isbn = '9789560000033'
WHERE s.rut = '10000003-2';

INSERT INTO detalle_prestamo (id_prestamo, id_libro, cantidad)
SELECT p.id_prestamo, l.id_libro, 1
FROM prestamos p
JOIN socios s ON s.id_socio = p.id_socio
JOIN libros l ON l.isbn = '9789560000040'
WHERE s.rut = '10000004-0';

INSERT INTO detalle_prestamo (id_prestamo, id_libro, cantidad)
SELECT p.id_prestamo, l.id_libro, 1
FROM prestamos p
JOIN socios s ON s.id_socio = p.id_socio
JOIN libros l ON l.isbn = '9789560000002'
WHERE s.rut = '10000005-9';

COMMIT;


-- 6. Consultas de comprobación.
SELECT table_name
FROM user_tables
WHERE table_name IN ('SOCIOS', 'GENEROS', 'LIBROS', 'PRESTAMOS', 'DETALLE_PRESTAMO')
ORDER BY table_name;

SELECT COUNT(*) AS total_socios FROM socios;
SELECT COUNT(*) AS total_generos FROM generos;
SELECT COUNT(*) AS total_libros FROM libros;
SELECT COUNT(*) AS total_prestamos FROM prestamos;
SELECT COUNT(*) AS total_detalles FROM detalle_prestamo;
