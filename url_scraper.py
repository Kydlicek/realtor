from Class import RealEstateListing, Database, Scrape


flat_rentals = Scrape(1, 2, "flat_rentals_urls")
flat_rentals.scrape_all()
flat_rentals.add_to_db()
