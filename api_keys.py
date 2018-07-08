import os
from os.path import join, dirname
from dotenv import load_dotenv

if(not os.path.isfile(".env")):
    print(".env does not exist")
    quit()
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AP = os.environ.get("API_KEY")
APS = os.environ.get("API_SECRET")
AT = os.environ.get("ACCESS_TOKEN")
ATS = os.environ.get("ACCESS_TOKEN_SECRET")
