INSERT INTO service (SRVC_M) VALUES
('Wellness Check-up'),
('Preventive Medicine'),
('Prenatal Pregnancy Care'),
('Postnatal Pregnancy Care');

INSERT INTO patient (PTT_FM, PTT_LM, PTT_BRTH, PTT_ADDR_STRT, PTT_ADDR_BRGY, PTT_ADDR_PROV, PTT_CTNB, PTT_CVST, PTT_EMC_M, PTT_EMC_RLN, PTT_EMC_CTNB, PTT_MED_HIST)
VALUES
('Maria', 'Santos', '1980-05-15', '123 Main Street', 'Barangay Uno', 'Metro Manila', '09123456789', 'Married', 'Juan Santos', 'Husband', 09187654321, 'No significant medical history'),
('Anna', 'Reyes', '1992-02-20', '456 Oak Avenue', 'Barangay Dos', 'Cebu', '09876543210', 'Single', 'Jose Reyes', 'Father', 09876543210, 'No significant medical history'),
('Luisa', 'Gonzales', '1975-09-10', '789 Pine Street', 'Barangay Tres', 'Davao', '08765432109', 'Widowed', 'Rosa Gonzales', 'Sister', 08765432109, 'Hypertension and diabetes'),
('Elena', 'Lopez', '1988-11-25', '101 Palm Drive', 'Barangay Cuatro', 'Manila', '09567890123', 'Married', 'Juan Lopez', 'Husband', 09567890123, 'Asthma and allergies');

INSERT INTO medical_secretary (MDSC_M, MDSC_PASS) VALUES
('Secretary1', 'secret1pass'),
('Secretary2', 'secret2pass'),
('Secretary3', 'secret3pass');

INSERT INTO patient_visit (VISIT_D_NOW, VISIT_D_PREV, VISIT_HR, VISIT_BP_SYS, VISIT_BP_DIA, VISIT_WGHT, VISIT_TMP, VISIT_Q, VISIT_DGNS, SRVC_ID, PTT_ID, MDSC_ID)
VALUES
('2024-01-20', '2024-01-10', 14, 120, 80, 65.5, 37.0, 'COMPLETED', 'Routine check-up', 1, 1, 1),
('2024-01-21', '2024-01-15', 15, 118, 78, 62.0, 36.5, 'COMPLETED', 'General health assessment', 2, 2, 2),
('2024-01-22', '2024-01-18', 16, 130, 85, 70.2, 37.2, 'COMPLETED', 'Prenatal check-up', 3, 3, 3),
('2024-01-23', '2024-01-20', 17, 122, 82, 68.0, 36.8, 'COMPLETED', 'Postnatal follow-up', 4, 4, 1);

INSERT INTO payment (PYM_MDE, PYM_SP, VISIT_ID)
VALUES
('Cash', 500, 1),
('Cash', 750, 2),
('Cash', 1000, 3),
('Cash', 600, 4);

INSERT INTO medicine (MED_M, MED_COST, MED_MP, MED_COUNT, MED_ROP)
VALUES
('Paracetamol', 50, 80, 100, 20),
('Lisinopril', 120, 180, 50, 10),
('Salbutamol', 70, 100, 80, 15),
('Metformin', 90, 150, 60, 12);

INSERT INTO medicine_payment (MED_PYM_Q, PYM_ID, MED_ID)
VALUES
(2, 1, 1),
(1, 2, 2),
(3, 3, 3),
(2, 4, 4);
