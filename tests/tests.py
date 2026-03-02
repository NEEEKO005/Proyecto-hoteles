"""Pruebas unitarias para el sistema de administración de hotel."""

import json
import tempfile
from pathlib import Path

import pytest

from hotel_manager.exceptions import (
    DatosInvalidosError,
    FechaInvalidaError,
    HabitacionNoDisponibleError,
    HabitacionNoEncontradaError,
    ReservaNoEncontradaError,
)
from hotel_manager.services import HotelService
from hotel_manager.storage import HotelStorage

# ── Fixture ───────────────────────────────────────────────────────────────────

_DB_INICIAL = {
    "habitaciones": [
        {"id": 1, "numero": "101", "tipo": "simple", "precio_por_noche": 80.0, "disponible": True},
        {"id": 2, "numero": "201", "tipo": "suite", "precio_por_noche": 200.0, "disponible": False},
    ],
    "reservas": [
        {
            "id": 1,
            "habitacion_id": 2,
            "nombre_huesped": "Ana Torres",
            "email_huesped": "ana@test.com",
            "fecha_entrada": "2025-03-01",
            "fecha_salida": "2025-03-05",
            "total": 800.0,
            "estado": "activa",
        }
    ],
}


@pytest.fixture
def service() -> HotelService:
    """Crea un HotelService con una base de datos temporal aislada por prueba."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(_DB_INICIAL, f, ensure_ascii=False)
        tmp_path = Path(f.name)
    storage = HotelStorage(db_path=tmp_path)
    return HotelService(storage=storage)


# ── Casos normales ────────────────────────────────────────────────────────────


def test_listar_habitaciones_retorna_todas(service: HotelService) -> None:
    """Debe retornar todas las habitaciones registradas."""
    habitaciones = service.listar_habitaciones()
    assert len(habitaciones) == 2


def test_listar_habitaciones_solo_disponibles(service: HotelService) -> None:
    """Debe retornar únicamente las habitaciones disponibles."""
    disponibles = service.listar_habitaciones(solo_disponibles=True)
    assert len(disponibles) == 1
    assert disponibles[0].disponible is True


def test_agregar_habitacion_exitoso(service: HotelService) -> None:
    """Debe agregar correctamente una nueva habitación."""
    hab = service.agregar_habitacion("302", "doble", 150.0)
    assert hab.id == 3
    assert hab.numero == "302"
    assert hab.tipo == "doble"
    assert hab.disponible is True


def test_crear_reserva_exitosa(service: HotelService) -> None:
    """Debe crear una reserva y marcar la habitación como no disponible."""
    reserva = service.crear_reserva(
        habitacion_id=1,
        nombre_huesped="Carlos López",
        email_huesped="carlos@test.com",
        fecha_entrada="2025-04-10",
        fecha_salida="2025-04-15",
    )
    assert reserva.id == 2
    assert reserva.total == 5 * 80.0
    assert reserva.estado == "activa"

    hab = service.obtener_habitacion(1)
    assert hab.disponible is False


def test_cancelar_reserva_libera_habitacion(service: HotelService) -> None:
    """Al cancelar una reserva, la habitación debe quedar disponible."""
    reserva = service.cancelar_reserva(1)
    assert reserva.estado == "completada"

    hab = service.obtener_habitacion(2)
    assert hab.disponible is True


def test_calcular_ingresos_solo_completadas(service: HotelService) -> None:
    """Los ingresos deben considerar solo las reservas completadas."""
    ingresos_iniciales = service.calcular_ingresos()
    assert ingresos_iniciales == 0.0

    service.cancelar_reserva(1)
    ingresos_post = service.calcular_ingresos()
    assert ingresos_post == 800.0


def test_actualizar_habitacion(service: HotelService) -> None:
    """Debe actualizar correctamente los campos especificados."""
    hab = service.actualizar_habitacion(1, precio_por_noche=100.0)
    assert hab.precio_por_noche == 100.0


# ── Casos de error ────────────────────────────────────────────────────────────


def test_obtener_habitacion_inexistente(service: HotelService) -> None:
    """Debe lanzar HabitacionNoEncontradaError si la habitación no existe."""
    with pytest.raises(HabitacionNoEncontradaError):
        service.obtener_habitacion(999)


def test_crear_reserva_habitacion_no_disponible(service: HotelService) -> None:
    """Debe lanzar HabitacionNoDisponibleError si la habitación está ocupada."""
    with pytest.raises(HabitacionNoDisponibleError):
        service.crear_reserva(
            habitacion_id=2,
            nombre_huesped="Pedro Ruiz",
            email_huesped="pedro@test.com",
            fecha_entrada="2025-04-01",
            fecha_salida="2025-04-03",
        )


def test_crear_reserva_fechas_invertidas(service: HotelService) -> None:
    """Debe lanzar FechaInvalidaError si la salida es anterior a la entrada."""
    with pytest.raises(FechaInvalidaError):
        service.crear_reserva(
            habitacion_id=1,
            nombre_huesped="Laura Gil",
            email_huesped="laura@test.com",
            fecha_entrada="2025-05-10",
            fecha_salida="2025-05-05",
        )


def test_agregar_habitacion_tipo_invalido(service: HotelService) -> None:
    """Debe lanzar DatosInvalidosError si el tipo de habitación no es válido."""
    with pytest.raises(DatosInvalidosError):
        service.agregar_habitacion("401", "penthouse", 500.0)


def test_agregar_habitacion_precio_negativo(service: HotelService) -> None:
    """Debe lanzar DatosInvalidosError si el precio es negativo."""
    with pytest.raises(DatosInvalidosError):
        service.agregar_habitacion("402", "simple", -50.0)


def test_cancelar_reserva_inexistente(service: HotelService) -> None:
    """Debe lanzar ReservaNoEncontradaError al cancelar una reserva que no existe."""
    with pytest.raises(ReservaNoEncontradaError):
        service.cancelar_reserva(999)


def test_crear_reserva_email_invalido(service: HotelService) -> None:
    """Debe lanzar DatosInvalidosError si el email no tiene formato válido."""
    with pytest.raises(DatosInvalidosError):
        service.crear_reserva(
            habitacion_id=1,
            nombre_huesped="Mario Vega",
            email_huesped="correo-sin-arroba",
            fecha_entrada="2025-06-01",
            fecha_salida="2025-06-03",
        )


def test_crear_reserva_nombre_vacio(service: HotelService) -> None:
    """Debe lanzar DatosInvalidosError si el nombre del huésped está vacío."""
    with pytest.raises(DatosInvalidosError):
        service.crear_reserva(
            habitacion_id=1,
            nombre_huesped="   ",
            email_huesped="valido@test.com",
            fecha_entrada="2025-07-01",
            fecha_salida="2025-07-03",
        )
