import json
import psycopg2

class JSONToPostgresOffersLoader:
    def __init__(self, json_filepath, dbname, user, password, host='localhost', port='5432'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.json_file = json_filepath

    def connect_to_postgres(self):
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return conn
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL database:", e)
            return None

    def insert_data_into_postgres(self):
        offers_data = self.__load_data_from_json()
        conn = self.connect_to_postgres()

        if offers_data is not None and conn is not None:
            cur = conn.cursor()

            # Your insertion logic here
            
            self.__insert_data_into_position_table(cur, offers_data)
            self.__insert_data_into_company_table(cur, offers_data)
            self.__insert_data_into_category_table(cur, offers_data)
            self.__insert_data_into_currency_table(cur, offers_data)
            self.__insert_data_into_source_table(cur, offers_data)
            self.__insert_data_into_skill_table(cur, offers_data)

            try:
                conn.commit()
                print("Transaction committed successfully.")
            except psycopg2.Error as e:
                print("Error committing transaction:", e)
                conn.rollback()
            finally:
                cur.close()
                conn.close()
            
            print('Data has been written to db')
        else: 
            print('Data has not been loaded to postgresql database.')

    def __load_data_from_json(self):
        try:
            with open(self.json_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{self.json_file}' not found.")
            return None
        except Exception:
            print(f"Error: There was a problem with '{self.json_file}'. Data from json file has not been fetched.")
            return None
        
    def __insert_data_into_position_table(self, cur, offers_data):
        for offer in offers_data:
            cur.execute("""
                INSERT INTO position (position_name)
                VALUES (%s)
                ON CONFLICT DO NOTHING
            """, (offer['job_position'],))
        
        print('Inserting into position table has been executed.')

    def __insert_data_into_company_table(self, cur, offers_data):
        for offer in offers_data:
            cur.execute("""
                INSERT INTO company (company_name)
                VALUES (%s)
                ON CONFLICT DO NOTHING
            """, (offer['company'],))

        print('Inserting into comapny table has been executed.')

    def __insert_data_into_category_table(self, cur, offers_data):
        for offer in offers_data:
            for offer_category in offer['category']:
                cur.execute("""
                    INSERT INTO category (category_name)
                    VALUES (%s)
                    ON CONFLICT DO NOTHING
                """, (offer_category,))
        
        print('Inserting into category table has been executed.')


    def __insert_data_into_currency_table(self, cur, offers_data):
        for offer in offers_data:
            cur.execute("""
                INSERT INTO currency (currency_name)
                VALUES (%s)
                ON CONFLICT DO NOTHING
            """, (offer['currency'],))

        print('Inserting into currency table has been executed.')

    def __insert_data_into_source_table(self, cur, offers_data):
        for offer in offers_data:
            cur.execute("""
                INSERT INTO source (source_name)
                VALUES (%s)
                ON CONFLICT DO NOTHING
            """, (offer['source'],))
        
        print('Inserting into source table has been executed.')

    def __insert_data_into_skill_table(self, cur, offers_data):
        for offer in offers_data:
            for offer_skill in offer['skills']:
                cur.execute("""
                    INSERT INTO skill (skill_name)
                    VALUES (%s)
                    ON CONFLICT DO NOTHING
                """, (offer_skill,))
        
        print('Inserting into skill table has been executed.')

    # def __insert_data_into_skills_table_and_offer_skills_table(self, cur, offers_data):
    #     for offer in offers_data:
    #         offer_id = offer['id']

    #         for skill in offer['skills']:
    #             cur.execute("""
    #                 INSERT INTO skills (skill_name)
    #                 VALUES (%s)
    #                 ON CONFLICT DO NOTHING
    #             """, (skill,))
    #             cur.execute("""
    #                 INSERT INTO offer_skills (offer_id, skill_id)
    #                 SELECT %s, skill_id
    #                 FROM skills
    #                 WHERE skill_name = %s
    #             """, (offer_id, skill))
        
    #     print('Inserting into skills and offer_skills table has been executed.')

