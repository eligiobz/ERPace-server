DROP VIEW salesview;
ALTER TABLE pricehistory ALTER COLUMN barcode TYPE CHARACTER VARYING(60);
ALTER TABLE masterlist RENAME TO products_masterlist;
ALTER TABLE  pricehistory RENAME TO products_price_history;

CREATE TABLE services (
	barcode VARCHAR PRIMARY KEY,
	name VARCHAR NOT NULL,
	price DOUBLE PRECISION
);

create table service_price_history(
    date_changed timestamp without time zone NOT NULL,
    old_price double precision,
    barcode varchar NOT NULL
);

CREATE VIEW masterlist AS 
SELECT barcode, price, name FROM products_masterlist
UNION
SELECT barcode, price, name FROM services
;


CREATE OR REPLACE VIEW salesview AS 
SELECT sale.date,
   masterlist.name,
   saledetails.idsale,
   saledetails.productprice,
   saledetails.units,
   saledetails.productprice * saledetails.units::double precision AS total_earning
  FROM saledetails
    JOIN sale ON sale.id = saledetails.idsale
    JOIN masterlist ON masterlist.barcode::text = saledetails.idproduct::text;
