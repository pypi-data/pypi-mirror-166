import logging

from typing import List, Any, Callable

#from mpi4py import MPI

from functools import wraps


from JuMonC.tasks import mpibase, mpiroot
from JuMonC.tasks.taskSwitcher import task_switcher


logger = logging.getLogger(__name__)

def build_mpi_command(mpi_id: int, block_communication:bool = False) -> List[int]:
    logging.debug("mpi command with: %i, %s", mpi_id, str(block_communication))
    return [mpi_id]


def multi_node_information(func: Callable[..., float]) -> Callable[..., float]:
    @wraps(func)
    def decorated_function(*args: Any, **kwargs: Any) -> float:
        if mpibase.size == 1:
            return func(*args, **kwargs)
        if mpibase.rank == 1:
            mpi_id = task_switcher.get_function_id(func)
            mpiroot.sendCommand(build_mpi_command(mpi_id))
        
        return func(*args, **kwargs)
            
    return decorated_function 
