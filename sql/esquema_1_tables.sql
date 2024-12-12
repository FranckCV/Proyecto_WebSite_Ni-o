CREATE TABLE participante (
    id int(10) NOT NULL AUTO_INCREMENT,
    nombres varchar(255) NOT NULL,
    fecha_nacimiento date NOT NULL,
    telefono varchar(255) NOT NULL,
    correo varchar(255) NOT NULL,
    fecha_registro timestamp not null default current_timestamp(),
    PRIMARY KEY (id)
);
CREATE TABLE elemento (
    id int(10) NOT NULL AUTO_INCREMENT,
    nomElemento varchar(15) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE cualidad (
    id int(10) NOT NULL AUTO_INCREMENT,
    nomAdjetivo varchar(25) NOT NULL,
    descripcion text NOT NULL,
    ELEMENTOid int(10) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE grupo (
    id int(10) NOT NULL AUTO_INCREMENT,
    nomgrupo varchar(255),
    PRIMARY KEY (id)
);
CREATE TABLE administrador (
    id int(11) NOT NULL AUTO_INCREMENT,
    nombres_completos varchar(255) NOT NULL,
    usuario varchar(255) NOT NULL,
    clave varchar(255) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE seleccion (
    PARTICIPANTEid int(10) NOT NULL,
    CUALIDADid int(10) NOT NULL,
    estado tinyint(3) NOT NULL,
    PRIMARY KEY (PARTICIPANTEid, CUALIDADid)
);
CREATE TABLE agrupacion (
    GRUPOid int(10) NOT NULL,
    CUALIDADid int(10) NOT NULL,
    PRIMARY KEY (GRUPOid, CUALIDADid)
);
CREATE TABLE empresa (
    id int(11) NOT NULL AUTO_INCREMENT,
    img_logo longblob NOT NULL,
    img_icono longblob NOT NULL,
    PRIMARY KEY (id)
);
ALTER TABLE cualidad
ADD CONSTRAINT FKCUALIDAD728706 FOREIGN KEY (ELEMENTOid) REFERENCES elemento (id);
ALTER TABLE seleccion
ADD CONSTRAINT FKSELECCION321704 FOREIGN KEY (PARTICIPANTEid) REFERENCES participante (id);
ALTER TABLE seleccion
ADD CONSTRAINT FKSELECCION809300 FOREIGN KEY (CUALIDADid) REFERENCES cualidad (id);
ALTER TABLE agrupacion
ADD CONSTRAINT FKAGRUPACION429682 FOREIGN KEY (GRUPOid) REFERENCES grupo (id);
ALTER TABLE agrupacion
ADD CONSTRAINT FKAGRUPACION321689 FOREIGN KEY (CUALIDADid) REFERENCES cualidad (id);