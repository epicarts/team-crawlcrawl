import time
import functools
import logging
from crontab import CronTab
from datetime import datetime, timedelta
import math

class JobController(object):
    @classmethod
    def run(cls, crontab): #
        """
        cls 메소드는 모르겟음. crontab "* * * * *" <- 이런식으로 넘기면됨.
        :param crontab: job schedule
        """
        def receive_func(job):
            @functools.wraps(job)
            def wrapper():

                job_settings = JobSettings(CronTab(crontab))#cronTab 에서 셋팅
                logging.info("->- Process Start")
                while True:
                    try:
                        logging.info(
                            "-?- next running\tschedule:%s" %
                            job_settings.schedule().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        time.sleep(job_settings.interval())
                        logging.info("->- Job Start")
                        job()
                        logging.info("-<- Job Done")
                    except KeyboardInterrupt:
                        break
                logging.info("-<- Process Done.")
            return wrapper
        return receive_func


class JobSettings(object):
    def __init__(self, crontab):
        """
        :param crontab: crontab.CronTab
        """
        self._crontab = crontab

    def schedule(self):
        """
        return: datetime
        """
        crontab = self._crontab
        return datetime.now() + timedelta(seconds=math.ceil(crontab.next()))

    def interval(self):
        """
        return: seconds
        """
        crontab = self._crontab
        return math.ceil(crontab.next())
