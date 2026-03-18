# Comandos CLI

Todos los comandos se ejecutan con `uv run python main.py <comando>`.

---

## Habitaciones

### `listar-habitaciones`

Muestra todas las habitaciones del hotel en una tabla.

```bash
uv run python main.py listar-habitaciones
```

!!! tip "Filtrar disponibles"
    Agrega `--disponibles` para ver solo las habitaciones libres:
    ```bash
    uv run python main.py listar-habitaciones --disponibles
    ```

---

### `agregar-habitacion`

Registra una nueva habitación.

```bash
uv run python main.py agregar-habitacion <numero> <tipo> <precio>
```

| Parámetro | Descripción | Valores válidos |
|---|---|---|
| `numero` | Identificador visible | Cualquier texto, ej. `305` |
| `tipo` | Categoría | `simple`, `doble`, `suite` |
| `precio` | Tarifa por noche en USD | Número positivo |

**Ejemplo:**
```bash
uv run python main.py agregar-habitacion 305 doble 140.0
```

---

### `actualizar-habitacion`

Modifica uno o más campos de una habitación existente.

```bash
uv run python main.py actualizar-habitacion <id> [opciones]
```

**Opciones disponibles:**

| Opción | Descripción |
|---|---|
| `--numero` | Nuevo número |
| `--tipo` | Nuevo tipo |
| `--precio` | Nuevo precio por noche |
| `--disponible` | `true` o `false` |

**Ejemplos:**
```bash
# Solo actualizar precio
uv run python main.py actualizar-habitacion 1 --precio 95.0

# Cambiar tipo y disponibilidad
uv run python main.py actualizar-habitacion 2 --tipo suite --disponible true
```

---

### `eliminar-habitacion`

Elimina una habitación por ID.

```bash
uv run python main.py eliminar-habitacion <id>
```

!!! warning "Acción irreversible"
    La habitación se elimina permanentemente del archivo JSON.

---

## Reservas

### `listar-reservas`

Muestra todas las reservas registradas.

```bash
uv run python main.py listar-reservas
```

Filtra por estado con `--estado`:

=== "Activas"

    ```bash
    uv run python main.py listar-reservas --estado activa
    ```

=== "Completadas"

    ```bash
    uv run python main.py listar-reservas --estado completada
    ```

---

### `crear-reserva`

Crea una reserva para una habitación disponible.

```bash
uv run python main.py crear-reserva <habitacion_id> <nombre> <email> <entrada> <salida>
```

**Ejemplo:**
```bash
uv run python main.py crear-reserva 2 "María García" "maria@email.com" 2025-04-01 2025-04-05
```

!!! info "Validaciones automáticas"
    - La habitación debe estar disponible.
    - La fecha de salida debe ser posterior a la de entrada.
    - El email debe contener `@`.
    - El nombre no puede estar vacío.

---

### `cancelar-reserva`

Cancela una reserva activa y libera la habitación asociada.

```bash
uv run python main.py cancelar-reserva <id>
```

---

## Ingresos

### `ingresos`

Muestra el total acumulado de ingresos por reservas **completadas**.

```bash
uv run python main.py ingresos
```
