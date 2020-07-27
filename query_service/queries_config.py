
from data_workflow_api.configs import POSTGRE_TABLE_NAME


#queries
META_DATA_UPDATE_QUERY = "UPDATE test set META_DATA = %s where ID = %s"

HISTOGRAM_QUERY = ""

WOMEN_ACCESSORIES_CASUAL_QUERY = "SELECT * FROM {table_name} WHERE gender='Women' AND masterCategory='Accessories' AND usage='Casual'".format(POSTGRE_TABLE_NAME)

MAN_OPEN_SHOES_FALL = "SELECT * FROM {table_name} WHERE gender='Men' AND (subCategory='Sandal' OR subCategory= 'Flip Flops') AND season='Fall'".format(POSTGRE_TABLE_NAME)

UNISEX_SUMMER = "SELECT gender, season, year, meta_data, hash_key FROM {table_name} WHERE gender='Unisex' AND season='Summer';".format(POSTGRE_TABLE_NAME)


