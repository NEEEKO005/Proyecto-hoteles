"""Capa de servicios: contiene toda la lógica de negocio del hotel."""

from datetime import date, datetime

from hotel_manager.exceptions import (
    DatosInvalidosError,
    FechaInvalidaError,
    HabitacionNoDisponibleError,
    HabitacionNoEncontradaError,
    ReservaNoEncontradaError,
)
from hotel_manager.models import Habitacion, Reserva
from hotel_manager.storage import HotelStorage

_TIPOS_VALIDOS = {"simple", "doble", "suite"}
_ESTADOS_VALIDOS = {"activa", "completada"}


def _parsear_fecha(fecha_str: str, campo: str) -> date:
    """Convierte una cadena 'YYYY-MM-DD' a un objeto date.

    Args:
        fecha_str: Cadena de texto con la fecha.
        campo: Nombre del campo (para mensajes de error).

    Raises:
        DatosInvalidosError: Si el formato de la fecha es incorrecto.
    """
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise DatosInvalidosError(campo, "el formato debe ser YYYY-MM-DD.") from exc


class HotelService:
    """Servicio principal que coordina las operaciones del hotel.

    Centraliza las reglas de negocio y delega la persistencia al storage.

    Attributes:
        storage: Instancia de HotelStorage para acceder a los datos.
    """

    def __init__(self, storage: HotelStorage | None = None) -> None:
        """Inicializa el servicio con el storage dado.

        Args:
            storage: Instancia de HotelStorage. Si no se provee, crea una por defecto.
        """
        self.storage = storage or HotelStorage()

    # ── Habitaciones ──────────────────────────────────────────────────────────

    def listar_habitaciones(self, solo_disponibles: bool = False) -> list[Habitacion]:
        """Retorna todas las habitaciones, opcionalmente filtrando las disponibles.

        Args:
            solo_disponibles: Si es True, retorna solo habitaciones libres.
        """
        habitaciones = self.storage.obtener_habitaciones()
        if solo_disponibles:
            return [h for h in habitaciones if h.disponible]
        return habitaciones

    def obtener_habitacion(self, habitacion_id: int) -> Habitacion:
        """Busca y retorna una habitación por ID.

        Args:
            habitacion_id: ID de la habitación.

        Raises:
            HabitacionNoEncontradaError: Si no existe la habitación.
        """
        habitacion = self.storage.obtener_habitacion_por_id(habitacion_id)
        if habitacion is None:
            raise HabitacionNoEncontradaError(habitacion_id)
        return habitacion

    def agregar_habitacion(
        self, numero: str, tipo: str, precio_por_noche: float
    ) -> Habitacion:
        """Registra una nueva habitación en el hotel.

        Args:
            numero: Número identificador visible de la habitación.
            tipo: Tipo de habitación ('simple', 'doble' o 'suite').
            precio_por_noche: Precio en USD por noche.

        Raises:
            DatosInvalidosError: Si el tipo es inválido o el precio es negativo.
        """
        if tipo not in _TIPOS_VALIDOS:
            raise DatosInvalidosError(
                "tipo", f"debe ser uno de: {', '.join(_TIPOS_VALIDOS)}."
            )
        if precio_por_noche <= 0:
            raise DatosInvalidosError(
                "precio_por_noche", "debe ser un valor positivo."
            )
        nueva = Habitacion(
            id=self.storage.siguiente_id_habitacion(),
            numero=numero.strip(),
            tipo=tipo,
            precio_por_noche=precio_por_noche,
            disponible=True,
        )
        self.storage.guardar_habitacion(nueva)
        return nueva

    def actualizar_habitacion(
        self,
        habitacion_id: int,
        numero: str | None = None,
        tipo: str | None = None,
        precio_por_noche: float | None = None,
        disponible: bool | None = None,
    ) -> Habitacion:
        """Actualiza uno o más campos de una habitación existente.

        Args:
            habitacion_id: ID de la habitación a actualizar.
            numero: Nuevo número (opcional).
            tipo: Nuevo tipo (opcional).
            precio_por_noche: Nuevo precio (opcional).
            disponible: Nueva disponibilidad (opcional).

        Raises:
            HabitacionNoEncontradaError: Si no existe la habitación.
            DatosInvalidosError: Si los nuevos valores son inválidos.
        """
        habitacion = self.obtener_habitacion(habitacion_id)
        if numero is not None:
            habitacion.numero = numero.strip()
        if tipo is not None:
            if tipo not in _TIPOS_VALIDOS:
                raise DatosInvalidosError(
                    "tipo", f"debe ser uno de: {', '.join(_TIPOS_VALIDOS)}."
                )
            habitacion.tipo = tipo
        if precio_por_noche is not None:
            if precio_por_noche <= 0:
                raise DatosInvalidosError(
                    "precio_por_noche", "debe ser un valor positivo."
                )
            habitacion.precio_por_noche = precio_por_noche
        if disponible is not None:
            habitacion.disponible = disponible
        self.storage.guardar_habitacion(habitacion)
        return habitacion

    def eliminar_habitacion(self, habitacion_id: int) -> None:
        """Elimina una habitación del hotel.

        Args:
            habitacion_id: ID de la habitación a eliminar.

        Raises:
            HabitacionNoEncontradaError: Si no existe la habitación.
        """
        self.obtener_habitacion(habitacion_id)
        self.storage.eliminar_habitacion(habitacion_id)

    # ── Reservas ──────────────────────────────────────────────────────────────

    def listar_reservas(self, estado: str | None = None) -> list[Reserva]:
        """Retorna todas las reservas, opcionalmente filtradas por estado.

        Args:
            estado: 'activa' o 'completada'. Si es None, retorna todas.
        """
        reservas = self.storage.obtener_reservas()
        if estado:
            return [r for r in reservas if r.estado == estado]
        return reservas

    def obtener_reserva(self, reserva_id: int) -> Reserva:
        """Busca y retorna una reserva por ID.

        Args:
            reserva_id: ID de la reserva.

        Raises:
            ReservaNoEncontradaError: Si no existe la reserva.
        """
        reserva = self.storage.obtener_reserva_por_id(reserva_id)
        if reserva is None:
            raise ReservaNoEncontradaError(reserva_id)
        return reserva

    def crear_reserva(
        self,
        habitacion_id: int,
        nombre_huesped: str,
        email_huesped: str,
        fecha_entrada: str,
        fecha_salida: str,
    ) -> Reserva:
        """Crea una nueva reserva validando disponibilidad y fechas.

        Args:
            habitacion_id: ID de la habitación a reservar.
            nombre_huesped: Nombre completo del huésped.
            email_huesped: Correo electrónico del huésped.
            fecha_entrada: Fecha de entrada en formato 'YYYY-MM-DD'.
            fecha_salida: Fecha de salida en formato 'YYYY-MM-DD'.

        Raises:
            HabitacionNoEncontradaError: Si la habitación no existe.
            HabitacionNoDisponibleError: Si la habitación está ocupada.
            FechaInvalidaError: Si el rango de fechas es inválido.
            DatosInvalidosError: Si algún dato tiene formato incorrecto.
        """
        habitacion = self.obtener_habitacion(habitacion_id)
        if not habitacion.disponible:
            raise HabitacionNoDisponibleError(habitacion.numero)

        entrada = _parsear_fecha(fecha_entrada, "fecha_entrada")
        salida = _parsear_fecha(fecha_salida, "fecha_salida")

        if salida <= entrada:
            raise FechaInvalidaError(
                "La fecha de salida debe ser posterior a la fecha de entrada."
            )

        if not nombre_huesped.strip():
            raise DatosInvalidosError("nombre_huesped", "no puede estar vacío.")
        if "@" not in email_huesped:
            raise DatosInvalidosError("email_huesped", "formato de email inválido.")

        noches = (salida - entrada).days
        total = noches * habitacion.precio_por_noche

        nueva = Reserva(
            id=self.storage.siguiente_id_reserva(),
            habitacion_id=habitacion_id,
            nombre_huesped=nombre_huesped.strip(),
            email_huesped=email_huesped.strip(),
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            total=total,
            estado="activa",
        )
        habitacion.disponible = False
        self.storage.guardar_habitacion(habitacion)
        self.storage.guardar_reserva(nueva)
        return nueva

    def cancelar_reserva(self, reserva_id: int) -> Reserva:
        """Cancela una reserva activa y libera la habitación.

        Args:
            reserva_id: ID de la reserva a cancelar.

        Raises:
            ReservaNoEncontradaError: Si no existe la reserva.
        """
        reserva = self.obtener_reserva(reserva_id)
        reserva.estado = "completada"
        self.storage.guardar_reserva(reserva)

        habitacion = self.storage.obtener_habitacion_por_id(reserva.habitacion_id)
        if habitacion:
            habitacion.disponible = True
            self.storage.guardar_habitacion(habitacion)

        return reserva

    def calcular_ingresos(self) -> float:
        """Calcula el total de ingresos acumulados por reservas completadas."""
        return sum(
            r.total
            for r in self.storage.obtener_reservas()
            if r.estado == "completada"
        )
