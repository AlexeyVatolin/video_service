from pathlib import Path
from typing import Literal, Optional

from ..settings import settings
from .playlist import PlaylistBuilder
from .video_cutter import FastVideoCutter, SlowVideoCutter


class VideoCutter:
    def __init__(
        self,
        input_file: Path,
        target_folder: Path,
        method: Literal["fast", "slow"] = "fast",
        segment_seconds: int = 1,
        tone_frequency: Optional[float] = None,
    ) -> None:
        if method == "fast":
            self.cutter = FastVideoCutter(
                input_file=input_file,
                target_folder=target_folder,
                segment_seconds=segment_seconds,
                tone_frequency=tone_frequency,
            )
        elif method == "slow":
            self.cutter = SlowVideoCutter(
                input_file=input_file,
                target_folder=target_folder,
                segment_seconds=segment_seconds,
                tone_frequency=tone_frequency,
            )
            self.playlist = PlaylistBuilder(target_folder / "out.m3u8", segment_seconds)
        else:
            raise ValueError("Method must be slow of fast")
        self.method = method

    def run(self) -> list[Path]:
        files = self.cutter.run()
        if self.method == "slow":
            self.playlist.run(files)
        files = self._get_relative_path(files)
        return files

    def _get_relative_path(self, video_files: list[Path]) -> list[Path]:
        video_files = [x.resolve().relative_to(settings["video_path"]) for x in video_files]
        return video_files


