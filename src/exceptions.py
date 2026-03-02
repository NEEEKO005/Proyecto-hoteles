"""Excepciones personalizadas para el sistema de administración de hotel."""


class HotelError(Exception):
    """Excepción base del sistema de hotel."""


class HabitacionNoEncontradaError(HotelError):
    """Se lanza cuando no se encuentra una habitación con el ID dado."""

    def __init__(self, habitacion_id: int) -> None:
        super().__init__(f"No se encontró la habitación con ID {habitacion_id}.")
        self.habitacion_id = habitacion_id


class ReservaNoEncontradaError(HotelError):
    """Se lanza cuando no se encuentra una reserva con el ID dado."""

    def __init__(self, reserva_id: int) -> None:
        super().__init__(f"No se encontró la reserva con ID {reserva_id}.")
        self.reserva_id = reserva_id


class HabitacionNoDisponibleError(HotelError):
    """Se lanza cuando se intenta reservar una habitación ocupada."""

    def __init__(self, numero: str) -> None:
        super().__init__(f"La habitación {numero} no está disponible actualmente.")
        self.numero = numero


class FechaInvalidaError(HotelError):
    """Se lanza cuando el rango de fechas es inválido."""

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)


class DatosInvalidosError(HotelError):
    """Se lanza cuando los datos de entrada no cumplen el formato esperado."""

    def __init__(self, campo: str, detalle: str) -> None:
        super().__init__(f"Dato inválido en '{campo}': {detalle}")
        self.campo = campo