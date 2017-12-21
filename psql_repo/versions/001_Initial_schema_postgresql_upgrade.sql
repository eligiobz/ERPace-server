--
-- PostgreSQL database dump
--

-- Dumped from database version 10.1
-- Dumped by pg_dump version 10.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: product; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE product (
    barcode character varying(60) NOT NULL,
    units integer,
    price double precision,
    name character varying(700)
);


--
-- Name: sale; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE sale (
    id bigint NOT NULL,
    date timestamp without time zone
);


--
-- Name: saledetails; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE saledetails (
    idsale integer NOT NULL,
    idproduct character varying(60) NOT NULL,
    productprice double precision,
    units integer
);


--
-- Name: depleteditemsview; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW depleteditemsview AS
 SELECT saledetails.idsale,
    product.barcode,
    product.name,
    sale.date
   FROM ((product
     JOIN saledetails ON (((saledetails.idproduct)::text = (product.barcode)::text)))
     JOIN sale ON ((sale.id = saledetails.idsale)))
  WHERE (product.units = 0);

--
-- Name: pricehistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE pricehistory (
    date_changed timestamp without time zone NOT NULL,
    old_price double precision,
    barcode integer NOT NULL
);


--
-- Name: sale_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE sale_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sale_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE sale_id_seq OWNED BY sale.id;


--
-- Name: salesview; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW salesview AS
 SELECT sale.date,
    product.name,
    saledetails.idsale,
    saledetails.productprice,
    saledetails.units,
    (saledetails.productprice * (saledetails.units)::double precision) AS total_earning
   FROM ((saledetails
     JOIN sale ON ((sale.id = saledetails.idsale)))
     JOIN product ON (((product.barcode)::text = (saledetails.idproduct)::text)));


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE users (
    id smallint NOT NULL,
    username character varying(120),
    password character varying(120),
    level integer
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;

--
-- Name: sale id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY sale ALTER COLUMN id SET DEFAULT nextval('sale_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);

ALTER TABLE ONLY pricehistory
    ADD CONSTRAINT pricehistory_pkey PRIMARY KEY (date_changed, barcode);


--
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY product
    ADD CONSTRAINT product_pkey PRIMARY KEY (barcode);


--
-- Name: sale sale_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY sale
    ADD CONSTRAINT sale_pkey PRIMARY KEY (id);


--
-- Name: saledetails saledetails_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY saledetails
    ADD CONSTRAINT saledetails_pkey PRIMARY KEY (idsale, idproduct);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--
