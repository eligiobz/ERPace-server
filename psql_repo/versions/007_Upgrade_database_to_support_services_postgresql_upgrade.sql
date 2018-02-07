ALTER TABLE masterlist RENAME TO products_masterlist;

CREATE TABLE services (
	barcode VARCHAR PRIMARY KEY,
	name VARCHAR NOT NULL,
	price DOUBLE PRECISION
);

CREATE VIEW masterlist AS 
SELECT barcode, price, name FROM products_masterlist
UNION
SELECT barcode, price, name FROM services
;
