"""
Synthea Population Generator for Ryan White/ADAP Programs
Generates synthetic patient data matching demographic distributions
using the 2023 ADAP and RSR Public Data Reports
"""

import json
import subprocess
import random
from pathlib import Path
from typing import Dict, List
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

# Demographics based on 2023 ADAP Data Report
ADAP_DEMOGRAPHICS = {
    'age_distribution': {
        '<13': 0.001,
        '13-14': 0.0001,
        '15-19': 0.009,
        '20-24': 0.080,
        '25-29': 0.160,
        '30-34': 0.189,
        '35-39': 0.144,
        '40-44': 0.105,
        '45-49': 0.081,
        '50-54': 0.069,
        '55-59': 0.061,
        '60-64': 0.048,
        '>=65': 0.051
    },
    'race_ethnicity': {
        'black': 0.380,
        'hispanic': 0.307,
        'white': 0.282,
        'asian': 0.019,
        'native': 0.005,
        'other': 0.007
    },
    'sex': {
        'M': 0.797,
        'F': 0.203
    },
    'poverty_level': {
        '0-100': 0.596,
        '101-138': 0.100,
        '139-250': 0.181,
        '251-400': 0.096,
        '>400': 0.027
    }
}

# HIV-related RxNorm codes (common ARV medications)
HIV_MEDICATIONS = {
    'biktarvy': '2120107',  # Biktarvy (bictegravir/emtricitabine/tenofovir alafenamide)
    'descovy': '1721603',   # Descovy (emtricitabine/tenofovir alafenamide)
    'genvoya': '1721606',   # Genvoya (elvitegravir/cobicistat/emtricitabine/tenofovir)
    'triumeq': '1546773',   # Triumeq (dolutegravir/abacavir/lamivudine)
    'dovato': '2183126',    # Dovato (dolutegravir/lamivudine)
    'biktarvy_generic': '2120108'
}

# LOINC codes for required lab tests
REQUIRED_LOINC_CODES = {
    # HIV Tests
    'hiv_viral_load': '20447-9',
    'hiv_antibody': '29893-5',
    'cd4_count': '24467-3',
    'cd4_percent': '32518-1',
    
    # Hepatitis B
    'hep_b_surface_ag': '5196-1',
    'hep_b_surface_ab': '16935-9',
    'hep_b_core_ab': '13952-0',
    
    # Hepatitis C
    'hep_c_antibody': '16128-1',
    'hep_c_rna': '11259-1',
    
    # Lipid Panel
    'cholesterol_total': '2093-3',
    'hdl': '2085-9',
    'ldl': '13457-7',
    'triglycerides': '2571-8',
    
    # Colposcopy (procedure code, not LOINC)
    'colposcopy_findings': '57454-9'
}


class SyntheaPopulationGenerator:
    """Generates synthetic patient populations using Synthea"""
    
    def __init__(self,
                 synthea_jar_path: str,
                 output_dir: str = None,
                 population_size: int = 1000):
        self.synthea_jar_path = Path(synthea_jar_path)
        if output_dir is None:
            output_dir = os.getenv('PROCESSED_FHIR_DIR', './output')
        self.output_dir = Path(output_dir)
        self.population_size = population_size
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
    def create_demographics_file(self) -> Path:
        """Create Synthea demographics configuration file"""
        
        # Convert age ranges to birth year ranges (assuming current year 2023)
        current_year = 2023
        
        demographics_config = {
            "generate": {
                "demographics": {
                    "default_file": "geography/demographics.csv",
                    "append_mode": False
                },
                "population": self.population_size,
                "append_mode": False
            }
        }
        
        config_path = self.output_dir / "synthea_config.json"
        with open(config_path, 'w') as f:
            json.dump(demographics_config, f, indent=2)
            
        return config_path
    
    def create_custom_demographics_csv(self) -> Path:
        """Create custom demographics CSV for Synthea"""
        
        csv_path = self.output_dir / "custom_demographics.csv"
        
        # Create weighted population distribution
        lines = ["COUNTY,NPOPUL,RATEWHT,RATEBLK,RATEASN,RATENATIVE,RATEOTHER,RATEHSP,RATEM,RATEF\n"]
        
        # Single aggregate row matching ADAP demographics
        demo = ADAP_DEMOGRAPHICS
        line = (
            f"CustomCounty,{self.population_size},"
            f"{demo['race_ethnicity']['white']},"
            f"{demo['race_ethnicity']['black']},"
            f"{demo['race_ethnicity']['asian']},"
            f"{demo['race_ethnicity']['native']},"
            f"{demo['race_ethnicity']['other']},"
            f"{demo['race_ethnicity']['hispanic']},"
            f"{demo['sex']['M']},"
            f"{demo['sex']['F']}\n"
        )
        lines.append(line)
        
        with open(csv_path, 'w') as f:
            f.writelines(lines)
            
        return csv_path
    
    def generate_age_range_file(self) -> Path:
        """Generate age range configuration for Synthea"""
        
        age_config = []
        age_dist = ADAP_DEMOGRAPHICS['age_distribution']
        
        # Convert to birth year ranges
        current_year = 2023
        age_ranges = {
            '<13': (2011, 2023),
            '13-14': (2009, 2010),
            '15-19': (2004, 2008),
            '20-24': (1999, 2003),
            '25-29': (1994, 1998),
            '30-34': (1989, 1993),
            '35-39': (1984, 1988),
            '40-44': (1979, 1983),
            '45-49': (1974, 1978),
            '50-54': (1969, 1973),
            '55-59': (1964, 1968),
            '60-64': (1959, 1963),
            '>=65': (1900, 1958)
        }
        
        for age_group, weight in age_dist.items():
            birth_start, birth_end = age_ranges[age_group]
            age_config.append({
                'min_birth_year': birth_start,
                'max_birth_year': birth_end,
                'weight': weight
            })
        
        config_path = self.output_dir / "age_distribution.json"
        with open(config_path, 'w') as f:
            json.dump(age_config, f, indent=2)
            
        return config_path
    
    def run_synthea(self, state: str = "Massachusetts", city: str = "Boston") -> Path:
        """Execute Synthea to generate population"""
        
        demographics_csv = self.create_custom_demographics_csv()
        
        cmd = [
            "java",
            "-jar", str(self.synthea_jar_path),
            "-p", str(self.population_size),
            "--exporter.fhir.export", "true",
            "--exporter.csv.export", "false",
            "--exporter.ccda.export", "false",
            f"--exporter.baseDirectory={self.output_dir}",
            state,
            city
        ]
        
        print(f"Running Synthea: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Synthea Error: {result.stderr}")
            raise RuntimeError(f"Synthea execution failed: {result.stderr}")
        
        print(f"Synthea completed successfully")
        return self.output_dir / "fhir"
    
    def get_generated_patients(self) -> List[Path]:
        """Get list of generated patient FHIR files"""
        fhir_dir = self.output_dir / "fhir"
        if not fhir_dir.exists():
            return []
        return list(fhir_dir.glob("*.json"))


def main():
    """Main execution"""
    
    generator = SyntheaPopulationGenerator(
        synthea_jar_path="./synthea-with-dependencies.jar",
        output_dir=os.getenv('PROCESSED_FHIR_DIR', './output_fhir'),
        population_size=1000
    )
    
    print("Creating demographic configuration...")
    generator.create_demographics_file()
    generator.create_custom_demographics_csv()
    generator.generate_age_range_file()
    
    print(f"Generating {generator.population_size} synthetic patients...")
    fhir_output = generator.run_synthea()
    
    patients = generator.get_generated_patients()
    print(f"Generated {len(patients)} patient records in {fhir_output}")
    
    print("\nNext steps:")
    print("1. Run post_process_fhir.py to add HIV medications and labs")
    print("2. Run fhir_uploader.py to upload to FHIR server")


if __name__ == "__main__":
    main()
