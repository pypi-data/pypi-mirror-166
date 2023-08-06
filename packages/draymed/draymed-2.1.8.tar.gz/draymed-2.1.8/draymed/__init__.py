"""
Sensyne health library for medical specific helper functions and snomed codes

"""
import re

from . import codes, pregnancy

DATE_DISPLAY_FORMAT = "%Y %b %d"
BMI_DECIMAL_PLACES = 2

NHS_NUMBER_MATCHER = re.compile(r"^[0-9]{10}$")


def bmi(height: float, weight: float) -> float:
    """
    Calculates a persons BMI.
    Uses NHS BMI formula -> (w/h)/h

    :param height: persons height in millimeters
    :type height: float

    :param weight: persons weight in grams
    :type weight: float

    :return: persons bmi (kg/m^2)
    :rtype: float
    """

    fields = [height, weight]
    if None in fields or 0 in fields:
        raise ValueError(
            f'could not calculate BMI from values {{"height": {height}, "weight": {weight}}}'
        )

    height_m = height / 1000
    weight_kg = weight / 1000

    sqr_height = height_m * height_m
    bmi_value = weight_kg / sqr_height
    return round(bmi_value, BMI_DECIMAL_PLACES)


def validate_nhs_number(nhs_number: str) -> bool:
    """
    Checks that a given nhs number is of the correct format

    :param nhs_number: string nhs number
    :type nhs_number: str

    :return: true if given nhs number matches the defined format
    :rtype: bool
    """
    if nhs_number is None:
        return False
    return re.match(NHS_NUMBER_MATCHER, nhs_number) is not None
