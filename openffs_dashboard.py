import sys
import os

# Dynamically locate the exact absolute folder pathway where this running dashboard script sits
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Map explicit target paths directly to the underlying package directories
part3_path = os.path.abspath(os.path.join(BASE_DIR, 'openffs', 'api579', 'part3'))
part4_path = os.path.abspath(os.path.join(BASE_DIR, 'openffs', 'api579', 'part4'))
part5_path = os.path.abspath(os.path.join(BASE_DIR, 'openffs', 'api579', 'part5'))
part6_path = os.path.abspath(os.path.join(BASE_DIR, 'openffs', 'api579', 'part6'))
part7_path = os.path.abspath(os.path.join(BASE_DIR, 'openffs', 'api579', 'part7'))
part9_path = os.path.abspath(os.path.join(BASE_DIR, 'openffs', 'api579', 'part9'))
part14_path = os.path.abspath(os.path.join(BASE_DIR, 'openffs', 'api579', 'part14'))

# Inject these verified directory locations straight into Python's active system path array
for path_dir in [BASE_DIR, part3_path, part4_path, part5_path, part6_path, part7_path, part9_path, part14_path]:
    if path_dir not in sys.path:
        sys.path.insert(0, path_dir)

# Safely import your local PDF documentation module
import pdf_generator  

def display_menu():
    print("\n" + "="*65)
    print("   Open_FFS_Initiative Software Engineering Enterprise Suite  ")
    print("="*65)
    print("   Part 3  - Low-Temperature Brittle Fracture & MDMT")
    print("   Part 4  - General Metal Loss (Uniform Thinning Text Parser)")
    print("   Part 5  - Local Metal Loss (Multi-Point UT Excel Parser)")
    print("   Part 6  - Pitting Damage (Localized Pit Spacing Field Logic)")
    print("   Part 7  - Hydrogen Blister and HIC Damage Screening")
    print("   Part 9  - Crack-Like Flaws Structural Assessment")
    print("  Part 14 - Paris' Law Fatigue Crack Life Integration")
    print("   V       - Run Automated API Benchmark Verification Ledger")
    print("   0       - Exit Application Workspace Window")
    print("="*65)

def get_signature_stamp_details():
    print("\n" + "-"*40)
    name = input("Enter Reviewing Senior Engineer's Name for Certificate Stamp: ").strip()
    if name == "":
        return "S. Prakash (Senior Structural Engineer)"
    return name

def main():
    while True:
        display_menu()
        choice = input("Select an API 579 Engineering Track Module to Execute: ").strip()
        
        if choice == '0':
            print("\nExiting OpenFFS Engine Workspace. Systems Synced Safely.")
            break
            
        elif choice == '3':
            import brittle_fracture_core
            print("\n--- Initiating API 579 Part 3 Brittle Fracture Evaluation ---")
            thickness = float(input("Enter Governing Component Thickness (inches): "))
            cet = float(input("Enter Site Critical Exposure Temperature (CET) (deg F): "))
            
            res = brittle_fracture_core.evaluate_brittle_fracture_mdmt("Carbon Steel Spec", thickness, cet, -20.0)
            print("\n[EVALUATION RESULT]:", res)
            
            reviewer = get_signature_stamp_details()
            inputs = {"Governing_Thickness_in": thickness, "Critical_Exposure_Temp_F": cet, "Base_MDMT_Limit_F": -20.0}
            metrics = {"Adjusted_MDMT_Threshold_F": res["calculated_adjusted_mdmt_f"]}
            
            pdf_filename = "Part3_Brittle_Fracture_Report.pdf"
            pdf_generator.generate_certified_pdf_report("Part 3 - Brittle Fracture Screening", inputs, metrics, res["status"], reviewer, pdf_filename)
            
        elif choice == '4':
            import general_loss_core
            print("\n--- Initiating API 579 Part 4 General Metal Loss Evaluation ---")
            data = general_loss_core.parse_site_record(os.path.join(part4_path, 'site_finding_report.txt'))
            if data:
                res = general_loss_core.evaluate_general_metal_loss(
                    data["nominal_thickness"], data["measured_thickness"], 
                    data["allowable_stress"], data["radius"], data["efficiency"], data["pressure"]
                )
                print("[EVALUATION RESULT]:", res)
                
                reviewer = get_signature_stamp_details()
                pdf_filename = "Part4_General_Metal_Loss_Report.pdf"
                pdf_generator.generate_certified_pdf_report("Part 4 - General Metal Loss", data, {"Required_t_min_in": res["required_t_min_in"], "Thickness_Margin_in": res["thickness_margin_in"]}, res["status"], reviewer, pdf_filename)
            else:
                print("[ERROR]: Missing site finding file report.")
                
        elif choice == '5':
            import local_loss_core
            print("\n--- Initiating API 579 Part 5 Local Metal Loss Evaluation ---")
            csv_path = os.path.join(part5_path, 'ut_grid_report.csv')
            readings = local_loss_core.parse_excel_grid(csv_path)
            if readings:
                res = local_loss_core.evaluate_local_metal_loss(readings, t_min=0.350)
                print("[EVALUATION RESULT]:", res)
                
                reviewer = get_signature_stamp_details()
                pdf_filename = "Part5_Local_Metal_Loss_Report.pdf"
                pdf_generator.generate_certified_pdf_report("Part 5 - Local Metal Loss Grid", {"Total_Readings_Parsed": len(readings)}, {"Absolute_Minimum_t_in": res["absolute_minimum_t_in"], "Critical_Threshold_in": res["critical_threshold_in"]}, res["status"], reviewer, pdf_filename)
            else:
                print("[ERROR]: ut_grid_report.csv data sheet could not be loaded.")

        elif choice == '6':
            import pitting_core
            print("\n--- Initiating API 579 Part 6 Pitting Damage Evaluation ---")
            nominal = float(input("Enter Nominal Original Wall Thickness (inches): "))
            measured = float(input("Enter Absolute Minimum Measured Pit Base Wall (inches): "))
            res = pitting_core.evaluate_pitting_damage(nominal, measured, 0.125, 0.500, 300, 12.0, 15000)
            print("\n[EVALUATION RESULT]:", res)
            
            reviewer = get_signature_stamp_details()
            inputs = {"Nominal_Thickness_in": nominal, "Measured_Min_Pit_Wall_in": measured, "Pit_Diameter_in": 0.125, "Pit_Spacing_in": 0.500}
            metrics = {"Required_t_min_in": res["required_t_min_in"], "Pit_Spacing_Ratio": res["pit_spacing_ratio"]}
            
            pdf_filename = "Part6_Pitting_Damage_Report.pdf"
            pdf_generator.generate_certified_pdf_report("Part 6 - Pitting Damage Screening", inputs, metrics, res["status"], reviewer, pdf_filename)

        elif choice == '7':
            import blister_core
            print("\n--- Initiating API 579 Part 7 Hydrogen Blister Evaluation ---")
            nom = float(input("Enter Nominal Original Wall Thickness (inches): "))
            meas = float(input("Enter Measured Min Sound Thickness profile (inches): "))
            dia = float(input("Enter Extracted Blister Void Diameter (inches): "))
            crown = float(input("Enter Measured Blister Crown Deflection Height (inches): "))
            press = float(input("Enter Pipeline Design Operating Pressure (psi): "))
            rad = float(input("Enter Pipe Internal Shell Radius (inches): "))
            stress = float(input("Enter Material Allowable Design Stress (psi): "))
            
            res = blister_core.evaluate_hydrogen_blister(nom, meas, dia, crown, press, rad, stress)
            print("\n[EVALUATION RESULT]:", res)
            
            reviewer = get_signature_stamp_details()
            inputs = {"Nominal_Thickness_in": nom, "Measured_Sound_Thickness_in": meas, "Blister_Diameter_in": dia, "Crown_Height_in": crown, "Operating_Pressure_psi": press, "Pipe_Radius_in": rad}
            metrics = {"Required_t_min_in": res["required_t_min_in"], "Max_Allowable_Diameter_in": res["max_allowable_diameter_in"], "Sound_Metal_Thickness_in": res["sound_metal_thickness_in"]}
            
            pdf_filename = "Part7_Hydrogen_Blister_Report.pdf"
            pdf_generator.generate_certified_pdf_report("Part 7 - Hydrogen Blister Screening", inputs, metrics, res["status"], reviewer, pdf_filename)
            
        elif choice == '9':
            import level1_core
            print("\n--- Initiating API 579 Part 9 Crack-Like Flaw Evaluation ---")
            p = float(input("Enter Design Operating Pressure (psi): "))
            depth = float(input("Enter Local Crack Flaw Depth (inches): "))
            res = level1_core.calculate_allowable_pressure(p, 17500, 0.5, 24.0, depth, 3.0)
            print("\n[EVALUATION RESULT]:", res)
            
            reviewer = get_signature_stamp_details()
            pdf_filename = "Part9_Crack_Flaw_Report.pdf"
            pdf_generator.generate_certified_pdf_report("Part 9 - Crack-Like Flaws", {"Operating_Pressure_psi": p, "Flaw_Depth_in": depth}, {"Base_MAWP_psi": res["base_mawp_psi"], "Reduced_MAWP_psi": res["reduced_mawp_psi"]}, res["status"], reviewer, pdf_filename)

        elif choice == '14':
            import fatigue_core
            print("\n--- Initiating API 579 Part 14 Fatigue Life Integration ---")
            cycles = float(input("Enter Targeted Cyclic Fatigue Evaluation Horizon (Cycles): "))
            res = fatigue_core.evaluate_paris_law_growth(0.05, 15.0, cycles, 3.6e-10, 3.0)
            print("\n[EVALUATION RESULT]:", res)
            
            reviewer = get_signature_stamp_details()
            pdf_filename = "Part14_Fatigue_Assessment_Report.pdf"
            pdf_generator.generate_certified_pdf_report("Part 14 - Fatigue Crack Growth", {"Target_Cycles": cycles, "Initial_Depth_in": 0.05}, {"Final_Depth_in": res["final_depth_in"], "Total_Growth_in": res["total_growth_in"]}, str(res["stable_growth"]), reviewer, pdf_filename)

        elif choice == 'V' or choice == 'v':
            import sys
            sys.path.append(os.path.join(BASE_DIR, 'validation'))
            import run_benchmarks
            run_benchmarks.execute_mathematical_audit()

        else:
            print("\n[INVALID SELECTION]: Please pick a valid engineering track index option.")
            
        input("\nPress Enter to return to main launcher control board...")

if __name__ == "__main__":
    main()

