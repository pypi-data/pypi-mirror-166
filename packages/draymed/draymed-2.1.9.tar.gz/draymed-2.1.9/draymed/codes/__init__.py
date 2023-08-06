from typing import Any, Callable, Dict, Optional

from .map import code_map


def description_from_code(code: str, category: Optional[str] = None) -> str:
    """
    Retrieves a human readable description label from a draymed code
    :param code: a valid draymed code
    :param category: the category that the code is associated with
    :return: the human readable description label associated with the supplied code
    """
    if not code:
        raise ValueError(f"a valid draymed code is required. not {code}")

    if category:
        if category not in code_map:
            raise KeyError(f"category '{category}' does not exist")
        elif code not in code_map[category]:
            raise KeyError(
                f"No name found with code '{code}' under category '{category}'"
            )
        return code_map[category][code]["long"]

    for key in code_map:
        if code in code_map[key]:
            return code_map[key][code]["long"]

    raise KeyError(f"No name found with code '{code}'")


def description_from_name(name: str, category: Optional[str] = None) -> str:
    """
    Retrieves a human readable description label from a short name tag
    :param name: short name tag
    :param category: the category that the name is associated with
    :type category: str or None
    :return: the human readable description label associated with the short name tag
    """
    if not name:
        raise ValueError(f"a valid name is required. not {name}")

    if category:
        if category not in code_map:
            raise KeyError(f"category '{category}' does not exist")
        for item in code_map[category]:
            if code_map[category][item]["short"] == name:
                return code_map[category][item]["long"]
        raise KeyError(f"No code found with name '{name}' under category '{category}'")

    for key in code_map:
        for item in code_map[key]:
            if code_map[key][item]["short"] == name:
                return code_map[key][item]["long"]

    raise KeyError(f"No code found with name '{name}'")


def code_from_name(name: str, category: Optional[str] = None) -> str:
    """
    Retrieves a draymed code from a short name tag
    :param name: short name tag
    :param category: the category that the name is associated with
    :return: the draymed associated with the supplied label
    """
    if not name:
        raise ValueError(f"a valid name is required. not {name}")

    if category:
        if category not in code_map:
            raise KeyError(f"category '{category}' does not exist")

        for item in code_map[category]:
            if code_map[category][item]["short"] == name:
                return item

        raise KeyError(f"No code found with name '{name}' under category '{category}'")

    for key in code_map:
        for item in code_map[key]:
            if code_map[key][item]["short"] == name:
                return item

    raise KeyError(f"No code found with name '{name}'")


def code_from_description(description: str, category: Optional[str] = None) -> str:
    """
    Retrieves a draymed code from a human readable description label
    :param description: human readable description label
    :param category: the category that the description is associated with
    :return: the draymed associated with the supplied label
    """
    if not description:
        raise ValueError(f"a valid description is required. not {description}")

    if category:
        if category not in code_map:
            raise KeyError(f"category '{category}' does not exist")

        for item in code_map[category]:
            if code_map[category][item]["long"] == description:
                return item

        raise KeyError(
            f"No code found with description '{description}' under category '{category}'"
        )

    for key in code_map:
        for item in code_map[key]:
            if code_map[key][item]["long"] == description:
                return item

    raise KeyError(f"No code found with description '{description}'")


def category_from_code(code: str) -> str:
    """
    Retrieves the category that draymed code is associated with
    :param code: a valid draymed code
    :return: string category name
    """
    if not code:
        raise ValueError(f"a valid draymed code is required. not {code}")

    for category in code_map:
        if code in code_map[category]:
            return category

    raise KeyError(f"No category found containing code '{code}'")


def category_from_name(name: str) -> str:
    """
    Retrieves the category the short name tag is associated with
    :param name: short name tag
    :return: string category name
    """
    if not name:
        raise ValueError(f"a valid draymed code is required. not {name}")

    for category in code_map:
        for item in code_map[category]:
            if code_map[category][item]["short"] == name:
                return category

    raise KeyError(f"No category found containing name '{name}'")


def code_exists(code: str, category: Optional[str] = None) -> bool:
    """
    Returns true if a code exists. If category is provided, True will be returned if
    the code exists in that category, otherwise, if None, True is returned if the
    code exists in any category.
    :param code: a valid code known to draymed
    :param category: the name of the category that the code is associated with
    :return: True if the code exists, otherwise False
    """
    if not code:
        raise ValueError(f"a valid draymed code is required. not {code}")

    if category:
        if category not in code_map:
            raise KeyError(f"category '{category}' does not exist")
        else:
            return code in code_map[category]

    for key in code_map:
        if code in code_map[key]:
            return True

    return False


def list_category(category: str) -> Dict[str, Dict[str, str]]:
    """
    returns a category by name
    :param category: name of category
    :return: category dict
    """
    if not category:
        raise ValueError(f"a valid draymed category name is required. not {category}")

    if category not in code_map:
        raise KeyError(f"category '{category}' does not exist")

    return code_map[category]


def find_or_none(method: Callable, code: str, category: Optional[str] = None) -> Any:
    """
    used to wrap another method in this module to return None instead of raising an error
    :param method: method to call in try block
    :param code: a valid code known to draymed
    :param category: the name of the category that the code is associated with
    :return: the return value of 'method' if no error is raised, otherwise None
    """
    try:
        if category:
            return method(code, category=category)
        return method(code)

    except (KeyError, ValueError):
        return None
