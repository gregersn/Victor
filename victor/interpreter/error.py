from .position import Position


class Error(BaseException):
    def __init__(self,
                 pos_start: Position,
                 pos_end: Position,
                 name: str,
                 details: str):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.name = name
        self.details = details

    def __str__(self):
        return (f'{self.name}: {self.details}' +
                f' at {self.pos_start.ln}, {self.pos_start.col}')


class IllegalCharError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details: str):
        super().__init__(pos_start, pos_end, "Illegal character", details)
