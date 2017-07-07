# MobilERP

**_Currently under heavy development_**

A small self-hosted ERP that works with your smarphone and laptop.

## The idea

Have a small business who want or need an ERP but have no internet access or can't afford to pay a susbcrition to a cloud hosted service? This solution is for you.
You can either find someone to run this on Raspberry Pi and help you configure your Android phone to work with it or DIY.

This is MobilERP-server. Check the companion repo [MobilERP-android][1].

## What it currently does

It currently saves new items into the stock database and keeps tracks of both sales and changes in item price. It also reports all items on stock (including depleted) or depleted articles exclusively. Works in team with [MobilERP-android][1].

## Roadmap

- [ ] Provide the following reports
	- [x] All products in stock database
	- [x] Depleted products
	- [ ] Changes in price per item
	- [ ] Daily statement
	- [ ] Monthly statement
	- [ ] Most sold products
	- [ ] Least sold products
- [ ] Refactor app to support Flask Blueprints
- [ ] Offer WebUI for people wanting to run it on a single computer.

[1]: https://github.com/eligiobz/mobilerp-android