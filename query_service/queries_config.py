
from data_workflow_api.configs import POSTGRE_TABLE_NAME


#queries
META_DATA_UPDATE_QUERY = "UPDATE test set META_DATA = %s where ID = %s"

HISTOGRAM_QUERY = ""

WOMEN_ACCESSORIES_CASUAL_QUERY = "SELECT * FROM {} WHERE gender='Women' AND masterCategory='Accessories' AND usage='Casual'".format(POSTGRE_TABLE_NAME)

MAN_OPEN_SHOES_FALL = "SELECT * FROM {} WHERE gender='Men' AND (subCategory='Sandal' OR subCategory= 'Flip Flops') AND season='Fall'".format(POSTGRE_TABLE_NAME)

UNISEX_SUMMER = "SELECT gender, season, year, meta_data, hash_key FROM {} WHERE gender='Unisex' AND season='Summer';".format(POSTGRE_TABLE_NAME)

#path to save

PATH_TO_SAVE_CSV = '/home/olysavra/datasqueezer/data_pipeline/data_pipeline_processor/data/csv'
PATH_TO_SAVE_IMAGES = '/home/olysavra/datasqueezer/data_pipeline/data_pipeline_processor/data/download'


