#Use Sqlite database
import sqlite3
from sqlite3 import Error

#Function to create a database connection
def create_connection():
    """Create  a database connection"""
    conn = None
    try:
        conn = sqlite3.connect('hipster_cookbooks.db');
        print(f"Sql Connetion Succesful {sqlite3.version} ")
        return conn
    except Error as e:
        print(f"Error establishing connection with Neo Space: {e}")
        return None

def create_table(conn):
    """Create table structure"""
    try:
        sql_create_cookbooks_table = """
        create table if not EXISTS cookbooks (
        id integer primary key autoincrement,
        title text not null,
        author text not null,
        year_published integer,
        aesthetic_rating integer,
        instagram_worthy boolean,
        cover_color text
        );"""
        #calling the constructor for the cursor object to create a new curosr

        cursor = conn.cursor()
        cursor.execute(sql_create_cookbooks_table)
        print("successfully created a database table")
    except Error as e:
        print(f"Error couldn't create table: {e}")

#function will isert new cookbook
def insert_cookbook(conn, cookbook):
    """Add new cookbook to your shelf"""
    sql ="""Insert into cookbooks(title, author, year_published, aesthetic_rating, 
    instagram_worthy, cover_color)
        values(?,?,?,?,?,?)"""

    #use database connction to insert new record
    try:
        #create a new cursor(this is a pointer thst lets us trsaverse our database)
        cursor = conn.cursor()
        cursor.execute(sql, cookbook)
        #commit changes
        conn.commit()
        print(f"Successfully created cookbook with the id: {cursor.lastrowid}")
        return cursor.lastrowid
    except Error as e:
        print(f"Error adding to the collection: {e}")
        return None
    
def get_all_cookbooks(conn):
    """"Browse your entire collection of cooknbooks"""
    try:
        cursor = conn.cursor()
        cursor.execute("Select * from cookbooks")
        books = cursor.fetchall()
            #put the resultset of cookbooks in a list called bookks
        for book in books:
            print(f"ID: {book[0]}")
            print(f"Title : {book[1]}")
            print(f"Author: {book[2]}")
            print(f"Published: {book[3]}(vintage is better) ")
            print(f"Aesthetic rathing: {'💥' *book[4]}")
            print(f"Instagram Worthy: {'=￣ω￣=' if book[5] else 'Not aesthetic enough'}")
            print(f"Cover color: {book[6]}")
            print(f"---")
        return books
    except Error as e:
        print(F"Error retrieving collections: {e}")
        return []

#Main function called when program executes
#it directs the show
def main():
    #Established connections to our cookbook database
    conn = create_connection()
    #Drop the existing table
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS cookbooks")
    conn.commit()
    #test if connection is viable
    if conn is not None:
        #create our table
        create_table(conn)

        #inserts some carefully curated cookbook samples
        cookbooks = [
            ('Foraged & Found: A guide to pretending you know about mushrooms',
            'Oak Wavelength', 2023, 5, True, 'ForestGreen'),
            ('Small Batch:  Recipes you will never actually make',
            'Sage Moonbeam', 2022, 4, True, 'Raw Linen'),
            ('The Artisitc Toast: Advanced Avovado Techniques',
            'River WildFlower', 2023,5,True, 'Recycled Brown'),
            ('Fermented Everything',
            'Jim Kombucha', 2021, 3, True, 'Denim'),
            ('The Deconstructed sandwich: Making simple things complcated',
            'Juniper vinegar-Smith', 2023, 5, True, 'Beige')
         ]


        print("\n Curating your cookbook collections")

        for cookbook in cookbooks:
            insert_cookbook(conn, cookbook)


        print("\nYour carefully curated collection:")
        get_all_cookbooks(conn)

        conn.close()
        print("\nDatabase connection closed")

    else:
        print("Error! ")

#Code to call the main function
if __name__ =='__main__':
    main()