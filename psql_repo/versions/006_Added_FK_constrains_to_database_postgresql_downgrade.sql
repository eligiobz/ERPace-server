ALTER TABLE product
	DROP CONSTRAINT fk_product_barcode;
   
ALTER TABLE product
	DROP CONSTRAINT fk_product_storeid;

ALTER TABLE pricehistory
   DROP CONSTRAINT fk_pricehistory_barcode;

ALTER TABLE saledetails
	DROP CONSTRAINT fk_saledetails_storeid;

ALTER TABLE saledetails
	DROP COLUMN storeid;

ALTER TABLE saledetails
	DROP CONSTRAINT fk_saledetails_idsale;