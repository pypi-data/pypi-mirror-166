# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Get a random quote for a given day."""

from __future__ import annotations

import dataclasses
import email.utils
import logging
from datetime import date, datetime, timedelta, timezone
from typing import Any

from tornado.web import HTTPError

from .. import EVENT_REDIS
from ..utils.request_handler import APIRequestHandler
from .utils import (
    WRONG_QUOTES_CACHE,
    QuoteReadyCheckHandler,
    WrongQuote,
    get_wrong_quotes,
)

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class QuoteOfTheDayData:
    """The class representing data for the quote of the day."""

    __slots__ = ("date", "wrong_quote", "url_without_path")
    date: date
    wrong_quote: WrongQuote
    url_without_path: str

    def get_date_for_rss(self) -> str:
        """Get the date as specified in RFC 2822."""
        return email.utils.format_datetime(
            datetime(
                year=self.date.year,
                month=self.date.month,
                day=self.date.day,
                tzinfo=timezone.utc,
            ),
            True,
        )

    def get_quote_as_str(self, new_line_char: str = "\n") -> str:
        """Get the quote as a string with new line."""
        return (
            f"»{self.wrong_quote.quote}«{new_line_char}"
            f"- {self.wrong_quote.author}"
        )

    def get_quote_image_url(self) -> str:
        """Get the URL of the image of the quote."""
        return self.get_quote_url() + ".gif"

    def get_quote_url(self) -> str:
        """Get the URL of the quote."""
        return (
            f"{self.url_without_path}/zitate/{self.wrong_quote.get_id_as_str()}"
        )

    def get_title(self) -> str:
        """Get the title for the quote of the day."""
        return f"Das Zitat des Tages vom {self.date:%d. %m. %Y}"

    def to_json(self) -> dict[str, Any]:
        """Get the quote of the day as JSON."""
        return {
            "date": self.date.isoformat(),
            "wrong_quote": self.wrong_quote.to_json(),
            "url": self.get_quote_url(),
            "image": self.get_quote_image_url(),
        }


class QuoteOfTheDayBaseHandler(QuoteReadyCheckHandler):
    """The base request handler for the quote of the day."""

    async def get_quote_by_date(
        self, wq_date: date | str
    ) -> None | QuoteOfTheDayData:
        """Get the quote of the date if one was saved."""
        if not EVENT_REDIS.is_set():
            return None

        if isinstance(wq_date, str):
            wq_date = date.fromisoformat(wq_date)

        wq_id = await self.redis.get(self.get_redis_quote_date_key(wq_date))
        if not wq_id:
            return None
        quote, author = tuple(int(x) for x in wq_id.split("-"))
        wrong_quote = WRONG_QUOTES_CACHE.get((quote, author))
        if not wrong_quote:
            return None
        return QuoteOfTheDayData(
            wq_date, wrong_quote, self.get_scheme_and_netloc()
        )

    async def get_quote_of_today(self) -> None | QuoteOfTheDayData:
        """Get the quote for today."""
        if not EVENT_REDIS.is_set():
            return None
        today = datetime.utcnow().date()
        quote_data = await self.get_quote_by_date(today)
        if quote_data:  # if was saved already
            return quote_data
        quotes: tuple[WrongQuote, ...] = get_wrong_quotes(
            lambda wq: wq.rating > 1, shuffle=True
        )
        if not quotes:
            logger.warning("No quotes available")
            return None
        for quote in quotes:
            if await self.has_been_used(quote.get_id_as_str()):
                continue
            wq_id = quote.get_id_as_str()
            await self.set_used(wq_id)
            await self.redis.setex(
                self.get_redis_quote_date_key(today),
                60 * 60 * 24 * 420,  # TTL
                wq_id,
            )
            return QuoteOfTheDayData(today, quote, self.get_scheme_and_netloc())
        logger.critical("Failed to generate a new quote of the day")
        return None

    def get_redis_quote_date_key(self, wq_date: date) -> str:
        """Get the Redis key for getting quotes by date."""
        return f"{self.redis_prefix}:quote-of-the-day:by-date:{wq_date.isoformat()}"

    def get_redis_used_key(self, wq_id: str) -> str:
        """Get the Redis used key."""
        return f"{self.redis_prefix}:quote-of-the-day:used:{wq_id}"

    def get_scheme_and_netloc(self) -> str:
        """Get the beginning of the URL."""
        return f"{self.request.protocol}://{self.request.host}"

    async def has_been_used(self, wq_id: str) -> None | bool:
        """Check with Redis here."""
        if not EVENT_REDIS.is_set():
            return None
        return bool(await self.redis.get(self.get_redis_used_key(wq_id)))

    async def set_used(self, wq_id: str) -> None:
        """Set Redis key with used state and TTL here."""
        if not EVENT_REDIS.is_set():
            return
        await self.redis.setex(
            self.get_redis_used_key(wq_id),
            #  we have over 720 funny wrong quotes, so 420 should be ok
            60 * 60 * 24 * 420,  # TTL
            1,  # True
        )


class QuoteOfTheDayRss(QuoteOfTheDayBaseHandler):
    """The request handler for the quote of the day RSS feed."""

    POSSIBLE_CONTENT_TYPES = ("application/rss+xml", "application/xml")
    IS_NOT_HTML = True

    async def get(self, *, head: bool = False) -> None:
        """Handle GET requests."""
        if head:
            return
        today = datetime.utcnow().date()
        quotes = (
            await self.get_quote_of_today(),
            *[
                await self.get_quote_by_date(today - timedelta(days=i))
                for i in range(1, 8)
            ],
        )
        await self.render(
            "rss/quote_of_the_day.xml",
            quotes=tuple(q for q in quotes if q),
        )


class QuoteOfTheDayAPI(APIRequestHandler, QuoteOfTheDayBaseHandler):
    """Handler for the JSON API that returns the quote of the day."""

    async def get(
        self,
        date_str: None | str = None,
        *,
        head: bool = False,  # pylint: disable=unused-argument
    ) -> None:
        """Handle GET requests."""
        if not EVENT_REDIS.is_set():
            raise HTTPError(503)

        quote_data = await (
            self.get_quote_by_date(date_str)
            if date_str
            else self.get_quote_of_today()
        )

        if not quote_data:
            raise HTTPError(404 if date_str else 503)

        if self.request.path.endswith("/full"):
            return await self.finish(quote_data.to_json())

        wrong_quote = quote_data.wrong_quote
        await self.finish_dict(
            date=quote_data.date.isoformat(),
            url=quote_data.get_quote_url(),
            id=wrong_quote.get_id_as_str(),
            quote=str(wrong_quote.quote),
            author=str(wrong_quote.author),
            rating=wrong_quote.rating,
        )


class QuoteOfTheDayRedirect(QuoteOfTheDayBaseHandler):
    """Redirect to the quote of the day."""

    async def get(
        self,
        date_str: None | str = None,
        *,
        head: bool = False,  # pylint: disable=unused-argument
    ) -> None:
        """Handle GET requests."""
        if not EVENT_REDIS.is_set():
            raise HTTPError(503)

        wrong_quote_data = await (
            self.get_quote_by_date(date_str)
            if date_str
            else self.get_quote_of_today()
        )

        if not wrong_quote_data:
            raise HTTPError(404 if date_str else 503)

        self.redirect(
            self.fix_url(
                wrong_quote_data.get_quote_url(),
            ),
            False,
        )
