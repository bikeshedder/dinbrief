class Document(object):

    title = ''
    subject = ''
    author = ''
    keywords = None
    creator = 'http://pypi.python.org/pypi/dinbrief'

    sender = None
    recipient = None
    content = None
    date = ''

    def __init__(self, **kwargs):
        # Metadata
        self.title = kwargs.pop('title', self.title)
        self.subject = kwargs.pop('subject', self.subject)
        self.author = kwargs.pop('author', self.author)
        self.keywords = kwargs.pop('keywords', self.keywords)
        self.creator = kwargs.pop('creator', self.creator)
        # Content
        self.sender = kwargs.pop('sender', self.sender or [])
        self.recipient = kwargs.pop('recipient', self.recipient or [])
        self.date = kwargs.pop('date', self.date)
        self.content = kwargs.pop('content', self.content or [])
