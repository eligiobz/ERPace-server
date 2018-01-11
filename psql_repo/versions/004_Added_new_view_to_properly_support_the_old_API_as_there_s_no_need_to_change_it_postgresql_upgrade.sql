CREATE VIEW products_store AS 
 SELECT masterlist.barcode, name, price, product.units, product.storeid 
 FROM masterlist 
 JOIN product ON  masterlist.barcode=product.barcode;
