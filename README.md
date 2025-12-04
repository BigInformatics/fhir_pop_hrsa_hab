# Synthea Population Generator for Ryan White/ADAP Programs

## Usage

Download Synthea.  You will need java installed.

```
wget https://github.com/synthetichealth/synthea/releases/download/v3.2.0/synthea-with-dependencies.jar
```

Install libraries and prepare synthetic records

```
pip install -r requirements.txt
python population_generator.py
python post_process.py
```

Obtain the [FHIR Uploader](https://github.com/BigInformatics/fhir_uploader) and execute:

```
pip install -r requirements.txt
python fhir_uploader.py
```

## Scripts

### 1. **population_generator.py** - Generates base population with correct demographics

- Configures age, race/ethnicity, sex distributions matching 2023 ADAP data
- Runs Synthea JAR to create FHIR bundles
- Default: 1,000 patients (configurable)


### 2. **post_process.py** - Adds HIV medications and lab results

- Adds HIV antiretroviral medications (RxNorm codes) to ~50% of patients
- Generates realistic HIV viral load, CD4 counts (LOINC codes)
- Adds Hepatitis B/C and lipid panel results
- 85% of ADAP patients have suppressed viral loads (<20 copies/mL)


### 3. **[fhir_uploader.py](https://github.com/BigInformatics/fhir_uploader)** - Uploads to FHIR server (Separate Project)

- Handles Service Token Access authentication
- Automatic retry logic
- Progress tracking and statistics
- Rate limiting protection

### 4. **medications_and_labs.py** - Comprehensive reference

- All HIV medication RxNorm codes with descriptions
- All LOINC codes for HIV, Hepatitis, lipids, STI screening
- Clinical interpretation guidance
- Usage notes and monitoring frequencies


## Customization

### Change Population Size

Edit `synthea_population_generator.py`:
```python
population_size=5000  # Generate 5,000 patients instead of 1,000
```

### Adjust ADAP Percentage

Edit `post_process_fhir.py`:
```python
adap_percentage=0.7  # 70% of patients in ADAP program
```

### Modify Demographics

Edit `ADAP_DEMOGRAPHICS` dictionary in `synthea_population_generator.py`:
```python
'race_ethnicity': {
    'black': 0.450,      # Increase to 45%
    'hispanic': 0.300,   # Keep at 30%
    'white': 0.250,      # Reduce to 25%
    # ...
}
```


## Tip

**Generate in Batches:** For large populations (10,000+), generate in batches of 1,000
 ```bash
 for i in {1..10}; do
     python synthea_population_generator.py
     python post_process_fhir.py
     python fhir_uploader.py
 done
 ```
