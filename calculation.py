"""
OpenFFS
========

Document Number : OSAS-004
Revision        : Rev 1.0
Status          : Approved for Implementation
Module          : calculation.py

Title
-----
Base Calculation Framework

Purpose
-------
Defines the abstract foundation for every engineering calculation
performed within OpenFFS.

Every engineering calculation—whether a simple corrosion rate,
an API 579 Fitness-for-Service assessment, a structural integrity
evaluation, or a future engineering module—shall inherit from
BaseCalculation.

The framework enforces:

    • Standard execution workflow
    • Input validation
    • Transparent assumptions
    • Standards traceability
    • Warning collection
    • Deterministic execution
    • Reproducible engineering calculations

This module intentionally contains no engineering equations.
It defines only the framework upon which engineering calculations
are built.

Engineering Principles
----------------------
• Transparency
• Determinism
• Traceability
• Modularity
• Single Responsibility
• Explainability

Engineering Knowledge Shared.
Integrity Assured.
Wisdom Preserved.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class CalculationError(Exception):
    """
    Base exception for engineering calculations.
    """


class ValidationError(CalculationError):
    """
    Raised when calculation input validation fails.
    """


class ExecutionError(CalculationError):
    """
    Raised when a calculation cannot be completed.
    """


class BaseCalculation(ABC):
    """
    Abstract base class for all OpenFFS engineering calculations.

    Every engineering calculation shall inherit from this class.

    Execution Workflow
    ------------------

        validate_inputs()

            ↓

        calculate()

            ↓

        return result()

    Notes
    -----
    Subclasses should implement only engineering-specific logic.

    Logging, validation, metadata collection, reporting, and
    traceability are managed by this framework.
    """

    ####################################################################
    # Construction
    ####################################################################

    def __init__(
        self,
        *,
        name: str,
        standard: Optional[str] = None,
        clause: Optional[str] = None,
        description: str = "",
    ) -> None:
        """
        Initialize an engineering calculation.

        Parameters
        ----------
        name
            Human-readable calculation name.

        standard
            Applicable engineering standard.

        clause
            Standard clause or reference.

        description
            Optional engineering description.
        """

        self._name = name
        self._standard = standard
        self._clause = clause
        self._description = description

        self._created = datetime.now(timezone.utc)

        self._inputs: Dict[str, Any] = {}

        self._outputs: Dict[str, Any] = {}

        self._assumptions: List[str] = []

        self._warnings: List[str] = []

        self._references: List[str] = []

        self._metadata: Dict[str, Any] = {}

    ####################################################################
    # Public Properties
    ####################################################################

    @property
    def name(self) -> str:
        """Calculation name."""
        return self._name

    @property
    def standard(self) -> Optional[str]:
        """Applicable engineering standard."""
        return self._standard

    @property
    def clause(self) -> Optional[str]:
        """Applicable engineering clause."""
        return self._clause

    @property
    def description(self) -> str:
        """Engineering description."""
        return self._description

    @property
    def inputs(self) -> Dict[str, Any]:
        """Read-only calculation inputs."""
        return dict(self._inputs)

    @property
    def outputs(self) -> Dict[str, Any]:
        """Read-only calculation outputs."""
        return dict(self._outputs)

    @property
    def assumptions(self) -> List[str]:
        """Engineering assumptions."""
        return list(self._assumptions)

    @property
    def warnings(self) -> List[str]:
        """Engineering warnings."""
        return list(self._warnings)

    @property
    def references(self) -> List[str]:
        """Engineering references."""
        return list(self._references)

    @property
    def metadata(self) -> Dict[str, Any]:
        """Calculation metadata."""
        return dict(self._metadata)

    ####################################################################
    # Input / Output Management
    ####################################################################

    def set_input(self, name: str, value: Any) -> None:
        """
        Store a calculation input.

        Parameters
        ----------
        name
            Input variable name.

        value
            Input value.
        """

        self._inputs[name] = value

    def get_input(self, name: str) -> Any:
        """
        Retrieve an input value.

        Raises
        ------
        KeyError
            If the input has not been defined.
        """

        return self._inputs[name]

    def set_output(self, name: str, value: Any) -> None:
        """
        Store a calculation output.
        """

        self._outputs[name] = value

    ####################################################################
    # Engineering Documentation
    ####################################################################

    def add_assumption(self, text: str) -> None:
        """
        Record an engineering assumption.
        """

        if text not in self._assumptions:
            self._assumptions.append(text)

    def add_warning(self, text: str) -> None:
        """
        Record a calculation warning.
        """

        if text not in self._warnings:
            self._warnings.append(text)

    def add_reference(self, text: str) -> None:
        """
        Record an engineering reference.
        """

        if text not in self._references:
            self._references.append(text)

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Store calculation metadata.
        """

        self._metadata[key] = value

    ####################################################################
    # Validation
    ####################################################################

    @abstractmethod
    def validate_inputs(self) -> None:
        """
        Validate engineering inputs.

        Implementations shall raise ValidationError if validation fails.
        """

    ####################################################################
    # Engineering Calculation
    ####################################################################

    @abstractmethod
    def calculate(self) -> None:
        """
        Execute the engineering calculation.

        Implementations should populate outputs using set_output().
        """

    ####################################################################
    # Execution Framework
    ####################################################################

    def execute(self) -> Dict[str, Any]:
        """
        Execute the complete engineering workflow.

        Returns
        -------
        dict
            Standardized engineering calculation record.

        Raises
        ------
        ValidationError
            Invalid engineering input.

        ExecutionError
            Calculation failure.
        """

        try:

            self.validate_inputs()

            self.calculate()

            return self.result()

        except ValidationError:
            raise

        except Exception as exc:

            raise ExecutionError(
                f"Calculation '{self.name}' failed."
            ) from exc

    ####################################################################
    # Standard Result
    ####################################################################

    def result(self) -> Dict[str, Any]:
        """
        Build a standardized calculation result.

        Notes
        -----
        A dedicated CalculationResult class will replace this
        dictionary in a future OpenFFS revision (OSAS-005).
        """

        return {
            "name": self._name,
            "description": self._description,
            "standard": self._standard,
            "clause": self._clause,
            "created": self._created.isoformat(),
            "inputs": dict(self._inputs),
            "outputs": dict(self._outputs),
            "assumptions": list(self._assumptions),
            "warnings": list(self._warnings),
            "references": list(self._references),
            "metadata": dict(self._metadata),
        }

    ####################################################################
    # Representation
    ####################################################################

    def __repr__(self) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.__class__.__name__}"
            f"(name={self._name!r}, "
            f"standard={self._standard!r})"
        )