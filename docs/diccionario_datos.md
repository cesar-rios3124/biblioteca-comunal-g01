# Diccionario de datos — G01 Biblioteca comunal «Letras del Sur»

**Asignatura:** Back End  
**Sección:** P13-C1 (código visible en la captura entregada)  
**Grupo:** G01  
**Versión:** Borrador consolidado de Semana 1

> El enunciado G01 define las entidades y sus atributos mínimos, pero no fija todas las longitudes, tipos detallados ni nulabilidades. Los tamaños y algunas decisiones de obligatoriedad que aparecen aquí son propuestas técnicas revisadas durante el diseño; no deben confundirse con valores textuales del enunciado.

## 1. SOCIOS

Almacena los datos de las personas que pueden solicitar préstamos en la biblioteca.

| Columna | Tipo Oracle | ¿Acepta nulos? | Restricción | Descripción |
|---|---|---:|---|---|
| `id_socio` | `NUMBER(11)` | No | PK; IDENTITY | Identificador numérico del socio, generado por Oracle. |
| `rut` | `VARCHAR2(12)` | No | UNIQUE | RUT único del socio. |
| `nombre` | `VARCHAR2(100)` | No | — | Nombre del socio. |
| `email` | `VARCHAR2(100)` | Sí | — | Correo electrónico del socio. |
| `telefono` | `VARCHAR2(20)` | Sí | — | Teléfono de contacto. |
| `activo` | `NUMBER(1)` | No | DEFAULT 1; CHECK (`activo` IN (0,1)) | Indica si el socio está habilitado (1) o inactivo (0). |

**Restricciones propuestas:** `pk_socios`, `uq_socios_rut`, `ck_socios_activo`.

## 2. GENEROS

Clasifica los libros por género literario.

| Columna | Tipo Oracle | ¿Acepta nulos? | Restricción | Descripción |
|---|---|---:|---|---|
| `id_genero` | `NUMBER(11)` | No | PK; IDENTITY | Identificador numérico del género, generado por Oracle. |
| `nombre` | `VARCHAR2(50)` | No | UNIQUE | Nombre del género literario; no se permiten nombres repetidos. |

**Restricciones propuestas:** `pk_generos`, `uq_generos_nombre`.

## 3. LIBROS

Registra los títulos, sus datos bibliográficos, el género al que pertenecen y sus ejemplares disponibles.

| Columna | Tipo Oracle | ¿Acepta nulos? | Restricción | Descripción |
|---|---|---:|---|---|
| `id_libro` | `NUMBER(11)` | No | PK; IDENTITY | Identificador numérico del libro, generado por Oracle. |
| `isbn` | `VARCHAR2(20)` | No | UNIQUE | ISBN único del libro. |
| `titulo` | `VARCHAR2(150)` | No | — | Título del libro. |
| `autor` | `VARCHAR2(100)` | No | — | Autor del libro. |
| `anio` | `NUMBER(4)` | No | — | Año de publicación. |
| `id_genero` | `NUMBER(11)` | No | FK → `GENEROS.id_genero` | Género al que pertenece el libro. |
| `ejemplares_disponibles` | `NUMBER(11)` | No | DEFAULT 0; CHECK (`ejemplares_disponibles` >= 0) | Cantidad de ejemplares que están disponibles para préstamo. |

**Restricciones propuestas:** `pk_libros`, `uq_libros_isbn`, `fk_libros_genero`, `ck_libros_ejemplares`.

## 4. PRESTAMOS

Registra cada operación de préstamo realizada por un socio.

| Columna | Tipo Oracle | ¿Acepta nulos? | Restricción | Descripción |
|---|---|---:|---|---|
| `id_prestamo` | `NUMBER(11)` | No | PK; IDENTITY | Identificador numérico del préstamo, generado por Oracle. |
| `id_socio` | `NUMBER(11)` | No | FK → `SOCIOS.id_socio` | Socio que realiza el préstamo. |
| `fecha_prestamo` | `TIMESTAMP` | No | DEFAULT UTC | Fecha y hora del préstamo, con valor por defecto en UTC. |
| `fecha_devolucion_esperada` | `TIMESTAMP` | No | — | Fecha y hora esperada para devolver los libros. La regla G01 establece un plazo de 14 días. |
| `estado` | `VARCHAR2(10)` | No | DEFAULT 'activo'; CHECK (`estado` IN ('activo','atrasado','devuelto')) | Estado actual del préstamo. |

**Restricciones propuestas:** `pk_prestamos`, `fk_prestamos_socio`, `ck_prestamos_estado`.

## 5. DETALLE_PRESTAMO

Relaciona cada préstamo con los libros que incluye y la cantidad de ejemplares solicitados de cada uno.

| Columna | Tipo Oracle | ¿Acepta nulos? | Restricción | Descripción |
|---|---|---:|---|---|
| `id_prestamo` | `NUMBER(11)` | No | PK compuesta; FK → `PRESTAMOS.id_prestamo` | Préstamo al que pertenece esta línea de detalle. |
| `id_libro` | `NUMBER(11)` | No | PK compuesta; FK → `LIBROS.id_libro` | Libro incluido en el préstamo. |
| `cantidad` | `NUMBER(11)` | No | CHECK (`cantidad` > 0) | Número de ejemplares de ese libro incluidos en el préstamo. |

**Clave primaria compuesta:** (`id_prestamo`, `id_libro`).  
**Restricciones propuestas:** `pk_detalle_prestamo`, `fk_detalle_prestamo`, `fk_detalle_libro`, `ck_detalle_cantidad`.

## 6. Resumen de relaciones y restricciones

| Clave foránea | Tabla/columna de origen | Referencia |
|---|---|---|
| `fk_libros_genero` | `LIBROS.id_genero` | `GENEROS.id_genero` |
| `fk_prestamos_socio` | `PRESTAMOS.id_socio` | `SOCIOS.id_socio` |
| `fk_detalle_prestamo` | `DETALLE_PRESTAMO.id_prestamo` | `PRESTAMOS.id_prestamo` |
| `fk_detalle_libro` | `DETALLE_PRESTAMO.id_libro` | `LIBROS.id_libro` |

Restricciones UNIQUE propuestas: RUT de socio, nombre de género e ISBN de libro.  
Restricciones CHECK propuestas: socio activo en 0/1, ejemplares disponibles no negativos, estado de préstamo limitado a los tres estados G01 y cantidad del detalle mayor que cero.

## 7. Notas para la implementación SQL

- Las columnas IDENTITY usarán la sintaxis Oracle del manual: `GENERATED BY DEFAULT ON NULL AS IDENTITY (NOCACHE)`.
- Las fechas se almacenarán en UTC, siguiendo el manual.
- Se crearán índices para las columnas de claves foráneas. La PK compuesta de `DETALLE_PRESTAMO` comienza por `id_prestamo`, por lo que su índice también cubre esa columna inicial; se deberá asegurar un índice para `id_libro`.
- No se agrega una columna virtual porque el problema G01 no define un atributo calculado equivalente al subtotal del ejemplo del manual.
- La fecha esperada se establecerá aplicando el plazo de 14 días en la lógica de aplicación. La forma de detectar y cambiar automáticamente el estado a `atrasado` debe definirse antes de programar esa parte.
- Sigue pendiente precisar si el límite de 3 libros se contará por ejemplares totales o por títulos diferentes, porque el enunciado no lo desglosa.
