import logging

from typing import Dict, Iterable, Tuple, Optional

from JuMonC import settings

logger = logging.getLogger(__name__)

_working_plugins: Dict[str, bool] = {}

_plugins_valid_mpi_ids: Dict[str, Dict[str, int]] = {}
__used_mpi_ids = 5 * settings.MPI_IDs_per_plugin


def addMPIIDsForPlugin(pluginName: str) -> Tuple[int, int]:
    global __used_mpi_ids
    mpiInfo = {"min": __used_mpi_ids,
                                          "max": __used_mpi_ids + settings.MPI_IDs_per_plugin - 1,
                                          "next": __used_mpi_ids}
    __used_mpi_ids = __used_mpi_ids + settings.MPI_IDs_per_plugin
    _plugins_valid_mpi_ids[pluginName] = mpiInfo
    
    MPIIDMin = mpiInfo["min"]
    MPIIDMax = mpiInfo["max"]
    return (MPIIDMin, MPIIDMax)


def getNextMPIID(pluginName: str) -> Optional[int]:
    mpiID:int = _plugins_valid_mpi_ids[pluginName]["next"]
    _plugins_valid_mpi_ids[pluginName]["next"] = mpiID + 1
    if mpiID < _plugins_valid_mpi_ids[pluginName]["max"]:
        return mpiID
    logging.error("plugin \"%s\" is trying to allocate to many mpiIDs, this resulted in an error", pluginName)
    return None


def getMPIIdsRangeForPlugin(pluginName: str) -> Tuple[int, int]:
    MPIIDMin = _plugins_valid_mpi_ids[pluginName]["min"]
    MPIIDMax = _plugins_valid_mpi_ids[pluginName]["max"]
    return (MPIIDMin, MPIIDMax)


def addPluginStatus(pluginName: str, working: bool) -> None:
    if pluginName not in _working_plugins:
        _working_plugins[pluginName] = working
    else:
        logging.error("Setting the working status for the plugin \"%s\" second time", pluginName)


def pluginIsWorking(pluginName: str) -> bool:
    return _working_plugins[pluginName]


def disablePlugin(pluginName: str) -> None:
    _working_plugins[pluginName] = False


def get_plugin_items() -> Iterable[Tuple[str, bool]]:
    return _working_plugins.items()


flask_path_reg = False
