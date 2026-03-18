# Primeros Pasos

## Instalación

=== "macOS / Linux"

    ```bash
    git clone https://github.com/tu-usuario/hotel-manager.git
    cd hotel-manager
    uv sync --extra dev
    ```

=== "Windows"

    ```bash
    git clone https://github.com/tu-usuario/hotel-manager.git
    cd hotel-manager
    uv sync --extra dev
    ```

!!! info "Requisito"
    Se necesita **Python 3.11+** y **uv** instalado. Si no tienes `uv`:
    ```bash
    pip install uv
    ```

---

## Sincronización de dependencias

`uv sync` instala todo lo declarado en `pyproject.toml`, incluyendo `typer`, `rich` y las dependencias de desarrollo (`pytest`, `ruff`, `radon`, `mkdocs`).

---

## Primer comando

Verifica que todo funciona listando las habitaciones precargadas:

```bash
uv run python main.py listar-habitaciones
```

Deberías ver una tabla como esta:

```
╭────┬────────┬────────┬──────────────┬────────────╮
│ ID │ Número │  Tipo  │ Precio/Noche │ Disponible │
├────┼────────┼────────┼──────────────┼────────────┤
│ 1  │  101   │ simple │    $80.00    │   ✅ Sí    │
│ 2  │  102   │ doble  │   $120.00    │   ✅ Sí    │
│ 3  │  201   │ suite  │   $250.00    │   ❌ No    │
╰────┴────────┴────────┴──────────────┴────────────╯
```

---

## Ver todos los comandos disponibles

```bash
uv run python main.py --help
```
