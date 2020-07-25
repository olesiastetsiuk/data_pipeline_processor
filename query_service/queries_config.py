#AWS configs

# cursor.execute("""SELECT table_name FROM information_schema.tables
# WHERE table_schema = 'public'""")
# for table in self.cursor.fetchall():
#     print(table)




#queries
META_DATA_UPDATE_QUERY = "UPDATE test set META_DATA = %s where ID = %s"

HISTOGRAM_QUERY = ""

WOMEN_ACCESSORIES_CASUAL_QUERY = "SELECT * FROM table_name WHERE gender='Women' AND masterCategory='Accessories' AND usage='Casual'"

MAN_OPEN_SHOES_FALL = "SELECT * FROM table_name WHERE gender='Men' AND (subCategory='Sandal' OR subCategory= 'Flip Flops') AND season='Fall'"

UNISEX_SUMMER = "SELECT gender, season, year, hash_key, meta_data FROM table_name WHERE gender='Unisex' AND season='Summer';"


