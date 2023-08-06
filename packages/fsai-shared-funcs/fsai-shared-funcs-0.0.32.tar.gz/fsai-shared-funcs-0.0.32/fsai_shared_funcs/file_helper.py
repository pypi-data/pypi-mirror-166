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
def get_file_name_from_path(file_path: str) -> str:
    head, tail = ntpath.split(file_path)
    return tail or ntpath.basename(head)


@beartype
def combine_path_and_filename(file_path: str, file_name: str):
    return os.path.join(
        file_path,
        file_name.lstrip(
            os.path.sep
        ),  # remove leading forward slash which causes join to think path is relative
    )


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


def get_file_size(file_path, unit: SIZE_UNIT):
    file_size_b = os.stat(file_path).st_size
    file_size_in_units = convert_unit(file_size_b, unit)
    return file_size_in_units
