from pathlib import Path

import ffmpeg

from .utils import get_video_info


class PlaylistBuilder:
    def __init__(self, target_file: Path, segment_seconds: int = 1) -> None:
        self.target_file = target_file
        self.segment_seconds = segment_seconds

    def run(self, input_files: list[Path]):
        with self.target_file.open("w") as f:
            f.write("\n".join([
                "#EXTM3U",
                "#EXT-X-VERSION:3", 
                "#EXT-X-MEDIA-SEQUENCE:0"
                "#EXT-X-ALLOW-CACHE:YES",
                f"#EXT-X-TARGETDURATION:{self.segment_seconds}"
            ]))
            for file in sorted(input_files):
                probe = ffmpeg.probe(str(file))
                video_info = get_video_info(probe)
                video_length = float(video_info["duration"])
                f.write("\n" +
                    f"#EXTINF:{video_length}," +
                    "\n" +
                    file.name
                )
