import schedule

from . import jobs


def add_all_jobs(bot, configs):
    """Добавить все задачи в расписание."""
    schedule.every(1).seconds.do(jobs.delete_expire_message,
                                 bot=bot,
                                 expire_message_time=configs.MESSAGE_EXPIRE_TIME,
                                 )
