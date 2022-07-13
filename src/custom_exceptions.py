


class TooManyPages(Exception):
    def __init__(self, message="Please narrow search with filters, too many pages!"):
        self.message = message
        super().__init__(self.message)