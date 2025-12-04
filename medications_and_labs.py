"""
RxNorm and LOINC Codes for HIV/AIDS Care
Based on DHHS Guidelines for Adults and Adolescents with HIV (2024)
Includes all initial assessment and monitoring tests
"""

# ============================================================================
# HIV ANTIRETROVIRAL MEDICATIONS (RxNorm Codes)
# ============================================================================

HIV_MEDICATIONS = {
    # Single Tablet Regimens (STRs) - First Line
    'biktarvy': {
        'rxnorm': '2120107',
        'name': 'Biktarvy',
        'components': 'bictegravir 50mg / emtricitabine 200mg / tenofovir alafenamide 25mg',
        'class': 'INSTI + NRTI',
        'frequency': 'Once daily',
        'notes': 'Preferred first-line regimen'
    },
    'triumeq': {
        'rxnorm': '1546773',
        'name': 'Triumeq',
        'components': 'dolutegravir 50mg / abacavir 600mg / lamivudine 300mg',
        'class': 'INSTI + NRTI',
        'frequency': 'Once daily',
        'notes': 'Requires HLA-B*5701 negative'
    },
    'dovato': {
        'rxnorm': '2183126',
        'name': 'Dovato',
        'components': 'dolutegravir 50mg / lamivudine 300mg',
        'class': 'INSTI + NRTI (2-drug)',
        'frequency': 'Once daily',
        'notes': 'For VL <500K, no HBV, no resistance'
    },
    'genvoya': {
        'rxnorm': '1721606',
        'name': 'Genvoya',
        'components': 'elvitegravir 150mg / cobicistat 150mg / emtricitabine 200mg / tenofovir alafenamide 10mg',
        'class': 'INSTI + Booster + NRTI',
        'frequency': 'Once daily'
    },
    'symtuza': {
        'rxnorm': '2041831',
        'name': 'Symtuza',
        'components': 'darunavir 800mg / cobicistat 150mg / emtricitabine 200mg / tenofovir alafenamide 10mg',
        'class': 'PI + Booster + NRTI',
        'frequency': 'Once daily'
    },
    'atripla': {
        'rxnorm': '722971',
        'name': 'Atripla',
        'components': 'efavirenz 600mg / emtricitabine 200mg / tenofovir disoproxil fumarate 300mg',
        'class': 'NNRTI + NRTI',
        'frequency': 'Once daily',
        'notes': 'Alternative regimen, CNS side effects'
    },
    
    # NRTI Backbones
    'descovy': {
        'rxnorm': '1721603',
        'name': 'Descovy',
        'components': 'emtricitabine 200mg / tenofovir alafenamide 25mg',
        'class': 'NRTI backbone',
        'frequency': 'Once daily (with 3rd agent)'
    },
    'truvada': {
        'rxnorm': '617296',
        'name': 'Truvada',
        'components': 'emtricitabine 200mg / tenofovir disoproxil fumarate 300mg',
        'class': 'NRTI backbone',
        'frequency': 'Once daily (treatment or PrEP)'
    },
    
    # Long-Acting Injectable
    'cabenuva': {
        'rxnorm': '2471641',
        'name': 'Cabenuva',
        'components': 'cabotegravir 200mg/ml / rilpivirine 300mg/ml',
        'class': 'INSTI + NNRTI (long-acting)',
        'frequency': 'Monthly or every 2 months IM injection'
    },
    
    # Single Agents - INSTIs
    'tivicay': {
        'rxnorm': '1433868',
        'name': 'Tivicay',
        'components': 'dolutegravir 50mg',
        'class': 'Integrase Inhibitor',
        'frequency': 'Once or twice daily'
    },
    'isentress': {
        'rxnorm': '617886',
        'name': 'Isentress',
        'components': 'raltegravir 400mg',
        'class': 'Integrase Inhibitor',
        'frequency': 'Twice daily'
    },
    
    # Single Agents - NRTIs
    'viread': {
        'rxnorm': '352372',
        'name': 'Viread',
        'components': 'tenofovir disoproxil fumarate 300mg',
        'class': 'NRTI',
        'frequency': 'Once daily'
    },
    'epivir': {
        'rxnorm': '105585',
        'name': 'Epivir',
        'components': 'lamivudine 300mg',
        'class': 'NRTI',
        'frequency': 'Once daily'
    }
}

# ============================================================================
# INITIAL ASSESSMENT - REQUIRED BASELINE TESTS
# ============================================================================

BASELINE_REQUIRED_TESTS = {
    # HIV-Specific Baseline Tests
    'hiv_viral_load': {
        'loinc': '20447-9',
        'name': 'HIV 1 RNA [#/volume] (viral load) in Serum or Plasma by NAA with probe detection',
        'unit': 'copies/mL',
        'frequency': 'Baseline, then per monitoring schedule',
        'clinical_significance': 'Establishes baseline viremia'
    },
    'cd4_count': {
        'loinc': '24467-3',
        'name': 'CD3+CD4+ (T4 helper) cells [#/volume] in Blood',
        'unit': 'cells/µL',
        'frequency': 'Baseline, then per monitoring schedule',
        'clinical_significance': 'Assesses immune function, guides OI prophylaxis'
    },
    'cd4_percent': {
        'loinc': '32518-1',
        'name': 'CD3+CD4+ (T4 helper) cells/100 cells in Blood',
        'unit': '%',
        'frequency': 'Baseline (alternative to absolute count)',
        'notes': 'Less variable than absolute count; 200 cells/µL ≈ 14%, 500 ≈ 29%'
    },
    
    # Resistance and Pharmacogenomic Testing
    'hiv_resistance_genotype': {
        'loinc': '51969-4',
        'name': 'HIV 1 genotype [Identifier] in Isolate',
        'frequency': 'Before starting ART, at virologic failure',
        'clinical_significance': 'REQUIRED to guide ART selection',
        'notes': 'Test PR, RT genes; also integrase if INSTI resistance suspected'
    },
    'hla_b5701': {
        'loinc': '13303-3',
        'name': 'HLA-B*57:01 [Presence]',
        'frequency': 'One time before abacavir',
        'clinical_significance': 'REQUIRED before ABC - prevents hypersensitivity reaction',
        'contraindication': 'If positive, do NOT prescribe abacavir'
    },
    
    # Hepatitis Screening (REQUIRED before ART)
    'hep_b_surface_ag': {
        'loinc': '5196-1',
        'name': 'Hepatitis B virus surface Ag [Presence] in Serum',
        'frequency': 'Baseline, periodic if at risk',
        'clinical_significance': 'Active HBV infection - affects ART choice'
    },
    'hep_b_surface_ab': {
        'loinc': '16935-9',
        'name': 'Hepatitis B virus surface Ab [Units/volume] in Serum',
        'unit': 'mIU/mL',
        'frequency': 'Baseline',
        'interpretation': '>10 mIU/mL = immune (vaccine or recovery)'
    },
    'hep_b_core_ab': {
        'loinc': '13952-0',
        'name': 'Hepatitis B virus core Ab [Presence] in Serum',
        'frequency': 'Baseline',
        'interpretation': 'Positive = prior or current infection'
    },
    'hep_c_antibody': {
        'loinc': '16128-1',
        'name': 'Hepatitis C virus Ab [Presence] in Serum',
        'frequency': 'Baseline, annual if at risk',
        'clinical_significance': 'Screen for HCV coinfection (~15-30% in HIV+)'
    },
    'hep_c_rna': {
        'loinc': '11259-1',
        'name': 'Hepatitis C virus RNA [Units/volume] in Serum or Plasma by NAA',
        'unit': 'IU/mL',
        'frequency': 'If HCV Ab positive',
        'interpretation': 'Detectable = active infection requiring treatment'
    },
    'hep_a_total_ab': {
        'loinc': '20575-7',
        'name': 'Hepatitis A virus Ab [Presence] in Serum',
        'frequency': 'Baseline',
        'clinical_significance': 'Vaccinate if negative'
    },
    
    # Complete Blood Count
    'cbc_with_diff': {
        'loinc': '58410-2',
        'name': 'Complete blood count (CBC) panel - Blood by Automated count',
        'frequency': 'Baseline, then every 3-6 months',
        'includes': 'WBC, RBC, Hgb, Hct, Platelets, Differential',
        'clinical_significance': 'Monitor for cytopenia from HIV or medications'
    },
    
    # Chemistry Panel
    'bmp': {
        'loinc': '24323-8',
        'name': 'Comprehensive metabolic panel',
        'frequency': 'Baseline, then every 3-6 months',
        'includes': 'Na, K, Cl, CO2, BUN, Creatinine, Glucose, Ca',
        'clinical_significance': 'Renal and metabolic function'
    },
    'creatinine': {
        'loinc': '2160-0',
        'name': 'Creatinine [Mass/volume] in Serum or Plasma',
        'unit': 'mg/dL',
        'frequency': 'Baseline, every 3-6 months',
        'reference': '0.6-1.2 mg/dL'
    },
    'egfr': {
        'loinc': '48643-1',
        'name': 'Glomerular filtration rate/1.73 sq M.predicted by Creatinine',
        'unit': 'mL/min/1.73m²',
        'frequency': 'Baseline, every 3-6 months',
        'clinical_significance': 'CRITICAL for tenofovir dosing',
        'reference': '>60 mL/min/1.73m²'
    },
    'serum_phosphate': {
        'loinc': '2777-1',
        'name': 'Phosphate [Mass/volume] in Serum or Plasma',
        'unit': 'mg/dL',
        'frequency': 'If on TDF with CKD',
        'notes': 'Monitor for Fanconi syndrome with tenofovir'
    },
    
    # Liver Function Tests
    'alt': {
        'loinc': '1742-6',
        'name': 'Alanine aminotransferase [Enzymatic activity/volume] in Serum or Plasma',
        'unit': 'U/L',
        'frequency': 'Baseline, every 3-6 months',
        'reference': '7-56 U/L',
        'clinical_significance': 'Monitor for hepatotoxicity'
    },
    'ast': {
        'loinc': '1920-8',
        'name': 'Aspartate aminotransferase [Enzymatic activity/volume] in Serum or Plasma',
        'unit': 'U/L',
        'frequency': 'Baseline, every 3-6 months',
        'reference': '10-40 U/L'
    },
    'bilirubin_total': {
        'loinc': '1975-2',
        'name': 'Bilirubin.total [Mass/volume] in Serum or Plasma',
        'unit': 'mg/dL',
        'frequency': 'Baseline, then as indicated',
        'notes': 'Elevated with atazanavir (indirect hyperbilirubinemia)'
    },
    
    # Lipid Panel
    'lipid_panel_fasting': {
        'loinc': '57698-3',
        'name': 'Lipid panel with direct LDL - Serum or Plasma',
        'frequency': 'Baseline (fasting), then annually or per CV risk',
        'clinical_significance': 'Monitor for dyslipidemia from ART'
    },
    'cholesterol_total': {
        'loinc': '2093-3',
        'name': 'Cholesterol [Mass/volume] in Serum or Plasma',
        'unit': 'mg/dL',
        'reference': '<200 mg/dL desirable'
    },
    'hdl': {
        'loinc': '2085-9',
        'name': 'HDL Cholesterol [Mass/volume] in Serum or Plasma',
        'unit': 'mg/dL',
        'reference': '>40 mg/dL (men), >50 mg/dL (women)'
    },
    'ldl': {
        'loinc': '13457-7',
        'name': 'LDL Cholesterol [Mass/volume] in Serum or Plasma by calculation',
        'unit': 'mg/dL',
        'reference': '<100 mg/dL optimal'
    },
    'triglycerides': {
        'loinc': '2571-8',
        'name': 'Triglyceride [Mass/volume] in Serum or Plasma',
        'unit': 'mg/dL',
        'reference': '<150 mg/dL',
        'notes': 'Requires fasting; elevated with some PIs'
    },
    
    # Glucose/Diabetes Screening
    'glucose_fasting': {
        'loinc': '1558-6',
        'name': 'Fasting glucose [Mass/volume] in Serum or Plasma',
        'unit': 'mg/dL',
        'frequency': 'Baseline, then annually',
        'reference': '70-100 mg/dL',
        'clinical_significance': 'Monitor for diabetes from ART'
    },
    'hba1c': {
        'loinc': '4548-4',
        'name': 'Hemoglobin A1c/Hemoglobin.total in Blood',
        'unit': '%',
        'frequency': 'If diabetic or prediabetic',
        'reference': '<5.7%',
        'notes': 'NOT recommended for initial diabetes diagnosis in HIV+ on ART'
    },
    
    # Urinalysis (REQUIRED with tenofovir)
    'urinalysis': {
        'loinc': '24357-6',
        'name': 'Urinalysis macro (dipstick) panel - Urine',
        'frequency': 'Baseline, then periodic with TAF/TDF regimens',
        'clinical_significance': 'Monitor protein & glucose for renal toxicity'
    },
    'urine_protein': {
        'loinc': '2888-6',
        'name': 'Protein [Mass/volume] in Urine',
        'frequency': 'With tenofovir regimens',
        'notes': 'Part of renal monitoring'
    },
    
    # Pregnancy Testing
    'pregnancy_test': {
        'loinc': '2118-8',
        'name': 'β-hCG [Mass/volume] in Serum or Plasma',
        'frequency': 'Baseline for women of childbearing age, then as indicated',
        'clinical_significance': 'Some ARVs contraindicated or require caution in pregnancy'
    },
    
    # Sexually Transmitted Infections
    'syphilis_rpr': {
        'loinc': '20507-0',
        'name': 'Reagin Ab [Presence] in Serum by RPR',
        'frequency': 'Baseline, then at least annually',
        'clinical_significance': 'MSM and sexually active persons at high risk'
    },
    'gonorrhea_urine': {
        'loinc': '21415-5',
        'name': 'Neisseria gonorrhoeae DNA [Presence] in Urine by NAA',
        'frequency': 'Baseline, then at least annually for sexually active'
    },
    'chlamydia_urine': {
        'loinc': '21613-5',
        'name': 'Chlamydia trachomatis DNA [Presence] in Urine by NAA',
        'frequency': 'Baseline, then at least annually for sexually active'
    },
    
    # Opportunistic Infection Screening
    'toxoplasma_igg': {
        'loinc': '22570-6',
        'name': 'Toxoplasma gondii IgG Ab [Presence] in Serum',
        'frequency': 'Baseline',
        'clinical_significance': 'If positive and CD4<100, start prophylaxis'
    },
    'cmv_igg': {
        'loinc': '22244-8',
        'name': 'Cytomegalovirus IgG Ab [Presence] in Serum',
        'frequency': 'Baseline',
        'notes': 'Risk stratification for CMV disease if CD4<50'
    },
    'tb_igra': {
        'loinc': '38372-3',
        'name': 'Mycobacterium tuberculosis stimulated gamma interferon [Presence] in Blood',
        'frequency': 'Baseline, then annually if high risk',
        'notes': 'QuantiFERON or T-SPOT preferred over TST in HIV+'
    },
    'tb_skin_test': {
        'loinc': '11580-3',
        'name': 'Tuberculin skin test reaction',
        'unit': 'mm induration',
        'frequency': 'Baseline if IGRA not available',
        'interpretation': '≥5mm positive in HIV+'
    }
}

# ============================================================================
# MONITORING SCHEDULE AFTER ART INITIATION
# ============================================================================

MONITORING_SCHEDULE = {
    # Weeks 2-8 after starting/changing ART
    'early_monitoring': {
        'timing': '2-4 weeks (no later than 8 weeks)',
        'tests': {
            'hiv_viral_load': 'Confirm response to therapy',
            'continue_every': '4-8 weeks until suppressed to <50 copies/mL'
        }
    },
    
    # Every 3-6 months (stable patients)
    'routine_monitoring': {
        'timing': 'Every 3-6 months',
        'tests': {
            'hiv_viral_load': 'Confirm sustained suppression',
            'cd4_count': 'Monitor immune recovery',
            'cbc_with_diff': 'Monitor for cytopenia',
            'bmp': 'Renal and electrolyte function',
            'alt_ast': 'Hepatotoxicity monitoring',
            'notes': 'Can extend to every 6 months if VL suppressed >1 year and stable'
        }
    },
    
    # Annual monitoring
    'annual_monitoring': {
        'timing': 'Annually',
        'tests': {
            'lipid_panel': 'CV risk assessment',
            'glucose_fasting': 'Diabetes screening',
            'hep_c_antibody': 'If at ongoing risk',
            'syphilis_gonorrhea_chlamydia': 'STI screening if sexually active',
            'urine_protein': 'If on tenofovir regimens'
        }
    },
    
    # Extended monitoring (very stable patients)
    'extended_monitoring': {
        'criteria': 'VL suppressed >2 years, CD4 >300 for >2 years',
        'cd4_frequency': 'Can consider stopping CD4 monitoring',
        'vl_frequency': 'Every 6 months minimum'
    }
}

# ============================================================================
# SPECIAL SITUATIONS
# ============================================================================

SPECIAL_MONITORING = {
    'pregnancy': {
        'vl_frequency': 'Monthly until suppressed, then every 3 months',
        'special_tests': ['β-hCG', 'routine prenatal labs'],
        'guideline': 'Follow HHS Perinatal ARV Guidelines'
    },
    
    'virologic_failure': {
        'tests': [
            'Repeat HIV viral load immediately',
            'Drug resistance genotype (if VL >500)',
            'Assess adherence barriers'
        ]
    },
    
    'starting_abacavir': {
        'required': 'HLA-B*5701 MUST be negative',
        'contraindication': 'Never rechallenge if prior hypersensitivity'
    },
    
    'starting_maraviroc': {
        'required': 'Tropism assay showing CCR5-tropic virus only',
        'loinc': 'No standard LOINC - send to specialty lab'
    },
    
    'tenofovir_monitoring': {
        'tests': ['eGFR', 'serum phosphate (if CKD)', 'urine protein'],
        'frequency': 'Every 3-6 months',
        'hold_criteria': 'eGFR <60 mL/min (adjust dose), <30 (avoid TDF)'
    }
}

# ============================================================================
# CLINICAL INTERPRETATION GUIDE
# ============================================================================

VIRAL_LOAD_INTERPRETATION = {
    'undetectable': '<20 copies/mL (goal)',
    'suppressed': '<200 copies/mL (DHHS threshold)',
    'blip': 'Isolated 50-200, then returns to undetectable',
    'low_level_viremia': 'Persistent 50-200 copies/mL',
    'virologic_failure': '>200 copies/mL on two consecutive tests'
}

CD4_THRESHOLDS = {
    '<50': 'MAC prophylaxis indicated',
    '<100': 'Toxoplasmosis prophylaxis if IgG+',
    '<200': 'AIDS diagnosis, PCP prophylaxis indicated',
    '200-350': 'Moderate immunosuppression',
    '>350': 'Generally adequate immune function',
    '>500': 'Normal range'
}

RESISTANCE_TESTING_INDICATIONS = {
    'baseline': 'Before starting ART (all ART-naive patients)',
    'virologic_failure': 'VL >500 while on ART',
    'suboptimal_response': 'VL >200 at 24 weeks despite adherence',
    'pregnancy': 'If not previously tested'
}

# ============================================================================
# USAGE NOTES FROM DHHS GUIDELINES
# ============================================================================

DHHS_GUIDELINE_SUMMARY = """
MONITORING FREQUENCY SUMMARY (DHHS Guidelines):

BEFORE STARTING ART:
✓ HIV viral load, CD4 count, CD4%
✓ Resistance testing (genotype)
✓ HLA-B*5701 (if considering abacavir)
✓ Hepatitis A, B, C screening
✓ Complete blood count
✓ Comprehensive metabolic panel
✓ Fasting lipids
✓ Fasting glucose
✓ Urinalysis
✓ Pregnancy test (women of childbearing age)
✓ STI screening
✓ TB screening
✓ Toxoplasma, CMV serology

AFTER STARTING ART:
• 2-4 weeks: HIV viral load
• Every 4-8 weeks: Repeat VL until suppressed (<50 copies/mL)
• Every 3-6 months: VL, CD4, CBC, chemistries, LFTs
• Annually: Lipids, glucose, STI screening
• With tenofovir: Periodic urinalysis, creatinine/eGFR

CAN REDUCE FREQUENCY IF:
• VL suppressed >1 year → Monitor every 6 months
• VL suppressed >2 years + CD4 >300 for >2 years → Consider stopping CD4 monitoring

CRITICAL REMINDERS:
1. HLA-B*5701 REQUIRED before abacavir (prevents hypersensitivity)
2. Resistance testing REQUIRED before starting ART
3. HBV serology affects ART choice (need drugs active against HBV)
4. Tenofovir requires renal monitoring (eGFR, urinalysis)
5. Some PIs cause dyslipidemia - monitor lipids
6. Pregnancy test before starting ART in women of childbearing age

REFERENCES:
- DHHS Guidelines: https://clinicalinfo.hiv.gov/en/guidelines/
- Last Updated: November 2024
- This reference reflects current standard of care
"""

if __name__ == "__main__":
    print("=" * 80)
    print("COMPLETE HIV/AIDS MEDICATION AND LAB TEST REFERENCE")
    print("Based on DHHS Guidelines (2024)")
    print("=" * 80)
    
    print("\n📋 HIV ANTIRETROVIRAL MEDICATIONS")
    print("-" * 80)
    for key, med in HIV_MEDICATIONS.items():
        print(f"\n{med['name']} (RxNorm: {med['rxnorm']})")
        print(f"  Components: {med['components']}")
        print(f"  Class: {med['class']}")
        print(f"  Frequency: {med['frequency']}")
        if 'notes' in med:
            print(f"  Notes: {med['notes']}")
    
    print("\n\n🔬 BASELINE REQUIRED TESTS (Before Starting ART)")
    print("-" * 80)
    categories = {
        'HIV Monitoring': ['hiv_viral_load', 'cd4_count', 'cd4_percent', 'hiv_resistance_genotype'],
        'Pharmacogenomics': ['hla_b5701'],
        'Hepatitis Screening': ['hep_a_total_ab', 'hep_b_surface_ag', 'hep_b_surface_ab', 'hep_b_core_ab', 'hep_c_antibody'],
        'Hematology': ['cbc_with_diff'],
        'Chemistry': ['bmp', 'creatinine', 'egfr'],
        'Liver Function': ['alt', 'ast', 'bilirubin_total'],
        'Lipids': ['lipid_panel_fasting', 'cholesterol_total', 'hdl', 'ldl', 'triglycerides'],
        'Metabolic': ['glucose_fasting'],
        'Renal': ['urinalysis', 'urine_protein'],
        'Women': ['pregnancy_test'],
        'STI Screening': ['syphilis_rpr', 'gonorrhea_urine', 'chlamydia_urine'],
        'OI Screening': ['toxoplasma_igg', 'cmv_igg', 'tb_igra']
    }
    
    for category, test_keys in categories.items():
        print(f"\n{category}:")
        for key in test_keys:
            if key in BASELINE_REQUIRED_TESTS:
                test = BASELINE_REQUIRED_TESTS[key]
                print(f"  • {test['name']}")
                print(f"    LOINC: {test['loinc']}")
                print(f"    Frequency: {test['frequency']}")
                if 'clinical_significance' in test:
                    print(f"    Clinical: {test['clinical_significance']}")
    
    print("\n\n📅 MONITORING SCHEDULE")
    print("-" * 80)
    for schedule_name, schedule_info in MONITORING_SCHEDULE.items():
        print(f"\n{schedule_name.replace('_', ' ').title()}:")
        print(f"  Timing: {schedule_info.get('timing', schedule_info.get('criteria', 'N/A'))}")
        if 'tests' in schedule_info:
            print("  Tests:")
            for test, reason in schedule_info['tests'].items():
                print(f"    - {test}: {reason}")
    
    print("\n\n" + DHHS_GUIDELINE_SUMMARY)
    
    print("\n" + "=" * 80)
    print("✅ This reference is COMPLETE and aligned with DHHS Guidelines")
    print("=" * 80)
