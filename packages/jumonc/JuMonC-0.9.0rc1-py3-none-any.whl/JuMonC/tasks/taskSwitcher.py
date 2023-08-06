import logging

from queue import Queue

from typing import List, Optional, Any, Callable, Dict


from JuMonC import settings



logger = logging.getLogger(__name__)



class _taskSwitcher:
    pending_tasks: Queue = Queue(settings.PENDING_TASKS_SOFT_LIMIT + settings.MAX_THREADS_PER_TASK * settings.MAX_WORKER_THREADS + 1)
    
    def __init__(self) -> None:
        self.max_id = 0
        """Singelton class that switches taks depending on id."""
        self.switch_dic: Dict[int, Callable[..., Any]] = {}
        
        self.inverse_dic_update_needed = False
        self.inverse_switch_dic: Dict[Callable[..., Any], int] = {}
        
    def executeNextTask(self) -> None:
        data = self.pending_tasks.get()
        self.executeTask(data)
        self.pending_tasks.task_done()
        
    def executeTask(self, data: List[Any]) -> None:
        logging.debug("Executing task: %s", str(data))
        task = self.switch_dic.get(data[0], lambda data: logging.warning("Invalid taskID: %s", str(data[0])))
        task(data)
        
    def addTask(self, data: Optional[List[Any]]) -> None:
        logging.debug("Adding task with data: %s", str(data))
        if data is not None:
            if data[1] == -1:
                self.executeTask(data)
            else:
                self.pending_tasks.put(data)
            return
        logging.info("added task has no data")
    
    def addFunction(self, func: Callable[..., Any]) -> int:
        logging.debug("Adding function: %s", str(func))
        self.max_id = self.max_id + 1
        self.switch_dic[self.max_id] = func
        self.inverse_dic_update_needed = True
        logging.debug("function ID: %s", str(self.max_id))
        return self.max_id
    
    def get_function_id(self, func: Callable[..., Any]) -> int:
        if self.inverse_dic_update_needed:
            self.inverse_switch_dic = {function: func_id for func_id, function in self.switch_dic.items()}
        return self.inverse_switch_dic[func]


task_switcher = _taskSwitcher()