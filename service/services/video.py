from pathlib import Path

from ..models.chunks import Chunk
from ..models.models import DBSession
from ..models.videos import Video


class VideoService:
    @staticmethod
    def add(video_name: str, playlist_files: list[Path], chunk_duration: int = 1) -> Video:
        with DBSession() as session:
            objects = []

            video = Video(name=video_name)
            session.add(video)
            session.commit()
            objects.append(video)

            for i, playlist_path in enumerate(playlist_files):
                objects.append(
                    Chunk(
                        start_second=i * chunk_duration,
                        duration=chunk_duration,
                        path=str(playlist_path),
                        video_id=video.id,
                    )
                )

            session.bulk_save_objects(objects)
            session.commit()
            session.refresh(video)
        return video

    @staticmethod
    def get_playlist_with_chunks(video_id: int):
        with DBSession() as session:
            video: Video = session.query(Video).filter(Video.id == video_id).all()[0]
            return video.as_dict(with_related=True)
