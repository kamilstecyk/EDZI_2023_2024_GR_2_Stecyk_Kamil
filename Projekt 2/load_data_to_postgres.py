from loaders.json_to_postgres_offers_loader import JSONToPostgresOffersLoader

def main():
    print('Saving to db has started...')

    json_to_postgres_loader = JSONToPostgresOffersLoader('data/offers-results.json', 'offers', 'admin', 'admin1234')
    json_to_postgres_loader.insert_data_into_postgres()

if __name__ == "__main__":
    main()

