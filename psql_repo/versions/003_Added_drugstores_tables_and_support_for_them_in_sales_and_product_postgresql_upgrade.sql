-- CREATE TABLE drugstore(
-- 	id SERIAL primary key,
-- 	name text
-- );

-- CREATE TABLE masterlist(
-- 	barcode character varying(60) NOT NULL primary key,
-- 	price double precision,
--     name character varying(700)
-- );

-- ALTER TABLE product RENAME TO tmp_product;

-- CREATE TABLE product(
-- 	barcode character varying(60),
-- 	units integer,
--     storeid integer NOT NULL
-- );

-- INSERT INTO drugstore(name) values('default');

-- INSERT INTO masterlist(barcode, name, price) SELECT barcode, name, price FROM tmp_product;

-- INSERT INTO product(barcode, units, storeid) SELECT barcode, units, 1 FROM tmp_product;

-- UPDATE product SET storeid = (SELECT MAX(id) FROM DrugStore);

-- -- We need to recreate the views
-- DROP VIEW salesview;
-- DROP VIEW depleteditemsview;

-- DROP table tmp_product;

-- -- New version of the views

-- CREATE VIEW salesview AS
--  SELECT sale.date,
--     masterlist.name,
--     saledetails.idsale,
--     saledetails.productprice,
--     saledetails.units,
--     (saledetails.productprice * (saledetails.units)::double precision) AS total_earning
--    FROM ((saledetails
--      JOIN sale ON ((sale.id = saledetails.idsale)))
--      JOIN masterlist ON (((masterlist.barcode)::text = (saledetails.idproduct)::text)));

-- -- New version of the views

-- CREATE VIEW depleteditemsview AS
--  SELECT saledetails.idsale,
--     masterlist.name,
--     sale.date,
--     product.storeid,
--     product.units,
--     product.barcode
--    FROM ((product
--      JOIN saledetails ON (((saledetails.idproduct)::text = (product.barcode)::text)))
--      JOIN masterlist on (((masterlist.barcode)::text = (product.barcode)::text))
--      JOIN sale ON ((sale.id = saledetails.idsale)))

--   WHERE (product.units = 0);
