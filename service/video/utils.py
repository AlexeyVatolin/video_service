from typing import Any


def get_video_info(probe: dict[str, Any]) -> dict[str, Any]:
    video_info = next(
        (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
        None,
    )
    return video_info or {}

def get_audio_info(probe: dict[str, Any]) -> dict[str, Any]:
    audio_info = next(
        (stream for stream in probe["streams"] if stream["codec_type"] == "audio"),
        None,
    )
    return audio_info or {}
