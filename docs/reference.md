# Referencia API

Documentación generada automáticamente desde los docstrings del código fuente.

---

## Modelos

### Habitacion

::: hotel_manager.models.habitacion.Habitacion
    options:
      show_source: true
      members:
        - __post_init__
        - to_dict
        - from_dict

### Reserva

::: hotel_manager.models.reserva.Reserva
    options:
      show_source: true
      members:
        - __post_init__
        - to_dict
        - from_dict

---

## Servicios

::: hotel_manager.services.HotelService
    options:
      show_source: true
      members:
        - listar_habitaciones
        - obtener_habitacion
        - agregar_habitacion
        - actualizar_habitacion
        - eliminar_habitacion
        - listar_reservas
        - obtener_reserva
        - crear_reserva
        - cancelar_reserva
        - calcular_ingresos

---

## Storage

::: hotel_manager.storage.HotelStorage
    options:
      show_source: true
      members:
        - obtener_habitaciones
        - obtener_habitacion_por_id
        - guardar_habitacion
        - eliminar_habitacion
        - siguiente_id_habitacion
        - obtener_reservas
        - obtener_reserva_por_id
        - guardar_reserva
        - eliminar_reserva
        - siguiente_id_reserva

---

## Excepciones

::: hotel_manager.exceptions
    options:
      show_source: false
