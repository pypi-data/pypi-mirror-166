import logging

from mpi4py import MPI

from typing import Any, List, Optional, Tuple


from JuMonC.tasks import taskPool
from JuMonC.tasks.taskSwitcher import task_switcher
from JuMonC.models import dataStore
from JuMonC.tasks import mpibase



logger = logging.getLogger(__name__)



__comm = MPI.COMM_WORLD



def waitForCommands() -> None:
    taskPool.setupTaskPool()
    while mpibase.keepRunning():
        task_switcher.executeNextTask()


def sendCommand(data: List[int]) -> None:
    logging.debug("sending mpi command with data: %s", str(data))
    __comm.bcast(data, root=0)
    task_switcher.addTask(data)


def gatherResult(dataID: int, command: List[int]) -> None:
    mpiOperation = 4
    
    with mpibase.mpi_lock:

        if mpiOperation == mpibase.MPIGatherFunctionality.ONENODE.value:
            pass

        __comm.bcast(dataID, root=0)
        (rec_res_avai, result) = __testResultAvaiable(dataID)
        if rec_res_avai == 1:
            if mpiOperation == mpibase.MPIGatherFunctionality.MIN.value:
                resultCom = __comm.reduce(result, op = MPI.MIN, root = 0)
            elif mpiOperation == mpibase.MPIGatherFunctionality.MAX.value:
                resultCom = __comm.reduce(result, op = MPI.MAX, root = 0)
            elif mpiOperation == mpibase.MPIGatherFunctionality.AVERAGE.value:
                resultCom = __comm.reduce(result, op = MPI.SUM, root = 0)
                if isinstance(resultCom,(int, float)):
                    resultCom = resultCom / __comm.Get_size()
                else:
                    logging.error("MPI reduce did not return a number as expected")
                    return
            elif mpiOperation == mpibase.MPIGatherFunctionality.SUM.value:
                resultCom = __comm.reduce(result, op = MPI.SUM, root = 0)
            elif mpiOperation == mpibase.MPIGatherFunctionality.ALL.value:
                pass
            dataStore.removeResult(dataID)
            dataStore.addResult(dataID, resultCom)
        else: 
            logging.info("Gathering resheduled, command: %s", str(command))
            #taskSwitcher.tasks.add(command)
    
    


        
def __testResultAvaiable(dataID: int) -> Tuple[int, Optional[Any]]:
    result_avaiable: int = 0
    result: Optional[Any] = None
    try:
        result = dataStore.getResult(dataID)
        result_avaiable = 1
    except KeyError:
        result_avaiable = 0

    rec_res_avai: int = 0
    __comm.Allreduce(result_avaiable, rec_res_avai, op=MPI.PROD)
    return (rec_res_avai, result)