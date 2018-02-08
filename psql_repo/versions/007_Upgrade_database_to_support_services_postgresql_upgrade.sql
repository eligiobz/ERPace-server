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
    barcode integer NOT NULL
);

CREATE VIEW masterlist AS 
SELECT barcode, price, name FROM products_masterlist
UNION
SELECT barcode, price, name FROM services
;
