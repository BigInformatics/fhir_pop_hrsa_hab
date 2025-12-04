"""
FHIR Post-Processor for Ryan White/ADAP Patients
Adds HIV medications and comprehensive lab results aligned with DHHS Guidelines
Includes all baseline and monitoring tests per DHHS recommendations
TODO: Need to link back into main list.
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid


# HIV Medication RxNorm codes (same as before)
HIV_MEDICATIONS = {
    'biktarvy': '2120107',
    'triumeq': '1546773',
    'dovato': '2183126',
    'descovy': '1721603',
    'genvoya': '1721606',
    'cabenuva': '2471641',
    'truvada': '617296',
    'atripla': '722971'
}

# COMPLETE LOINC panel aligned with DHHS Guidelines
COMPLETE_HIV_LABS = {
    # Core HIV Monitoring
    'hiv_viral_load': {
        'loinc': '20447-9',
        'display': 'HIV 1 RNA [#/volume] in Serum or Plasma by NAA with probe detection',
        'unit': 'copies/mL',
        'ranges': {'undetectable': (0, 20), 'suppressed': (20, 200), 'detectable': (200, 100000)},
        'frequency': 'baseline_and_monitoring'
    },
    'cd4_count': {
        'loinc': '24467-3',
        'display': 'CD3+CD4+ (T4 helper) cells [#/volume] in Blood',
        'unit': 'cells/uL',
        'ranges': {'low': (200, 350), 'normal': (350, 1500)},
        'frequency': 'baseline_and_monitoring'
    },
    'cd4_percent': {
        'loinc': '32518-1',
        'display': 'CD3+CD4+ cells/100 cells in Blood',
        'unit': '%',
        'ranges': {'low': (14, 25), 'normal': (25, 60)},
        'frequency': 'baseline_and_monitoring'
    },
    
    # Hepatitis Panel
    'hep_b_surface_ag': {
        'loinc': '5196-1',
        'display': 'Hepatitis B virus surface Ag [Presence] in Serum',
        'result_type': 'qualitative',
        'values': ['negative', 'positive'],
        'distribution': [0.90, 0.10],  # 10% HBV coinfection
        'frequency': 'baseline'
    },
    'hep_b_surface_ab': {
        'loinc': '16935-9',
        'display': 'Hepatitis B virus surface Ab [Units/volume] in Serum',
        'unit': 'mIU/mL',
        'ranges': {'immune': (10, 100), 'non_immune': (0, 10)},
        'frequency': 'baseline'
    },
    'hep_b_core_ab': {
        'loinc': '13952-0',
        'display': 'Hepatitis B virus core Ab [Presence] in Serum',
        'result_type': 'qualitative',
        'values': ['negative', 'positive'],
        'distribution': [0.85, 0.15],
        'frequency': 'baseline'
    },
    'hep_c_antibody': {
        'loinc': '16128-1',
        'display': 'Hepatitis C virus Ab [Presence] in Serum',
        'result_type': 'qualitative',
        'values': ['negative', 'positive'],
        'distribution': [0.85, 0.15],  # 15% HCV coinfection
        'frequency': 'baseline'
    },
    'hep_c_rna': {
        'loinc': '11259-1',
        'display': 'Hepatitis C virus RNA [Units/volume] in Serum or Plasma by NAA',
        'unit': 'IU/mL',
        'ranges': {'undetectable': (0, 15), 'detectable': (15, 1000000)},
        'frequency': 'if_hcv_positive'
    },
    'hep_a_total_ab': {
        'loinc': '20575-7',
        'display': 'Hepatitis A virus Ab [Presence] in Serum',
        'result_type': 'qualitative',
        'values': ['negative', 'positive'],
        'distribution': [0.40, 0.60],  # Many vaccinated or prior exposure
        'frequency': 'baseline'
    },
    
    # Chemistry Panel
    'creatinine': {
        'loinc': '2160-0',
        'display': 'Creatinine [Mass/volume] in Serum or Plasma',
        'unit': 'mg/dL',
        'ranges': {'normal': (0.6, 1.2), 'elevated': (1.2, 2.0)},
        'frequency': 'baseline_and_monitoring'
    },
    'egfr': {
        'loinc': '48643-1',
        'display': 'Glomerular filtration rate/1.73 sq M.predicted by Creatinine',
        'unit': 'mL/min/1.73m2',
        'ranges': {'normal': (60, 120), 'reduced': (30, 60)},
        'frequency': 'baseline_and_monitoring'
    },
    'alt': {
        'loinc': '1742-6',
        'display': 'Alanine aminotransferase [Enzymatic activity/volume] in Serum or Plasma',
        'unit': 'U/L',
        'ranges': {'normal': (7, 40), 'elevated': (40, 120)},
        'frequency': 'baseline_and_monitoring'
    },
    'ast': {
        'loinc': '1920-8',
        'display': 'Aspartate aminotransferase [Enzymatic activity/volume] in Serum or Plasma',
        'unit': 'U/L',
        'ranges': {'normal': (10, 35), 'elevated': (35, 120)},
        'frequency': 'baseline_and_monitoring'
    },
    
    # Lipid Panel
    'cholesterol_total': {
        'loinc': '2093-3',
        'display': 'Cholesterol [Mass/volume] in Serum or Plasma',
        'unit': 'mg/dL',
        'ranges': {'normal': (150, 200), 'high': (200, 240)},
        'frequency': 'baseline_and_annual'
    },
    'hdl': {
        'loinc': '2085-9',
        'display': 'HDL Cholesterol [Mass/volume] in Serum or Plasma',
        'unit': 'mg/dL',
        'ranges': {'normal': (40, 60)},
        'frequency': 'baseline_and_annual'
    },
    'ldl': {
        'loinc': '13457-7',
        'display': 'LDL Cholesterol [Mass/volume] in Serum or Plasma by calculation',
        'unit': 'mg/dL',
        'ranges': {'normal': (70, 130)},
        'frequency': 'baseline_and_annual'
    },
    'triglycerides': {
        'loinc': '2571-8',
        'display': 'Triglyceride [Mass/volume] in Serum or Plasma',
        'unit': 'mg/dL',
        'ranges': {'normal': (50, 150), 'elevated': (150, 300)},
        'frequency': 'baseline_and_annual'
    },
    
    # Glucose/Diabetes
    'glucose_fasting': {
        'loinc': '1558-6',
        'display': 'Fasting glucose [Mass/volume] in Serum or Plasma',
        'unit': 'mg/dL',
        'ranges': {'normal': (70, 100), 'prediabetic': (100, 125), 'diabetic': (126, 200)},
        'frequency': 'baseline_and_annual'
    },
    
    # STI Screening
    'syphilis_rpr': {
        'loinc': '20507-0',
        'display': 'Reagin Ab [Presence] in Serum by RPR',
        'result_type': 'qualitative',
        'values': ['nonreactive', 'reactive'],
        'distribution': [0.95, 0.05],  # 5% prevalence
        'frequency': 'baseline_and_annual'
    }
}

# Additional baseline-only tests
BASELINE_ONLY_TESTS = {
    'hla_b5701': {
        'loinc': '13303-3',
        'display': 'HLA-B*57:01 [Presence]',
        'result_type': 'qualitative',
        'values': ['negative', 'positive'],
        'distribution': [0.95, 0.05],  # ~5% positive in general population
        'notes': 'REQUIRED before abacavir'
    },
    'toxoplasma_igg': {
        'loinc': '22570-6',
        'display': 'Toxoplasma gondii IgG Ab [Presence] in Serum',
        'result_type': 'qualitative',
        'values': ['negative', 'positive'],
        'distribution': [0.70, 0.30],  # ~30% seropositive
        'notes': 'Baseline OI screening'
    },
    'cmv_igg': {
        'loinc': '22244-8',
        'display': 'Cytomegalovirus IgG Ab [Presence] in Serum',
        'result_type': 'qualitative',
        'values': ['negative', 'positive'],
        'distribution': [0.40, 0.60],  # ~60% seropositive in US
        'notes': 'Baseline OI screening'
    },
    'tb_igra': {
        'loinc': '38372-3',
        'display': 'Mycobacterium tuberculosis stimulated gamma interferon [Presence] in Blood',
        'result_type': 'qualitative',
        'values': ['negative', 'positive', 'indeterminate'],
        'distribution': [0.92, 0.05, 0.03],  # ~5% LTBI prevalence
        'notes': 'Baseline TB screening'
    }
}


class FHIRPostProcessor:
    """Add comprehensive HIV-related medications and lab results to FHIR bundles"""
    
    def __init__(self, input_dir: str, output_dir: str, adap_percentage: float = 0.5):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.adap_percentage = adap_percentage
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
    def generate_medication_statement(self, 
                                     patient_ref: str,
                                     rx_code: str,
                                     medication_name: str,
                                     start_date: str) -> Dict:
        """Create FHIR MedicationStatement resource"""
        return {
            "resourceType": "MedicationStatement",
            "id": str(uuid.uuid4()),
            "status": "active",
            "medicationCodeableConcept": {
                "coding": [{
                    "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                    "code": rx_code,
                    "display": medication_name
                }]
            },
            "subject": {"reference": patient_ref},
            "effectivePeriod": {"start": start_date},
            "dateAsserted": start_date
        }
    
    def generate_observation_quantitative(self,
                                         patient_ref: str,
                                         loinc_code: str,
                                         display: str,
                                         value: float,
                                         unit: str,
                                         date: str) -> Dict:
        """Create quantitative FHIR Observation resource"""
        return {
            "resourceType": "Observation",
            "id": str(uuid.uuid4()),
            "status": "final",
            "category": [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "laboratory",
                    "display": "Laboratory"
                }]
            }],
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": loinc_code,
                    "display": display
                }]
            },
            "subject": {"reference": patient_ref},
            "effectiveDateTime": date,
            "issued": date,
            "valueQuantity": {
                "value": value,
                "unit": unit,
                "system": "http://unitsofmeasure.org",
                "code": unit
            }
        }
    
    def generate_observation_qualitative(self,
                                        patient_ref: str,
                                        loinc_code: str,
                                        display: str,
                                        value: str,
                                        date: str) -> Dict:
        """Create qualitative FHIR Observation resource"""
        return {
            "resourceType": "Observation",
            "id": str(uuid.uuid4()),
            "status": "final",
            "category": [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "laboratory",
                    "display": "Laboratory"
                }]
            }],
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": loinc_code,
                    "display": display
                }]
            },
            "subject": {"reference": patient_ref},
            "effectiveDateTime": date,
            "issued": date,
            "valueString": value
        }
    
    def generate_complete_lab_panel(self, patient_ref: str, base_date: datetime) -> List[Dict]:
        """Generate complete lab panel per DHHS guidelines"""
        observations = []
        
        # Determine viral suppression status (85% undetectable per ADAP outcomes)
        vl_status = random.choices(
            ['undetectable', 'suppressed', 'detectable'],
            weights=[0.85, 0.10, 0.05]
        )[0]
        
        # HIV Core Monitoring Labs
        for test_name, test_info in COMPLETE_HIV_LABS.items():
            if test_info.get('result_type') == 'qualitative':
                # Qualitative test
                value = random.choices(
                    test_info['values'],
                    weights=test_info.get('distribution', [1.0/len(test_info['values'])] * len(test_info['values']))
                )[0]
                
                obs = self.generate_observation_qualitative(
                    patient_ref,
                    test_info['loinc'],
                    test_info['display'],
                    value,
                    base_date.isoformat()
                )
                observations.append(obs)
                
                # If HCV positive, add HCV RNA
                if test_name == 'hep_c_antibody' and value == 'positive':
                    hcv_rna = COMPLETE_HIV_LABS['hep_c_rna']
                    hcv_value = random.uniform(*hcv_rna['ranges']['detectable'])
                    obs_rna = self.generate_observation_quantitative(
                        patient_ref,
                        hcv_rna['loinc'],
                        hcv_rna['display'],
                        hcv_value,
                        hcv_rna['unit'],
                        base_date.isoformat()
                    )
                    observations.append(obs_rna)
                    
            else:
                # Quantitative test
                # Special handling for HIV VL and CD4 correlation
                if test_name == 'hiv_viral_load':
                    vl_range = test_info['ranges'][vl_status]
                    value = random.uniform(*vl_range)
                elif test_name in ['cd4_count', 'cd4_percent']:
                    # Correlate with VL status
                    cd4_status = 'normal' if vl_status == 'undetectable' else random.choice(['low', 'normal'])
                    value = random.uniform(*test_info['ranges'][cd4_status])
                else:
                    # Random normal or abnormal
                    range_choice = random.choice(list(test_info['ranges'].keys()))
                    value = random.uniform(*test_info['ranges'][range_choice])
                
                obs = self.generate_observation_quantitative(
                    patient_ref,
                    test_info['loinc'],
                    test_info['display'],
                    round(value, 2),
                    test_info['unit'],
                    base_date.isoformat()
                )
                observations.append(obs)
        
        # Add baseline-only tests
        for test_name, test_info in BASELINE_ONLY_TESTS.items():
            value = random.choices(
                test_info['values'],
                weights=test_info.get('distribution', [1.0/len(test_info['values'])] * len(test_info['values']))
            )[0]
            
            obs = self.generate_observation_qualitative(
                patient_ref,
                test_info['loinc'],
                test_info['display'],
                value,
                base_date.isoformat()
            )
            observations.append(obs)
        
        return observations
    
    def process_patient_bundle(self, bundle_path: Path) -> Dict:
        """Process a patient bundle and add HIV-related data"""
        with open(bundle_path, 'r') as f:
            bundle = json.load(f)
        
        # Determine if this patient is in ADAP
        is_adap = random.random() < self.adap_percentage
        
        if not is_adap:
            return bundle
        
        # Find patient resource
        patient_resource = None
        patient_ref = None
        for entry in bundle.get('entry', []):
            if entry['resource']['resourceType'] == 'Patient':
                patient_resource = entry['resource']
                patient_ref = f"Patient/{patient_resource['id']}"
                break
        
        if not patient_resource:
            return bundle
        
        # Generate dates
        base_date = datetime.now() - timedelta(days=random.randint(0, 180))  # Recent labs
        med_start_date = datetime.now() - timedelta(days=random.randint(365, 1825))  # 1-5 years on ART
        
        # Add HIV medications (1-2 per patient)
        num_meds = random.choice([1, 2])
        selected_meds = random.sample(list(HIV_MEDICATIONS.items()), num_meds)
        
        for med_name, rx_code in selected_meds:
            med_statement = self.generate_medication_statement(
                patient_ref,
                rx_code,
                med_name,
                med_start_date.isoformat()
            )
            bundle['entry'].append({
                'fullUrl': f"urn:uuid:{med_statement['id']}",
                'resource': med_statement
            })
        
        # Add complete lab panel
        lab_observations = self.generate_complete_lab_panel(patient_ref, base_date)
        for obs in lab_observations:
            bundle['entry'].append({
                'fullUrl': f"urn:uuid:{obs['id']}",
                'resource': obs
            })
        
        return bundle
    
    def process_all_bundles(self):
        """Process all FHIR bundles in input directory"""
        bundle_files = list(self.input_dir.glob("*.json"))
        print(f"Processing {len(bundle_files)} patient bundles...")
        
        adap_count = 0
        total_meds = 0
        total_labs = 0
        
        for bundle_file in bundle_files:
            processed_bundle = self.process_patient_bundle(bundle_file)
            
            # Count resources added
            has_meds = any(
                entry['resource'].get('resourceType') == 'MedicationStatement'
                for entry in processed_bundle.get('entry', [])
            )
            if has_meds:
                adap_count += 1
            
            med_count = sum(
                1 for entry in processed_bundle.get('entry', [])
                if entry['resource'].get('resourceType') == 'MedicationStatement'
            )
            lab_count = sum(
                1 for entry in processed_bundle.get('entry', [])
                if entry['resource'].get('resourceType') == 'Observation'
            )
            
            total_meds += med_count
            total_labs += lab_count
            
            output_file = self.output_dir / bundle_file.name
            with open(output_file, 'w') as f:
                json.dump(processed_bundle, f, indent=2)
        
        print(f"\n✅ Processed {len(bundle_files)} bundles")
        print(f"   ADAP patients: {adap_count} ({adap_count/len(bundle_files)*100:.1f}%)")
        print(f"   Total medications added: {total_meds}")
        print(f"   Total lab observations added: {total_labs}")
        print(f"   Average labs per ADAP patient: {total_labs/adap_count:.0f}")
        print(f"\n📁 Output saved to: {self.output_dir}")


def main():
    """Main execution"""
    processor = FHIRPostProcessor(
        input_dir="./synthea_output/fhir",
        output_dir="./processed_fhir",
        adap_percentage=0.5  # 50% of patients in ADAP program
    )
    
    processor.process_all_bundles()


if __name__ == "__main__":
    main()
