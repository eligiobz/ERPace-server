-- We need to recreate the views
DROP VIEW salesview;
DROP VIEW depleteditemsview;

ALTER TABLE product RENAME TO tmp_product;

CREATE TABLE product (
    barcode character varying(60) NOT NULL,
    units integer,
    price double precision,
    name character varying(700)
);

INSERT INTO product(barcode, price, name, units) 
	SELECT masterlist.barcode, masterlist.price, masterlist.name, units
	FROM masterlist 
	INNER JOIN tmp_Product ON masterlist.barcode = tmp_product.barcode;

DROP table tmp_product;

DROP TABLE drugstore;
DROP TABLE masterlist;

CREATE VIEW depleteditemsview AS
 SELECT saledetails.idsale,
    product.barcode,
    product.name,
    sale.date
   FROM ((product
     JOIN saledetails ON (((saledetails.idproduct)::text = (product.barcode)::text)))
     JOIN sale ON ((sale.id = saledetails.idsale)))
  WHERE (product.units = 0);


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