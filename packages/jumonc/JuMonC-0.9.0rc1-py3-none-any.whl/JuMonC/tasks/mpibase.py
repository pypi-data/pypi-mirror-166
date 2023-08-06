import logging

from threading import Lock
from enum import Enum

from typing import List, Any

from mpi4py import MPI

import sys


from JuMonC.tasks.taskSwitcher import task_switcher


logger = logging.getLogger(__name__)


__keep_running = True

mpi_lock = Lock()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


class MPIGatherFunctionality(Enum):
    MIN = 1
    MAX = 2
    AVERAGE = 3
    SUM = 4
    ONENODE = 5
    ALL = 6
    


def keepRunning() -> bool:
    return __keep_running

    
# stop all MPI handlers
def MPI_fin(data:List[Any]) -> None:
    global __keep_running
    logging.debug("MPI stop data: %s", str(data))
    
    __keep_running = False
    
    MPI.Finalize()
    sys.exit(0)


stop_handlers_id = task_switcher.addFunction(MPI_fin)