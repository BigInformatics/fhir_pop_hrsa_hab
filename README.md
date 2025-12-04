# Synthea Population Generator for Ryan White/ADAP Programs


1. **population_generator.py** - Generates base population with correct demographics

- Configures age, race/ethnicity, sex distributions matching 2023 ADAP data
- Runs Synthea JAR to create FHIR bundles
- Default: 1,000 patients (configurable)


2. **post_process.py** - Adds HIV medications and lab results

- Adds HIV antiretroviral medications (RxNorm codes) to ~50% of patients
- Generates realistic HIV viral load, CD4 counts (LOINC codes)
- Adds Hepatitis B/C and lipid panel results
- 85% of ADAP patients have suppressed viral loads (<20 copies/mL)


3. **[fhir_uploader.py](https://github.com/BigInformatics/fhir_uploader)** - Uploads to FHIR server (Separate Project)

- Handles Service Token Access authentication
- Automatic retry logic
- Progress tracking and statistics
- Rate limiting protection
