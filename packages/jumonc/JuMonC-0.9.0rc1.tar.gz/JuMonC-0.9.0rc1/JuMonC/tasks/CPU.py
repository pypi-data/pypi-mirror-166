import logging

from typing import Dict, List, Union, Optional
from types import ModuleType

from JuMonC.tasks import Plugin


logger = logging.getLogger(__name__)


class _CPUPlugin(Plugin.Plugin): 
    
    _psutil: Optional[ModuleType]
    
    def __init__(self) -> None:
        super().__init__()
        if self.isWorking():
            self.getLoad() # make sure it is correctly init even for windows
    
    
    def _isWorking(self) -> bool:
        try:
            self._psutil = __import__('psutil')
        except ModuleNotFoundError:
            logging.warning("psutil can not be imported, therefore CPU functionality not avaiable")
            return False
        return True
    
    def getLoad(self) -> List[float]:
        if self.works is True:
            if isinstance(self._psutil, ModuleType):
                return self._psutil.getloadavg()
            logging.error("CPU plugin has no psutil module, \"getLoad\" should not be called")
            raise RuntimeError("CPU plugin has no psutil module, \"getLoad\" should not be called")
        logging.error("CPU plugin is disabled, \"getLoad\" should not be called")
        raise RuntimeError("CPU plugin is disabled, \"getLoad\" should not be called")
    
    
    def getFreq(self) -> float:
        if self.works is True:
            if isinstance(self._psutil, ModuleType):
                return self._psutil.cpu_freq().current
            logging.error("CPU plugin has no psutil module, \"getFreq\" should not be called")
            raise RuntimeError("CPU plugin has no psutil module, \"getFreq\" should not be called")
        logging.error("CPU plugin is disabled, \"getFreq\" should not be called")
        raise RuntimeError("CPU plugin is disabled, \"getFreq\" should not be called")

    def getPerc(self) -> float:
        if self.works is True:
            if isinstance(self._psutil, ModuleType):
                return self._psutil.cpu_percent()
            logging.error("CPU plugin has no psutil module, \"getPerc\" should not be called")
            raise RuntimeError("CPU plugin has no psutil module, \"getPerc\" should not be called")
        logging.error("CPU plugin is disabled, \"getPerc\" should not be called")
        raise RuntimeError("CPU plugin is disabled, \"getPerc\" should not be called")
    
    
    def getStatusData(self,
                      dataType: str, 
                      overrideHumanReadableWithValue: Optional[bool] = None) -> List[Dict[str, Union[bool, int, float ,str]]]:
        logging.debug("get CPU status data with type=%s, overrride humand readable=%s",
                     str(dataType),
                     str(overrideHumanReadableWithValue))
        if dataType == "load":
            load = self.getLoad()
            return [{"load_1": load[0],
                     "load_5": load[1],
                     "load_15": load[2]}]
        if dataType == "percent":
            percent_load = self.getPerc()
            return [{"CPU utilization": percent_load}]
        if dataType == "frequency":
            frequency = self.getFreq()
            return [{"CPU frequency": frequency}]
        return []
    
    
    def getConfigData(self,
                      dataType: str, 
                      overrideHumanReadableWithValue: Optional[bool] = None) -> List[Dict[str, Union[bool, int, float ,str]]]:
        logging.debug("get CPU config data with type=%s, overrride humand readable=%s",
                     str(dataType),
                     str(overrideHumanReadableWithValue))
        return []
    
    
plugin = _CPUPlugin()