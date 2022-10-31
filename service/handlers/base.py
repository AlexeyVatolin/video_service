import json
import shutil
import tempfile
from pathlib import Path
from tempfile import NamedTemporaryFile

from tornado.web import RequestHandler

from ..services.video import VideoService
from ..settings import settings
from ..video.playlist_creator import VideoCutter


class MainHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def post(self):
        video_file = self.request.files['video'][0]
        cutter_method = self.get_body_argument("method", default="fast") or "fast"
        tone_frequency = float(self.get_body_argument("tone_frequency", default="1") or "1")

        with NamedTemporaryFile(prefix=video_file["filename"], dir=settings["temp_path"]) as f:
            f.write(video_file["body"])
            
            target_path = Path(tempfile.mkdtemp(dir=settings["video_path"]))
            try:
                cutter = VideoCutter(Path(f.name), target_path, method=cutter_method, tone_frequency=tone_frequency)
                playlist_files = cutter.run()
            except:
                shutil.rmtree(target_path)
                raise
        
        video_name = self.get_body_argument("name")
        video = VideoService.add(video_name=video_name, playlist_files=playlist_files)
        self.write(video.as_dict())


class PlaylistHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def get(self, video_id: str):
        video = VideoService.get_playlist_with_chunks(video_id=int(video_id))
        self.write(json.dumps(video))
