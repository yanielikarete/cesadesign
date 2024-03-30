ALTER TABLE proveedor ADD COLUMN ciudad_id bigint;
ALTER TABLE proveedor
  ADD CONSTRAINT ciudad_fkey FOREIGN KEY (ciudad_id)
      REFERENCES ciudad (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE proveedor ADD COLUMN pais_id bigint;
ALTER TABLE proveedor
  ADD CONSTRAINT pais_fkey FOREIGN KEY (pais_id)
      REFERENCES pais (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE proveedor ADD COLUMN provincia_id bigint;
ALTER TABLE proveedor
  ADD CONSTRAINT provincia_fkey FOREIGN KEY (provincia_id)
      REFERENCES provincia (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE proveedor ADD COLUMN cuenta_contable_compra_id bigint;
ALTER TABLE proveedor
  ADD CONSTRAINT contabilidad_plandecuentas_fkey FOREIGN KEY (cuenta_contable_compra_id)
      REFERENCES contabilidad_plandecuentas (plan_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

CREATE SEQUENCE sri_forma_pago_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE sri_forma_pago_id_seq
  OWNER TO postgres;


CREATE TABLE sri_forma_pago
(
  id bigint NOT NULL DEFAULT nextval('sri_forma_pago_id_seq'::regclass),
  descripcion character varying,
  codigo character varying,
  CONSTRAINT sri_forma_pago_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE sri_forma_pago
  OWNER TO postgres;


--***************************************************************

-- Table: documento_compra

-- DROP TABLE documento_compra;

CREATE SEQUENCE documento_venta_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE documento_venta_id_seq
  OWNER TO postgres;


CREATE TABLE documento_venta
(
  id bigint NOT NULL DEFAULT nextval('documento_venta_id_seq'::regclass),
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  created_by character varying,
  updated_by character varying,
  fecha_emision date,
  establecimiento character varying(3),
  punto_emision character varying(3),
  secuencial character varying,
  autorizacion character varying,
  descripcion character varying,
  base_iva double precision,
  valor_iva double precision,
  porcentaje_iva double precision,
  base_ice double precision,
  valor_ice double precision,
  porcentaje_ice double precision,
  base_iva_0 double precision,
  valor_iva_0 double precision,
  subtotal double precision,
  descuento double precision,
  total double precision,
  cliente_id bigint,
  proforma_id bigint,
  CONSTRAINT documento_venta_pkey PRIMARY KEY (id),
  CONSTRAINT cliente_fkey FOREIGN KEY (cliente_id)
      REFERENCES cliente (id_cliente) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT proforma_fkey FOREIGN KEY (proforma_id)
      REFERENCES proforma (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE documento_venta
  OWNER TO postgres;

-- Index: fki_cliente_fkey

-- DROP INDEX fki_cliente_fkey;

CREATE INDEX fki_cliente_fkey
  ON documento_venta
  USING btree
  (cliente_id);

-- Index: fki_proforma_fkey

-- DROP INDEX fki_proforma_fkey;

CREATE INDEX fki_proforma_fkey
  ON documento_venta
  USING btree
  (proforma_id);

--***************************************************************

CREATE SEQUENCE documento_venta_detalle_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE documento_venta_detalle_id_seq
  OWNER TO postgres;


-- Table: documento_venta_detalle

-- DROP TABLE documento_venta_detalle;

CREATE TABLE documento_venta_detalle
(
  id bigint NOT NULL DEFAULT nextval('documento_venta_detalle_id_seq'::regclass),
  documento_venta_id bigint,
  producto_id bigint,
  descripcion character varying,
  base_iva double precision,
  valor_iva double precision,
  porcentaje_iva double precision,
  base_ice double precision,
  valor_ice double precision,
  porcentaje_ice double precision,
  base_iva_0 double precision,
  valor_iva_0 double precision,
  subtotal double precision,
  cantidad double precision,
  descuento double precision,
  CONSTRAINT documento_venta_detalle_pkey PRIMARY KEY (id),
  CONSTRAINT documento_venta_fkey FOREIGN KEY (documento_venta_id)
      REFERENCES documento_venta (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT producto_fkey FOREIGN KEY (id)
      REFERENCES producto (producto_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE documento_venta_detalle
  OWNER TO postgres;

-- Index: fki_documento_venta_fkey

-- DROP INDEX fki_documento_venta_fkey;

CREATE INDEX fki_documento_venta_fkey
  ON documento_venta_detalle
  USING btree
  (documento_venta_id);



--***************************************************************

CREATE SEQUENCE documento_retencion_venta_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE documento_retencion_venta_id_seq
  OWNER TO postgres;


-- Table: documento_retencion_venta

-- DROP TABLE documento_retencion_venta;

CREATE TABLE documento_retencion_venta
(
  id bigint NOT NULL DEFAULT nextval('documento_retencion_venta_id_seq'::regclass),
  documento_venta_id bigint,
  fecha_emision date,
  establecimiento character varying(3),
  punto_emision character varying(3),
  secuencial character varying,
  autorizacion character varying,
  descripcion character varying,
  CONSTRAINT documento_retencion_venta_pkey PRIMARY KEY (id),
  CONSTRAINT documento_venta_fkey FOREIGN KEY (documento_venta_id)
      REFERENCES documento_venta (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE documento_retencion_venta
  OWNER TO postgres;

  
--***************************************************************

  CREATE SEQUENCE documento_retencion_detalle_compra_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE documento_retencion_detalle_compra_id_seq
  OWNER TO postgres;
  
CREATE TABLE documento_retencion_detalle_compra
(
  id bigint NOT NULL DEFAULT nextval('documento_retencion_detalle_compra_id_seq'::regclass),
  retencion_detalle_id bigint,
  base_imponible double precision,
  porcentaje_retencion double precision,
  valor_retenido double precision,
  documento_retencion_compra_id bigint,
  CONSTRAINT documento_retencion_detalle_compra_pkey PRIMARY KEY (id),
  CONSTRAINT documento_retencion_compra_fkey FOREIGN KEY (documento_retencion_compra_id)
      REFERENCES documento_retencion_compra (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT retencion_detalle_fkey FOREIGN KEY (retencion_detalle_id)
      REFERENCES retencion_detalle (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE documento_retencion_detalle_compra
  OWNER TO postgres;

-- Index: fki_documento_retencion_compra_fkey

-- DROP INDEX fki_documento_retencion_compra_fkey;

CREATE INDEX fki_documento_retencion_compra_fkey
  ON documento_retencion_detalle_compra
  USING btree
  (documento_retencion_compra_id);


--***************************************************************


CREATE SEQUENCE documento_retencion_detalle_venta_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE documento_retencion_detalle_venta_id_seq
  OWNER TO postgres;


-- Table: documento_retencion_detalle_venta

-- DROP TABLE documento_retencion_detalle_venta;

CREATE TABLE documento_retencion_detalle_venta
(
  id bigint NOT NULL DEFAULT nextval('documento_retencion_detalle_venta_id_seq'::regclass),
  retencion_detalle_id bigint,
  base_imponible double precision,
  porcentaje_retencion double precision,
  valor_retenido double precision,
  documento_retencion_venta_id bigint,
  CONSTRAINT documento_retencion_detalle_venta_pkey PRIMARY KEY (id),
  CONSTRAINT documento_retencion_venta_fkey FOREIGN KEY (documento_retencion_venta_id)
      REFERENCES documento_retencion_detalle_venta (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT retencion_detalle_fkey FOREIGN KEY (retencion_detalle_id)
      REFERENCES retencion_detalle (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE documento_retencion_detalle_venta
  OWNER TO postgres;

-- Index: fki_documento_retencion_venta_fkey

-- DROP INDEX fki_documento_retencion_venta_fkey;

CREATE INDEX fki_documento_retencion_venta_fkey
  ON documento_retencion_detalle_venta
  USING btree
  (documento_retencion_venta_id);

-- Index: fki_retencion_detalle_fkey

-- DROP INDEX fki_retencion_detalle_fkey;

CREATE INDEX fki_retencion_detalle_fkey
  ON documento_retencion_detalle_venta
  USING btree
  (retencion_detalle_id);


--******************** LEONEL *******************************************


CREATE TABLE proveedor_plancuenta
(
  id bigserial NOT NULL,
  proveedor_id integer,
  plancuenta_id integer,
  CONSTRAINT proveedor_plancuenta_pkey PRIMARY KEY (id),
  CONSTRAINT plancuenta_fkey FOREIGN KEY (plancuenta_id)
      REFERENCES contabilidad_plandecuentas (plan_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT proveedor_fkey FOREIGN KEY (proveedor_id)
      REFERENCES proveedor (proveedor_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE proveedor_plancuenta
  OWNER TO postgres;



CREATE TABLE proveedor_retenciones
(
  id bigserial NOT NULL,
  proveedor_id integer,
  retencion_id integer,
  CONSTRAINT proveedor_retenciones_pkey PRIMARY KEY (id),
  CONSTRAINT proveedor_fkey FOREIGN KEY (proveedor_id)
      REFERENCES proveedor (proveedor_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT retencion_fkey FOREIGN KEY (retencion_id)
      REFERENCES retencion_detalle (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE proveedor_retenciones
  OWNER TO postgres;



--proveedor

ALTER TABLE proveedor ADD COLUMN vendedor_id integer;
ALTER TABLE proveedor ADD COLUMN tipo_persona character varying(255);
ALTER TABLE proveedor ADD COLUMN dias_credito character varying(255);
ALTER TABLE proveedor ADD COLUMN fecha_emision character varying(255);
ALTER TABLE proveedor ADD COLUMN comentario character varying(255);
ALTER TABLE proveedor ADD COLUMN tipo_proveedor character varying(255);
ALTER TABLE proveedor ADD COLUMN cuenta_anticipo_id integer;
ALTER TABLE proveedor ADD COLUMN cuenta_contable_compra_id bigint;
ALTER TABLE proveedor ADD COLUMN cedula character varying(20);
ALTER TABLE proveedor ADD COLUMN ciudad_id bigint;
ALTER TABLE proveedor ADD COLUMN pais_id bigint;
ALTER TABLE proveedor ADD COLUMN provincia_id bigint;
ALTER TABLE proveedor ADD COLUMN razon_social character varying(255);
ALTER TABLE proveedor ADD COLUMN tipo_proveedor character varying(255);
ALTER TABLE proveedor ADD COLUMN apellido character varying(255);


--cliente


ALTER TABLE cliente ADD COLUMN tipo_cliente character varying(255);
ALTER TABLE cliente ADD COLUMN serie character varying(255);
ALTER TABLE cliente ADD COLUMN pais_id bigint;
ALTER TABLE cliente ADD COLUMN cuenta_contable_venta_id bigint;
ALTER TABLE cliente ADD COLUMN cedula character varying(20);
ALTER TABLE cliente ADD COLUMN cuenta_cobrar_id bigint;
ALTER TABLE cliente ADD COLUMN apellido character varying(255);
ALTER TABLE cliente ADD COLUMN fecha_emision character varying(255);


--******************** LEONEL *******************************************

CREATE SEQUENCE documento_venta_forma_pago_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE documento_venta_forma_pago_id_seq
  OWNER TO postgres;

-- Table: documento_venta_forma_pago_id_seq

-- DROP TABLE documento_venta_forma_pago_id_seq;

CREATE TABLE documento_venta_forma_pago
(
  id bigint NOT NULL DEFAULT nextval('documento_venta_forma_pago_id_seq'::regclass),
  codigo character varying,
  descripcion character varying,
  documento_venta_id bigint,
  CONSTRAINT documento_venta_forma_pago_pkey PRIMARY KEY (id),
  CONSTRAINT documento_venta_fkey FOREIGN KEY (documento_venta_id)
      REFERENCES documento_venta (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE documento_venta_forma_pago
  OWNER TO postgres;


-- Foreign Key: documento_retencion_venta_fkey

-- ALTER TABLE documento_retencion_detalle_venta DROP CONSTRAINT documento_retencion_venta_fkey;

ALTER TABLE documento_retencion_detalle_venta
  ADD CONSTRAINT documento_retencion_venta_fkey FOREIGN KEY (documento_retencion_venta_id)
      REFERENCES documento_retencion_venta (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;


--Cuenta de anticipo y por pagar a proveedores
update proveedor set cuenta_contable_compra_id = 678, cuenta_anticipo_id=601;


--Cuenta de anticipo y por cobrar a clientes
--Ceunta x cobrar y cuenta de anticipo
update cliente set cuenta_contable_venta_id = 21, cuenta_cobrar_id=1056;

ALTER TABLE movimiento ADD COLUMN proveedor_id bigint;
ALTER TABLE movimiento
  ADD CONSTRAINT proveedor_id_fkey FOREIGN KEY (proveedor_id)
      REFERENCES proveedor (proveedor_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;


