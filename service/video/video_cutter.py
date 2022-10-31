import datetime
import math
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import ffmpeg

from .utils import get_audio_info, get_video_info


class BaseVideoCutter(ABC):
    def __init__(
        self,
        input_file: Path,
        target_folder: Path,
        segment_seconds: int = 1,
        tone_frequency: Optional[float] = None,
    ) -> None:
        self.input_file = input_file
        self.target_folder = target_folder
        self.segment_seconds = segment_seconds
        self.tone_frequency = tone_frequency

        self.target_folder.mkdir(exist_ok=True)

    @abstractmethod
    def run(self) -> list[Path]:
        pass

    def _get_audio_param(self, name: str, probe = None) -> str:
        if not probe:
            probe = ffmpeg.probe(self.input_file)
        audio_info = get_audio_info(probe)
        param = audio_info[name]
        return param


class FastVideoCutter(BaseVideoCutter):
    def run(self) -> list[Path]:
        probe = ffmpeg.probe(self.input_file)
        sample_rate = float(self._get_audio_param("sample_rate", probe))
        audio_codec = self._get_audio_param("codec_name", probe)
        segment_time = str(datetime.timedelta(seconds=self.segment_seconds))
        stream = ffmpeg.input(self.input_file)

        stream = stream.output(
            str(self.target_folder / "video_%05d.mp4"),
            f='segment',
            segment_list=str(self.target_folder / "out.m3u8"),
            segment_time=segment_time,
            map=0,
            vcodec="copy",
            acodec=audio_codec,
            reset_timestamps=1,
            sc_threshold=0,
            force_key_frames="expr:gte(t,n_forced*{duration})",
            af=f"asetrate={sample_rate}*{self.tone_frequency},aresample={sample_rate}",
        )
        ffmpeg.run(stream)

        video_files = list(sorted(self.target_folder.glob("*.mp4")))
        return video_files


class SlowVideoCutter(BaseVideoCutter):
    def run(self) -> list[Path]:
        probe = ffmpeg.probe(self.input_file)
        video_info = get_video_info(probe)
        video_length = float(video_info["duration"])

        sample_rate = self._get_audio_param("sample_rate", probe)
        files_count = math.ceil(video_length)

        stream = ffmpeg.input(self.input_file)

        files = []
        for i in range(files_count):
            if self.tone_frequency:
                output_path = self.target_folder / f"video_{i:05}.mp4"
                files.append(output_path)
                ffmpeg.run(
                    stream.output(
                        str(output_path),
                        ss=i,
                        t=self.segment_seconds,
                        af=f"asetrate={sample_rate}*{self.tone_frequency},aresample={sample_rate}",
                    )
                )
        
        return files
