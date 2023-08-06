"""The module reserved for the decorators available by the Herodotus package"""

import copy
from typing import Any, Callable, Dict, Generator, Optional
from scrapy.selector.unified import Selector
from sqlalchemy.orm import Session
from sqlalchemy import Table


def parse_for_db(
    parse_method: Callable[[Selector, Optional[Any]], Generator[Any, None, None]],
    session: Session,
    **kwargs: Optional[Any]
) -> Generator[Dict[str, Any], None, None]:
    """Decorator for Scrapy Spider parsing method for automatically storing data into
    the database

    Args:
        parse_method (Callable[[Response], Iterator[registry]]): the method to parse the
        HTTP response into data to store
        response (Response): the HTTP response to be parsed
        session (Session): the SQLAlchemy session to store the data into the database

    Yields:
        Iterator[Dict[str, Any]]: the stored objects iterator
    """
    response = kwargs.pop("response")

    result: Table

    for result in parse_method(response, **kwargs):  # type: ignore

        result_payload = copy.deepcopy(vars(result))
        result_payload.pop("_sa_instance_state")

        session.add(result)  # type: ignore

        yield result_payload
