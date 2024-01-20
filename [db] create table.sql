CREATE TABLE patient (
    PTT_ID serial NOT NULL,
    PTT_FM varchar(32), 
    PTT_LM varchar(32), 
    PTT_BRTH date,
    PTT_ADDR_STRT varchar(128),
	PTT_ADDR_BRGY varchar(128),
	PTT_ADDR_PROV varchar(128),
    PTT_CTNB varchar(11),
    PTT_CVST varchar(20),
	PTT_EMC_M varchar(64),
	PTT_EMC_RLN varchar(32),
	PTT_EMC_CTNB integer,
    PTT_MED_HIST varchar(2000),
    PTT_DEL_IND bool DEFAULT FALSE,
    PRIMARY KEY (PTT_ID)
);

CREATE TABLE medical_secretary (
    MDSC_ID serial,
    MDSC_M varchar(32),
    MDSC_PASS varchar(64) not null,
    MDSC_MOD_ON timestamp without time zone default now(),
    MDSC_DEL_IND bool DEFAULT FALSE,
    PRIMARY KEY (MDSC_ID)
);

CREATE TABLE service (
    SRVC_ID serial,
    SRVC_M varchar(32),
    SRVC_DEL_IND bool DEFAULT FALSE,
    PRIMARY KEY (SRVC_ID)
);


CREATE TABLE patient_visit (
    VISIT_ID serial NOT NULL,
    VISIT_D_NOW date,
	VISIT_D_PREV date,
    VISIT_HR integer,
    VISIT_BP_SYS integer,
    VISIT_BP_DIA integer,
    VISIT_WGHT numeric,
    VISIT_TMP numeric,
	VISIT_Q varchar(32) DEFAULT 'NO-SHOW',
    VISIT_DGNS varchar(4000),
	SRVC_ID integer REFERENCES service(SRVC_ID),
    PTT_ID integer REFERENCES patient(PTT_ID),
    MDSC_ID integer REFERENCES medical_secretary(MDSC_ID),
    VISIT_DEL_IND bool DEFAULT FALSE,
    PRIMARY KEY (VISIT_ID)
);

CREATE TABLE payment (
    PYM_ID serial NOT NULL,
    PYM_MDE varchar(32),
	PYM_SP integer,
    PYM_DEL_IND bool DEFAULT FALSE,
	VISIT_ID integer REFERENCES patient_visit(VISIT_ID), 
    PRIMARY KEY (PYM_ID)
);

CREATE TABLE medicine (
    MED_ID serial NOT NULL,
    MED_M varchar(64),
    MED_COST integer,
	MED_COUNT integer, 
    MED_ROP integer,
	MED_MP integer,
    MED_COUNT_LAST_UPD timestamp without time zone DEFAULT NOW(),
    MED_DEL_IND bool DEFAULT FALSE,
    PRIMARY KEY (MED_ID)
);

CREATE TABLE medicine_payment (
	MED_PYM_ID serial NOT NULL,
	MED_PYM_Q integer,
    MED_PYM_TIME timestamp without time zone DEFAULT NOW(),
    MED_PYM_DEL_IND bool DEFAULT FALSE,
    PYM_ID integer REFERENCES payment(PYM_ID),
	MED_ID integer REFERENCES medicine(MED_ID), 
	PRIMARY KEY (MED_PYM_ID)
);