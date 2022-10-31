import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import options

from service.settings import settings
from service.urls import url_patterns


class TornadoApplication(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)

    # def create_database(self):
    #     """ this will create a database """
    #     models_base.metadata.create_all(db_engine)


def main():
    app = TornadoApplication()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
