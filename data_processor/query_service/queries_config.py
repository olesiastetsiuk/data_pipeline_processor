
from data_processor.data_workflow_api.configs import POSTGRE_TABLE_NAME


#queries


HISTOGRAM_QUERY = ""#TODO write a query to create histograms

WOMEN_ACCESSORIES_CASUAL_QUERY = "SELECT * FROM {} WHERE gender='Women' AND masterCategory='Accessories' AND usage='Casual'".format(POSTGRE_TABLE_NAME)

MAN_OPEN_SHOES_FALL = "SELECT * FROM {} WHERE gender='Men' AND (subCategory='Sandal' OR subCategory= 'Flip Flops') AND season='Fall'".format(POSTGRE_TABLE_NAME)

UNISEX_SUMMER = "SELECT gender, season, year, meta_data, hash_key FROM {} WHERE gender='Unisex' AND season='Summer';".format(POSTGRE_TABLE_NAME)


META_DATA_UPDATE_QUERY = "UPDATE {} SET meta_data = meta_data || %s ::jsonb WHERE ID = %s".format(POSTGRE_TABLE_NAME)

#META_DATA_UPDATE_QUERY = "UPDATE test set META_DATA = %s where ID = %s"

#path to save

PATH_TO_SAVE_CSV = ''
PATH_TO_SAVE_IMAGES = ''


