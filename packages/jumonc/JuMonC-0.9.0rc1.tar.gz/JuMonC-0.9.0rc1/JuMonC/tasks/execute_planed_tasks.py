import logging

from threading import Thread, Condition

import urllib.request
import urllib.error

import json

from typing import Optional

from JuMonC import settings
from JuMonC.models import planed_tasks


logger = logging.getLogger(__name__)


__scheduling_lock = Condition()
_scheduling_thread:Optional[Thread]
_keep_running = True

def new_task() -> None:
    with __scheduling_lock:
        __scheduling_lock.notify()


def init_scheduling() -> None:
    #global _new_task_function
    if settings.SCHEDULED_TASKS_ENABLED:
        planed_tasks.set_new_task_callback(new_task)
        _scheduling_thread = Thread(target = __scheduling_worker)
        _scheduling_thread.start()


def __scheduling_worker() -> None:
    while True:
        taskinfo = planed_tasks.get_next_task_and_time()
        logging.debug("Next scheduled task with id %i and waiting time %i", taskinfo[1], taskinfo[0])
        with __scheduling_lock:
            while taskinfo[0] <= 0 and _keep_running:
                _execute_task(taskinfo[1], taskinfo[2])
                taskinfo = planed_tasks.get_next_task_and_time()
                logging.debug("Next scheduled task with id %i and waiting time %i", taskinfo[1], taskinfo[0])
            if _keep_running:
                logging.debug("Sleeping time %s", str(taskinfo[0]/1000))
                __scheduling_lock.wait(timeout = taskinfo[0]/1000) # wait time in seconds
            else:
                return


def _execute_task(ID:int, task:str) -> None:
    logging.debug("Executing task \"%s\" with id: %i", task, ID)
    url = "http://localhost:" + str(settings.REST_API_PORT) + task + "&prefer_id=True"
    if (url.startswith("http://") or url.startswith("https://")) and "file:/" not in url:
        req = urllib.request.Request(url)
    else:
        logging.error("Non viable url, due to a security risk this scheduled job will be cancled, id: %i, task: \"%s\"", id, task)
        planed_tasks.cancel(ID)
        return
    logging.debug("Accessing \"%s\" now", req.get_full_url())
    try:
        # Disable bandit checking in this line, because the url is checked to prevent the opening of files.
        with urllib.request.urlopen(req) as response: #nosec B310
            text = response.read()
            text = text.decode("utf8", 'ignore')
            textDic = json.loads(text)
            
            planed_tasks.task_executed(ID, response.getcode(), textDic["cache_id"])
            #print(textDic)
            #planed_tasks.task_executed(ID, response.getcode(), -1)
    except urllib.error.HTTPError as exception:
        http_status = exception.getcode()
        if http_status is None:
            http_status = 404
            logging.warning("No http error code even with execution error in scheduled task: %s", task)
        planed_tasks.task_executed(ID, http_status, -1)
        logging.warning("Execution error with scheduled task: %s", task)
    except urllib.error.URLError:
        planed_tasks.task_executed(ID, 404, -1)
        logging.warning("Execution error with scheduled task: %s", task)
        