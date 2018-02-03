ALTER TABLE product 
	ADD CONSTRAINT fk_product_barcode
	FOREIGN KEY (barcode)
	REFERENCES masterlist(barcode);

ALTER TABLE product 
	ADD CONSTRAINT fk_product_storeid
	FOREIGN KEY (storeid)
	REFERENCES drugstore(id);

ALTER TABLE pricehistory
	ADD CONSTRAINT fk_pricehistory_barcode
	FOREIGN KEY (barcode) 
	REFERENCES masterlist(barcode);

ALTER TABLE saledetails
	ADD COLUMN storeid integer,
	ADD CONSTRAINT fk_saledetails_storeid
	FOREIGN KEY (storeid)
	REFERENCES drugstore(id);

ALTER TABLE saledetails
	ADD CONSTRAINT fk_saledetails_idsale
	FOREIGN KEY (idsale)
	REFERENCES sale(id);