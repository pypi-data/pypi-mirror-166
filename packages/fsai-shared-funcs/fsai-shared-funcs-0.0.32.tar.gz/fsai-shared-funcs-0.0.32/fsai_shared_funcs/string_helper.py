from beartype import beartype


@beartype
def string_is_true_or_false(input_string: str) -> bool:
    ua = input_string.capitalize()
    if "True".startswith(ua):
        return True
    elif "False".startswith(ua):
        return False
    else:
        return False
