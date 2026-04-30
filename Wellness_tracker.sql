SELECT current_database();
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE patients (
patient_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
date_of_birth DATE NOT NULL,
phone TEXT,
email TEXT,
status TEXT DEFAULT 'ACTIVE',
created_at TIMESTAMP DEFAULT NOW()
);

SELECT * FROM patients;

CREATE TABLE treatments (
treatment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

patient_id UUID NOT NULL
	REFERENCES patients(patient_id),

treatment_type TEXT NOT NULL, 
drug_name TEXT NOT NULL, 
concentration TEXT,

monthly_fee NUMERIC(10,2),
mandatory_lab_fee NUMERIC (10,2),

autopay_enabled BOOLEAN DEFAULT FALSE, 
active BOOLEAN DEFAULT TRUE, 
notes TEXT,
created_at TIMESTAMP DEFAULT NOW()
);

SELECT * FROM treatments;

CREATE TABLE injections (
injection_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

patient_id UUID NOT NULL
	REFERENCES patients(patient_id),

treatment_id UUID NOT NULL
		REFERENCES treatments(treatment_id),

injection_date DATE NOT NULL,
dose NUMERIC(6,2),
weight NUMERIC(6,2),

labs_required BOOLEAN DEFAULT FALSE,
paid BOOLEAN DEFAULT FALSE,

notes TEXT,
created_at TIMESTAMP DEFAULT NOW()

	
);
SELECT * FROM injections;

CREATE TABLE labs (
lab_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

patient_id UUID NOT NULL
	REFERENCES patients(patient_id),

treatment_id UUID 
	REFERENCES treatments(treatment_id),

lab_type TEXT NOT NULL,
ordered_date DATE NOT NULL,

completed_date DATE,
next_lab_due_date DATE,
mandatory BOOLEAN DEFAULT FALSE,
lab_fee NUMERIC(10,2),
notes TEXT,
created_at TIMESTAMP DEFAULT NOW()

);

SELECT * FROM labs;

SELECT *
FROM patients p
JOIN treatments t ON p.patient_id = t.patient_id
JOIN labs l ON t.treatment_id = l.treatment_id;

SELECT p.patient_id, t.treatment_id
FROM patients p
JOIN treatments t ON p.patient_id = t.patient_id
LIMIT 1;

INSERT INTO patients (
first_name,
last_name,
date_of_birth,
phone,
email
)
VALUES (
'test',
'John Doe',
'1959-01-01',
'123-456-7890',
'test@example.com'
);

INSERT INTO treatments (
patient_id,
treatment_type, 
drug_name,
concentration,
monthly_fee
)

SELECT
	patient_id,
	'Testosterone',
	'Testosterone Cypionate',
	'200 mg/ml',
	165.00
FROM patients
LIMIT 1;

INSERT INTO injections (
	patient_id,
	treatment_id,
	injection_date,
	dose
)
SELECT 
	p.patient_id,
	t.treatment_id,	
	CURRENT_DATE,
	0.50
FROM patients p
JOIN treatments t ON p.patient_id = t.treatment_id
LIMIT 1;

SELECT
	p.first_name,
	p.last_name,
	t.treatment_type,
	i.injection_date,
	i.dose,
	i.paid,
	i.notes
FROM patients p
JOIN treatments t ON p.patient_id = t.patient_id
JOIN injections i ON t.treatment_id = t.treatment_id
ORDER BY i.injection_date DESC;

SELECT * FROM patients;
SELECT * FROM treatments;

