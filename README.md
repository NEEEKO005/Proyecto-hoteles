# 🏨 Hotel Manager

Administración de habitaciones y reservas de hotel desde la línea de comandos.


## Comandos

```bash
# Habitaciones
uv run python main.py listar-habitaciones [--disponibles]
uv run python main.py agregar-habitacion 305 doble 140.0
uv run python main.py actualizar-habitacion 1 --precio 95.0
uv run python main.py eliminar-habitacion 3

# Reservas
uv run python main.py listar-reservas [--estado activa]
uv run python main.py crear-reserva 2 "María García" "maria@email.com" 2025-04-01 2025-04-05
uv run python main.py cancelar-reserva 1

# Ingresos
uv run python main.py ingresos
```

## Pruebas

```bash
uv run pytest -v
```
