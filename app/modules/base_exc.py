class WrongFormat(ValueError):
    """Неверный формат"""

    @property
    def message(self):
        """Сообщение об ошибке"""
        if self.args:
            return f'Запись "{self.args[0]}" имеет неверный формат'
        return f'Запись имеет неверный формат'


class CommandNotFounded(ValueError):
    """Команда не найдена"""

    @property
    def message(self):
        """Сообщение об ошибке"""
        if len(self.args) > 1:
            return f'Команда "{self.args[0]}" не найдена в "{self.args[1]}"'
        return f'Команда не найдена'


class CommandDoesNotExist(ValueError):
    """Команда не существует"""

    @property
    def message(self):
        """Сообщение об ошибке"""

        if self.args:
            return f'Команда {self.args[0]} недоступна в боте.\n' \
                   'Ознакомиться с командами можно, перейдя по /start'

        return 'Такая команда недоступна в боте.\n' \
               'Ознакомиться с командами можно, перейдя по /start'
