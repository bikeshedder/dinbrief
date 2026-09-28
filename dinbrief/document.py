from collections.abc import Sequence
from typing import Any

from reportlab.platypus import Flowable


class Document:
    title: str = ""
    subject: str = ""
    author: str = ""
    keywords: str | Sequence[str] | None = None
    creator: str = "https://pypi.org/project/dinbrief/"

    sender: Sequence[str] = ()
    recipient: Sequence[str] = ()
    infobox: Sequence[Flowable] = ()
    content: Sequence[Flowable] = ()
    date: str = ""

    def __init__(
        self,
        *,
        title: str | None = None,
        subject: str | None = None,
        author: str | None = None,
        keywords: str | Sequence[str] | None = None,
        creator: str | None = None,
        sender: Sequence[str] | None = None,
        recipient: Sequence[str] | None = None,
        infobox: Sequence[Flowable] | None = None,
        date: str | None = None,
        content: Sequence[Flowable] | None = None,
        # Unknown arguments have always been ignored.
        **kwargs: Any,
    ):
        # Metadata
        self.title = title if title is not None else self.title
        self.subject = subject if subject is not None else self.subject
        self.author = author if author is not None else self.author
        self.keywords = keywords if keywords is not None else self.keywords
        self.creator = creator if creator is not None else self.creator
        # Content
        self.sender = sender if sender is not None else list(self.sender)
        self.recipient = recipient if recipient is not None else list(self.recipient)
        self.infobox = infobox if infobox is not None else list(self.infobox)
        self.date = date if date is not None else self.date
        self.content = content if content is not None else list(self.content)
