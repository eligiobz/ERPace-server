# MobilERP

[![Build Status](https://travis-ci.org/eligiobz/mobilerp-server.svg?branch=master)](https://travis-ci.org/eligiobz/mobilerp-server) [![codecov](https://codecov.io/gh/eligiobz/mobilerp-server/branch/master/graph/badge.svg)](https://codecov.io/gh/eligiobz/mobilerp-server)


A small self-hosted ERP that works with your smarphone and laptop.

## Goal

Provide people with an easy to use, no bs, FOSS solution to help them manage their stores/shops, giving them the choice on how and where they want to deploy the system.


This is MobilERP-server. Check the companion repo [MobilERP-kotlin][1].

## What it currently does

* Saves new items into the stock database 
* Keeps tracks of both sales and changes in item price
* It also reports all items on stock (including depleted) or depleted articles exclusively
* Manage multiple store witht the same stock
* Report of most/least sold items

## Roadmap

- [ ] Provide the following reports
	- [x] ~~All products in stock database~~
	- [x] ~~Depleted products~~
	- [X] ~~Changes in price per item~~
	- [X] ~~Daily statement~~
	- [X] ~~Monthly statement~~
	- [ ] Most sold products
	- [ ] Least sold products
- [X] ~~Refactor app to support Flask Blueprints~~
- [ ] Offer WebUI for people wanting to run it on a single computer.
- [ ] Multiple users with permision levels

## License

This project is licensed under [AGPL3][2]

[1]: https://github.com/eligiobz/mobilerp-kotlin
[2]: LICENSE.md