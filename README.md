
# Biblioteca comunal "Letras del Sur"

## Proyecto Final Back End - INACAP 2026

Sistema de gestión de préstamos de libros para una biblioteca comunal. Permite administrar socios, géneros, libros y préstamos, controlando la disponibilidad de ejemplares y las devoluciones.

## Información del grupo

- Grupo: G01
- Sección: P13-C1
- Asignatura: Back End

### Integrantes

- Ilse Gonzáles
- Abraham Silva
- Cesar Rios

## Tecnologías

- Python 3.12 o superior
- Django 5.2 LTS
- Django REST Framework
- Oracle Database 26ai (FreeSQL)
- React + Vite
- Git

## Entidades del sistema

1. Socios: registro de las personas que solicitan libros.
2. Géneros: clasificación de los libros.
3. Libros: información de títulos, autores y ejemplares disponibles.
4. Préstamos: registro de préstamos y fechas de devolución.
5. Detalle de préstamo: libros y cantidades incluidas en cada préstamo.

## Reglas de negocio

- R1: No se presta un libro sin ejemplares disponibles. Al prestar se descuentan y al devolver se reponen.
- R2: Un socio con un préstamo atrasado o inactivo no puede solicitar otro.
- R3: Máximo 3 libros por préstamo y plazo de 14 días.

## Roles

- Bibliotecario: acceso a todas las operaciones.
- Asistente: registra préstamos y devoluciones, pero no elimina ni edita libros.

## Reportes

- Los 5 libros más prestados.
- Lista de préstamos atrasados.

## Responsabilidades del grupo

- Ilse Gonzáles: socios y géneros.
- Abraham Silva: libros.
- Cesar Rios: préstamos y detalle de préstamo.

## Estructura del proyecto

```text
Biblioteca comunal/
├── backEnd/
│   ├── sql/
│   └── .env.example
├── frontend/
├── docs/
├── .gitignore
└── README.md
```

## Base de datos

Cada integrante utiliza su propio esquema Oracle FreeSQL.

Las credenciales se guardan en un archivo `.env` individual y no deben compartirse ni subirse al repositorio.

## Estado del proyecto

Proyecto en desarrollo. La documentación inicial y los scripts SQL de creación y datos de ejemplo han sido preparados para el grupo G01.
