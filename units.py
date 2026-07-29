from __future__ import annotations

"""
OpenFFS Engineering Core

units.py

Defines engineering dimensions, engineering units, and the
engineering unit registry with an integrated conversion engine.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

import json

try:
    import pint
except ImportError as exc:  # pragma: no cover
    raise RuntimeError(
        "The Pint package is required by the OpenFFS Engineering Units "
        "Framework. Install it using: pip install pint"
    ) from exc


@dataclass(frozen=True, slots=True)
class EngineeringUnit:
    """Canonical engineering unit definition."""
    symbol: str
    display_name: str
    dimension: str
    si_factor: float | None
    aliases: tuple[str, ...] = ()
    affine: bool = False


@dataclass(frozen=True, slots=True)
class EngineeringDimension:
    """Represents a physical engineering dimension."""
    name: str
    display_name: str
    base_unit: str
    description: str
    units: dict[str, EngineeringUnit] = field(default_factory=dict)


# =============================================================================
# Pint Abstraction Boundary Layer (ADR-005 Isolation Zone)
# =============================================================================

class PintAdapter:
    """Internal adapter around Pint. No module outside units.py should directly access Pint."""
    def __init__(self) -> None:
        self._ureg: Final[pint.UnitRegistry] = pint.UnitRegistry()

    @property
    def registry(self) -> pint.UnitRegistry:
        """Internal access to the Pint registry."""
        return self._ureg


class ConversionEngine:
    """Performs engineering unit conversions while isolating Pint layers."""
    def __init__(self, adapter: PintAdapter | None = None) -> None:
        self._adapter = adapter or PintAdapter()

    def convert(self, value: float, from_unit: EngineeringUnit, to_unit: EngineeringUnit) -> float:
        """Convert a value between two compatible engineering units with error translation."""
        if from_unit.dimension != to_unit.dimension:
            from openffs.core.exceptions import UnitMismatchError
            raise UnitMismatchError(left_unit=from_unit.symbol, right_unit=to_unit.symbol, operation="conversion")

        try:
            # Explicit Quantity construction to handle offset temperature calculations safely
            ureg = self._adapter.registry
            quantity = ureg.Quantity(value, from_unit.symbol)
            converted = quantity.to(to_unit.symbol)
            return float(converted.magnitude)
        except pint.DimensionalityError as exc:
            from openffs.core.exceptions import UnitMismatchError
            raise UnitMismatchError(left_unit=from_unit.symbol, right_unit=to_unit.symbol, operation="conversion") from exc
        except Exception as exc:
            from openffs.core.exceptions import UnitConversionError
            raise UnitConversionError(from_unit=from_unit.symbol, to_unit=to_unit.symbol, reason=str(exc)) from exc


# =============================================================================
# Core Registry Class
# =============================================================================

class UnitRegistry:
    """Central registry of engineering dimensions and units."""
    def __init__(self, conversion_engine: ConversionEngine | None = None) -> None:
        """Initialize the engineering unit registry with lookup indexes."""
        self._dimensions: dict[str, EngineeringDimension] = {}
        self._units: dict[str, EngineeringUnit] = {}
        self._aliases: dict[str, str] = {}
        self._engine = conversion_engine or ConversionEngine()

    @property
    def dimensions(self) -> dict[str, EngineeringDimension]:
        """Return all registered engineering dimensions."""
        return self._dimensions

    def load(self, json_file: str | Path) -> None:
        """Load engineering reference data from a JSON file."""
        with open(json_file, "r", encoding="utf-8") as fp:
            data: dict[str, Any] = json.load(fp)

        for dim_key, dim_data in data["dimensions"].items():
            units: dict[str, EngineeringUnit] = {}

            for unit_key, unit_data in dim_data["units"].items():
                unit_instance = EngineeringUnit(
                    symbol=unit_data["symbol"],
                    display_name=unit_data["display_name"],
                    dimension=dim_key,
                    si_factor=unit_data.get("si_factor"),
                    aliases=tuple(unit_data.get("aliases", [])),
                    affine=bool(unit_data.get("affine", False)),
                )
                units[unit_key] = unit_instance
                self._units[unit_key.casefold()] = unit_instance

                for alias in unit_data.get("aliases", []):
                    self._aliases[alias.casefold()] = unit_key.casefold()

            self._dimensions[dim_key.casefold()] = EngineeringDimension(
                name=dim_key,
                display_name=dim_data["display_name"],
                base_unit=dim_data["base_unit"],
                description=dim_data["description"],
                units=units,
            )

    def get_dimension(self, dimension_key: str) -> EngineeringDimension:
        """Return a registered engineering dimension."""
        key = dimension_key.casefold()
        if key not in self._dimensions:
            from openffs.core.exceptions import InvalidValueError
            raise InvalidValueError(param_name="dimension", value=dimension_key, reason="Unknown engineering dimension.")
        return self._dimensions[key]

    def get_unit(self, unit_key: str) -> EngineeringUnit:
        """Return a registered engineering unit."""
        key = unit_key.casefold()
        if key in self._units:
            return self._units[key]
        if key in self._aliases:
            canonical = self._aliases[key]
            return self._units[canonical]
        from openffs.core.exceptions import UnsupportedUnitError
        raise UnsupportedUnitError(unit_key)

    def convert(self, value: float, from_unit_str: str, to_unit_str: str) -> float:
        """Convenience faÃ§ade method to convert directly using string symbols or aliases."""
        from_unit = self.get_unit(from_unit_str)
        to_unit = self.get_unit(to_unit_str)
        return self._engine.convert(value, from_unit, to_unit)
    # ------------------------------------------------------------------
    # Engineering Quantity Factory
    # ------------------------------------------------------------------

    def quantity(self, magnitude: float, unit_str: str, metadata=None):
        """
        Create a validated EngineeringQuantity.

        This factory is the recommended construction pathway for all
        engineering quantities within OpenFFS.
        """
        import math
        from openffs.core.exceptions import InvalidValueError
        from openffs.core.quantities import EngineeringQuantity

        # Validate numeric type
        if not isinstance(magnitude, (int, float)):
            raise InvalidValueError(
                param_name="magnitude",
                value=magnitude,
                reason="Magnitude must be a real numeric value.",
            )

        # Reject NaN
        if math.isnan(float(magnitude)):
            raise InvalidValueError(
                param_name="magnitude",
                value=magnitude,
                reason="NaN values are not permitted.",
            )

        # Reject infinities
        if math.isinf(float(magnitude)):
            raise InvalidValueError(
                param_name="magnitude",
                value=magnitude,
                reason="Infinite values are not permitted.",
            )

        # Resolve canonical unit using existing lookup engine
        unit = self.get_unit(unit_str)

        # Construct immutable EngineeringQuantity
        return EngineeringQuantity(
            magnitude=float(magnitude),
            unit=unit,
            metadata=metadata,
        )
