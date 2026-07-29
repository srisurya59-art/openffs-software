from calculation import BaseCalculation, ValidationError

class Part4MetalLoss(BaseCalculation):
    """
    API 579-1 Part 4 Level 1 Assessment for General Metal Loss.
    Inherits from the core OpenFFS BaseCalculation framework.
    """
    
    def __init__(self):
        super().__init__(
            name="API 579 Part 4 - General Metal Loss",
            standard="API 579-1 / ASME FFS-1",
            clause="Part 4, Section 4.4.2",
            description="Level 1 evaluation of components subjected to general corrosion masking."
        )

    def validate_inputs(self) -> None:
        """Enforces rigorous industrial input guardrails (Addressing Page 7 of Review)."""
        p = self.get_input("pressure")
        s = self.get_input("allowable_stress")
        d = self.get_input("diameter")
        t_nom = self.get_input("t_nominal")
        t_min_m = self.get_input("t_min_measured")

        if p <= 0 or s <= 0 or d <= 0 or t_nom <= 0:
            raise ValidationError("Operational and geometric inputs must be strictly positive values.")
        if t_min_m > t_nom:
            raise ValidationError("Measured minimum wall thickness cannot exceed nominal thickness spec.")

    def calculate(self) -> None:
        """Executes traceable design thickness code calculations (Addressing Page 3 & 11)."""
        # Fetch verified inputs
        p = self.get_input("pressure")
        s = self.get_input("allowable_stress")
        e = self.get_input("efficiency")
        d = self.get_input("diameter")
        t_min_m = self.get_input("t_min_measured")
        fca = self.get_input("corrosion_allowance")

        # 🧮 ASME Section VIII Div 1 governing hoop stress thickness formula
        t_min_required = (p * (d / 2)) / ((s * e) - (0.6 * p))
        
        # Determine actual available corroded ligament thickness
        t_available = t_min_m - fca
        
        # Calculate Remaining Strength Factor (RSF)
        rsf = 1.0 if t_available >= t_min_required else (t_available / t_min_required if t_min_required > 0 else 0.0)
        
        # Populate standardized results into framework output arrays
        self.set_output("t_min_required", t_min_required)
        self.set_output("t_available", t_available)
        self.set_output("rsf", rsf)
        self.set_output("status", "PASS (Level 1)" if rsf >= 0.90 else "REJECT / ACTION REQUIRED")

        # Record audit traceability documentation metadata
        self.add_assumption("Thin-walled cylindrical membrane shell theory applies.")
        self.add_assumption("Loading configurations are limited to uniform internal static pressure fields.")
        self.add_reference("API 579-1/ASME FFS-1 2021 Edition, Fitness-For-Service.")
        self.add_reference("ASME Section VIII, Division 1 Code Construction Rules.")

