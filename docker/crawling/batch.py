# -*- coding: utf-8 -*-

import logging
from multiprocessing import Pool
from crontab_scheduler import JobController

# Docker ImageのTimezoneがUTCなので注意！  
@JobController.run("* * * * *")# 내 생각으로 cron 기능일듯...
def notice_tmr_club():
    """
    タモリ倶楽部の時間だお(東京)
    :return: None
    """
    logging.info("タモリ倶楽部はじまるよ！！！")


# Docker ImageのTimezoneがUTCなので注意！(大切なので2回言いました)
@JobController.run("10 * * * *")
def notice_baseball():
    """
    やきうの時間を教えるお
    :return: None
    """
    logging.info("やきうの時間だあああ！！！！")


def main():
    """
    crontab method
    :return: None
    """
    logging.basicConfig(
        level=logging.INFO,
        format="time:%(asctime)s.%(msecs)03d\tprocess:%(process)d" + "\tmessage:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # crontabで実行したいジョブを登録
    jobs = [notice_tmr_club, notice_baseball]

    # multi process running
    p = Pool(len(jobs))
    
    try:
        for job in jobs: # noticetmr_club에 대한 job과 jobs 실행.
            p.apply_async(job)
        p.close()
        p.join()
    except KeyboardInterrupt:
        logging.info("exit")


if __name__ == '__main__':
    main()