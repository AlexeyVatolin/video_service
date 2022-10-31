from .handlers import base

url_patterns = [
    (r"/", base.MainHandler),
    (r"/(\d+)", base.PlaylistHandler),
]
