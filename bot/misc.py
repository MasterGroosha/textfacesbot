from pathlib import Path

from bot.config_reader import config


def get_faces() -> list[str]:
    """
    Fetches kaomoji faces either from local file or from custom path
    :return: list of parsed kaomoji
    """
    if not config.custom_faces_path:
        return [
            item.strip()
            for item in
            Path(__file__).parent
                .joinpath(config.default_faces_filename)
                .open()
                .readlines()
        ]

    try:
        raw_lines = Path(config.custom_faces_path).open().readlines()
    except PermissionError:
        raw_lines = Path(__file__).parent \
            .joinpath(config.default_faces_filename) \
            .open() \
            .readlines()
    return [item.strip() for item in raw_lines]
