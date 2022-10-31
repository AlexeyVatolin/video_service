import os

from tornado.options import define

define("port", default=8000, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("database_url", default="postgresql+psycopg2://postgres:postgres@db:5432/postgres", help="database url")
define("debug", default=False, help="debug mode")

__BASE_PACKAGE__ = "video_service"

settings = {}

settings["debug"] = True
settings["temp_path"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "temp_data"))
settings["video_path"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "video_data"))

if not os.path.exists(settings["temp_path"]):
    os.makedirs(settings["temp_path"])
if not os.path.exists(settings["video_path"]):
    os.makedirs(settings["video_path"])
