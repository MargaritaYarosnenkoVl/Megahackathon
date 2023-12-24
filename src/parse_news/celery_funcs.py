from celery import shared_task
import logging
import subprocess
import json
# from .schemas import SpiderOrigin, UserName

logger = logging.getLogger('app')


@shared_task()
def launch_spider(origin: str, username: str):
    origin_spiders = {"naked-science.ru": "naked_science",
                      "cnews.ru": "cnews",
                      "fontanka.ru": "fontanka",
                      "dimonvideo.ru": "dimonvideo",
                      "3dnews.ru": "news3d",
                      "forbes.ru": "forbes",
                      "knife.media": "knife_media",
                      "nplus1.ru": "nplus1",
                      "portal-kultura.ru": "portal_kultura",
                      "sdelanounas.ru": "sdelanounas",
                      "snob.ru": "snob",
                      "techno-news.ru": "techno_news",
                      "windozo.ru": "windozo"}
    spidername = origin_spiders.get(origin)
    # spidername = origin.__dict__.get("parsed_from").__dict__.get("_name_")
    try:
        logger.info(f"Try to launch spider {spidername} by {username}")
        proc_result = subprocess.run([f"curl",
                                      f"http://localhost:6800/schedule.json",
                                      f"-d",
                                      f"project=parse_news",
                                      f"-d",
                                      f"spider={spidername}",
                                      f"-d",
                                      f"username={username}",
                                      f"-d",
                                      f"spidername={spidername}",
                                      ], stdout=subprocess.PIPE,
                                     cwd="/home/alexander/PycharmProjects/Megahackathon_T17/src/parse_news/parse_news")
        params = json.loads(proc_result.stdout)
        job_id = params["jobid"]
        logger.info(f"Spider {spidername} is launched by {username} with params = {params}")
        print("OK", "Please, wait while parser is working. JobID: ", job_id)
        return job_id
    except Exception as e:
        print(e)
        logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}
