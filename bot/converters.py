import re
from datetime import datetime

import dateutil.parser
import dateutil.tz
from dateutil.relativedelta import relativedelta

from discord.ext import commands


class ISO8601Converter(commands.Converter):
    """Converts a ISO 8601 string into a `datetime.datetime` object."""

    async def convert(
        self,
        ctx: commands.Context,
        iso8601_str: str
    ) -> datetime:
        """Converts a ISO 8601 string into a `datetime.datetime` object."""
        try:
            datetime_obj = dateutil.parser.parse(iso8601_str)
        except ValueError:
            raise commands.errors.BadArgument(
                f"{iso8601_str} is not a valid ISO 8601 string."
            )

        return datetime_obj


class DurationConverter(commands.Converter):
    """
    Converts a duration string into a `datetime.datetime` object.

    Example of a duration string: 1h2m3s
    """

    compiled = re.compile(
        r"(?:(?P<years>\d)y)?"
        r"(?:(?P<months>\d{1,2})mo)?"
        r"(?:(?P<weeks>\d{1,4})w)?"
        r"(?:(?P<days>\d{1,5})d)?"
        r"(?:(?P<hours>\d{1,5})h)?"
        r"(?:(?P<minutes>\d{1,5})m)?"
        r"(?:(?P<seconds>\d{1,5})s)?"
    )

    async def convert(
        self,
        ctx: commands.Context,
        duration_str: str
    ) -> datetime:
        """
        Converts a duration string into a `datetime.datetime` object.

        Example of a duration string: 1h2m3s
        """
        match = self.compiled.fullmatch(duration_str)
        if match is None or not match.group(0):
            raise commands.BadArgument(
                f'Invalid duration provided: "{duration_str}"'
            )

        duration_dict = {
            k: int(v)
            for k, v in match.groupdict(default=0).items()
        }
        return datetime.now() + relativedelta(**duration_dict)
