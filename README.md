# MotoTaller Pro - Sistema de Gestión de Taller y Repuestos

**Integrantes:** Sammyr Valderrama y David Córdoba  
**Asignatura:** Programación II

Aplicación de escritorio desarrollada en **Python** con **Flet** y **SQLite**, estructurada bajo una arquitectura multicapa (**Domain**, **Data**, **UI**) aplicando Programación Orientada a Objetos y patrones de diseño.

## Estructura del Proyecto

```text
mi_proyecto_final/
├── main.py
├── README.md
├── informe_final.pdf
├── data/
│   ├── database_manager.py
│   ├── cliente_dao.py
│   └── producto_repository.py
├── domain/
│   ├── cliente.py
│   ├── producto.py
│   └── orden_servicio.py
└── ui/
    ├── app_view.py
    └── components/
        └── tabla_generica.py
```

## Requisitos e Instalación

1. Instalar Flet:
   ```bash
   pip install flet
   ```
2. Ejecutar la aplicación:
   ```bash
   python main.py
   ```
