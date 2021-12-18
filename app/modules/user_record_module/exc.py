from sqlalchemy.exc import NoResultFound


class RecordNotFounded(NoResultFound):
    """Запись не найдена"""

    @property
    def message(self):
        if self.args:
            return f'Запись {self.args[0]} не найдена'
        return f'Запись не найдена'


__all__ = ['RecordNotFounded']
