"""
Contains helper functions for things specifically relating to pregnancy

"""
import datetime
from typing import NamedTuple

PREGNANCY_PERIOD_DAYS = 280


class PregnancyStage(NamedTuple):
    weeks: int
    days: int
    string: str


def stage(delivery_date: datetime.date) -> PregnancyStage:
    """
    Determines the length of time that a person has been pregnant based the the estimated delivery date

    :param delivery_date: the delivery date
    :type delivery_date: datetime.date

    :return: tuple (weeks, days) representing the elapsed pregnancy time
    :rtype: draymed.PregnancyStage
    """

    if not delivery_date:
        raise ValueError(
            f'could not calculate pregnancy stage from {{"height": {delivery_date}}}'
        )

    today = datetime.date.today()
    full_pregnancy_period = datetime.timedelta(days=PREGNANCY_PERIOD_DAYS)
    conception_date = delivery_date - full_pregnancy_period
    elapsed_pregnancy_period = min(
        (today - conception_date).days, PREGNANCY_PERIOD_DAYS
    )

    if elapsed_pregnancy_period == 0:
        elapsed_weeks = 0
        elapsed_days = 0

    else:
        elapsed_weeks = int(elapsed_pregnancy_period / 7)
        elapsed_days = elapsed_pregnancy_period % 7

    return PregnancyStage(
        weeks=elapsed_weeks,
        days=elapsed_days,
        string=f"{elapsed_weeks} weeks {elapsed_days} days",
    )
