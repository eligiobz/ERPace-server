DROP VIEW masterlist;
DROP TABLE service_price_history;
DROP TABLE services;

ALTER TABLE products_masterlist RENAME TO masterlist;
ALTER TABLE products_price_history RENAME TO pricehistory;