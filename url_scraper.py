from Scrape import Scrape

flat_rentals = Scrape(1,2,'flat_rentals_urls')
flat_rentals.scrape(1,5)
flat_rentals.add_to_db()

