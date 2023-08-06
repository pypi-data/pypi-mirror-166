import enum, ntpath, os
from beartype import beartype
from beartype.typing import Union
from pathlib import Path


# Enum for size units
class SIZE_UNIT(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


@beartype
def convert_unit(
    size_in_bytes: Union[float, int], unit: SIZE_UNIT
) -> Union[float, int]:
    """Convert the size from bytes to other units like KB, MB or GB"""
    if unit == SIZE_UNIT.KB:
        return size_in_bytes / 1024
    elif unit == SIZE_UNIT.MB:
        return size_in_bytes / (1024 * 1024)
    elif unit == SIZE_UNIT.GB:
        return size_in_bytes / (1024 * 1024 * 1024)
    else:
        return size_in_bytes


@beartype
def delete_file(file_path: str) -> None:
    try:
        os.remove(file_path)
    except:
        pass


@beartype
def file_exists(file_path: str) -> bool:
    if os.path.exists(file_path):
        return True

    return False


@beartype
def get_file_name_from_path(path: str) -> str:
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


@beartype
def remove_file_extention(file_path: str):
    path = Path(file_path).with_suffix("")
    return str(path)


@beartype
def create_directory(file_path: str):
    try:
        os.makedirs(file_path, exist_ok=True)
    except:
        pass
