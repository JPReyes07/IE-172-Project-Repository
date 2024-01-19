-- Insert data into the medical_secretary table
INSERT INTO medical_secretary (MDSC_M, MDSC_PASS) VALUES
('Rose', 'rose123'),
('Cha', 'cha456');

-- Insert data into the service table
INSERT INTO service (SRVC_M) VALUES
('Wellness Check-up'),
('Preventive Medicine'),
('Prenatal Pregnancy Care'),
('Postnatal Pregnancy Care');

-- Insert data into the patient table
INSERT INTO patient (PTT_FM, PTT_LM, PTT_BRTH, PTT_ADDR_STRT, PTT_ADDR_BRGY, PTT_ADDR_PROV, PTT_CTNB, PTT_CVST, PTT_EMC_M, PTT_EMC_RLN, PTT_EMC_CTNB, PTT_MED_HIST)
VALUES
('Maria', 'Santos', '1980-05-15', '123 Main St', 'Brgy. San Juan', 'Metro Manila', 123456789, 'Single', 'Juan Santos', 'Spouse', 987654321, 'No significant medical history'),
('Lorna', 'Garcia', '1992-12-08', '456 Oak St', 'Brgy. Bagong Ilog', 'Metro Manila', 987654321, 'Singlw', 'Dain Garcia', 'Sister', 876543210, 'Asthma during childhood'),
('Lea', 'Torres', '1985-09-20', '789 Pine St', 'Brgy. Malate', 'Manila', 876543210, 'Married', 'Zeke Abella', 'Mother', 765432109, 'Hypertension, under medication'),
('Elena', 'Villanueva', '1998-03-02', '101 Palm St', 'Brgy. Quezon City', 'Metro Manila', 765432109, 'Single', 'Pat Villa', 'Daughter', 654321098, 'No significant medical history'),
('Carmen', 'Reyes', '1970-07-12', '202 Bamboo St', 'Brgy. Makati', 'Metro Manila', 654321098, 'Married', 'Jon Reyes', 'Spouse', 543210987, 'Diabetes, controlled by diet');

-- Insert data into the patient_visit table
INSERT INTO patient_visit (VISIT_D_NOW, VISIT_D_PREV, VISIT_HR, VISIT_BP_SYS, VISIT_BP_DIA, VISIT_WGHT, VISIT_TMP, VISIT_Q, VISIT_DGNS, SRVC_ID, PTT_ID, MDSC_ID)
VALUES
('2024-01-15', '2023-12-01', 75, 120, 80, 65.5, 98.6, 'COMPLETED', 'Routine check-up. Patient in good health.', 1, 1, 1),
('2024-01-10', '2023-11-20', 80, 130, 85, 70.2, 99.0, 'COMPLETED', 'Monitoring preventive measures. Patient advised on lifestyle changes.', 2, 2, 2),
('2024-01-05', '2023-10-15', 78, 125, 82, 68.9, 98.8, 'COMPLETED', 'Routine prenatal care. Mother and baby are doing well.', 3, 3, 1),
('2024-01-02', '2023-09-25', 76, 122, 79, 67.3, 98.5, 'COMPLETED', 'Postnatal check-up. Mother and baby are healthy and thriving.', 4, 4, 2),
('2023-12-28', '2023-08-30', 85, 135, 88, 72.5, 99.2, 'COMPLETED', 'Routine check-up. Patient with well-controlled hypertension.', 1, 5, 1);

-- Insert data into the payment table
INSERT INTO payment (PYM_MDE, PYM_SP, VISIT_ID)
VALUES
('Cash', 500, 1),
('Cash', 800, 2),
('Cash', 500, 3),
('Cash', 500, 4),
('Cash', 600, 5);

-- Insert data into the medicine table
INSERT INTO medicine (MED_M, MED_COUNT, MED_MP)
VALUES
('Paracetamol', 50, 10),
('Amoxicillin', 30, 15),
('Lisinopril', 20, 5),
('Salbutamol', 40, 8),
('Metformin', 25, 12);

-- Insert data into the medicine_payment table
INSERT INTO medicine_payment (MED_PYM_Q, PYM_ID, MED_ID)
VALUES
(2, 1, 1),
(1, 2, 2),
(3, 3, 3),
(2, 4, 4),
(1, 5, 5);

DELETE FROM patient_visit;
ALTER SEQUENCE patient_visit_visit_id_seq RESTART WITH 1;

SELECT * FROM patient_visit


