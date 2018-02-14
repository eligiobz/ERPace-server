DROP VIEW masterlist;
DROP TABLE service_price_history;
DROP TABLE services;

ALTER TABLE products_masterlist RENAME TO masterlist;
ALTER TABLE products_price_history RENAME TO pricehistory;

CREATE OR REPLACE VIEW public.salesview AS
 SELECT sale.date,
    masterlist.name,
    saledetails.idsale,
    saledetails.productprice,
    saledetails.units,
    saledetails.productprice * saledetails.units::double precision AS total_earning
   FROM saledetails
     JOIN sale ON sale.id = saledetails.idsale
     JOIN masterlist ON masterlist.barcode::text = saledetails.idproduct::text;
