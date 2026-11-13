import sqlalchemy

print(sqlalchemy.__version__)

# ---- Here you need to install pymysql driver -----
DATABASE_URL = "mysql+pymysql://root:Vishu%401609@127.0.0.1:3306/learnfastapi"

engine = sqlalchemy.create_engine(DATABASE_URL)

conn = engine.connect()

metadata = sqlalchemy.MetaData()
division = sqlalchemy.Table('divisions', metadata, autoload=True, autoload_with=engine)

#* ------------------- Creating URLs Programmatically --------------------------- 
# from sqlalchemy.engine import URL

# url_object = URL.create(
#     "postgresql+pg8000",
#     username="dbuser",
#     password="kx@jj5/g",  # plain (unescaped) text
#     host="pghost10",
#     database="appdb",
# ) 