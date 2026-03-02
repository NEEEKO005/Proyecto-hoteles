"""Capa de persistencia: única responsable de leer y escribir el archivo JSON."""

import json
from pathlib import Path

from hotel_manager.models import Habitacion, Reserva

_DEFAULT_DB_PATH = Path(__file__).parent.parent.parent / "data" / "database.json"


class HotelStorage:
    """Gestiona la lectura y escritura de datos en el archivo JSON local.
    """

    def __init__(self, db_path: Path = _DEFAULT_DB_PATH) -> None:
        """Inicializa el almacenamiento con la ruta al archivo de datos.
        """
        self.db_path = db_path

    def _leer(self) -> dict:
        """Lee y retorna el contenido completo del archivo JSON."""
        with self.db_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _escribir(self, data: dict) -> None:
        """Escribe el diccionario dado en el archivo JSON.
        """
        with self.db_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ── Habitaciones ──────────────────────────────────────────────────────────

    def obtener_habitaciones(self) -> list[Habitacion]:
        """Retorna la lista completa de habitaciones del hotel."""
        data = self._leer()
        return [Habitacion.from_dict(h) for h in data["habitaciones"]]

    def obtener_habitacion_por_id(self, habitacion_id: int) -> Habitacion | None:
        """Busca y retorna una habitación por su ID, o None si no existe.
        """
        for habitacion in self.obtener_habitaciones():
            if habitacion.id == habitacion_id:
                return habitacion
        return None

    def guardar_habitacion(self, habitacion: Habitacion) -> None:
        """Crea o actualiza una habitación en el almacenamiento.

        Si ya existe una habitación con el mismo ID, se actualiza. Si no, se agrega como nueva.
        """
        data = self._leer()
        habitaciones = data["habitaciones"]
        for i, h in enumerate(habitaciones):
            if h["id"] == habitacion.id:
                habitaciones[i] = habitacion.to_dict()
                self._escribir(data)
                return
        habitaciones.append(habitacion.to_dict())
        self._escribir(data)

    def eliminar_habitacion(self, habitacion_id: int) -> bool:
        """Elimina una habitación por ID. Retorna True si fue eliminada.
        """
        data = self._leer()
        original = len(data["habitaciones"])
        data["habitaciones"] = [
            h for h in data["habitaciones"] if h["id"] != habitacion_id
        ]
        if len(data["habitaciones"]) < original:
            self._escribir(data)
            return True
        return False

    def siguiente_id_habitacion(self) -> int:
        """Calcula y retorna el siguiente ID disponible para habitaciones."""
        habitaciones = self.obtener_habitaciones()
        if not habitaciones:
            return 1
        return max(h.id for h in habitaciones) + 1

    # ── Reservas ──────────────────────────────────────────────────────────────

    def obtener_reservas(self) -> list[Reserva]:
        """Retorna la lista completa de reservas registradas."""
        data = self._leer()
        return [Reserva.from_dict(r) for r in data["reservas"]]

    def obtener_reserva_por_id(self, reserva_id: int) -> Reserva | None:
        """Busca y retorna una reserva por su ID, o None si no existe.
        """
        for reserva in self.obtener_reservas():
            if reserva.id == reserva_id:
                return reserva
        return None

    def guardar_reserva(self, reserva: Reserva) -> None:
        """Crea o actualiza una reserva en el almacenamiento.
        """
        data = self._leer()
        reservas = data["reservas"]
        for i, r in enumerate(reservas):
            if r["id"] == reserva.id:
                reservas[i] = reserva.to_dict()
                self._escribir(data)
                return
        reservas.append(reserva.to_dict())
        self._escribir(data)

    def eliminar_reserva(self, reserva_id: int) -> bool:
        """Elimina una reserva por ID. Retorna True si fue eliminada.
        """
        data = self._leer()
        original = len(data["reservas"])
        data["reservas"] = [r for r in data["reservas"] if r["id"] != reserva_id]
        if len(data["reservas"]) < original:
            self._escribir(data)
            return True
        return False

    def siguiente_id_reserva(self) -> int:
        """Calcula y retorna el siguiente ID disponible para reservas."""
        reservas = self.obtener_reservas()
        if not reservas:
            return 1
        return max(r.id for r in reservas) + 1
