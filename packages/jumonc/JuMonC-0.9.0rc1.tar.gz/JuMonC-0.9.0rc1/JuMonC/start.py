import logging

import mpi4py
from mpi4py import MPI

from threading import Thread

import sys

from typing import Any


from JuMonC import settings
from JuMonC._version import __version__, __REST_version__, __DB_version__
from JuMonC.helpers.startup import checkIfPluginsAreWorking, communicateAvaiablePlugins, setPluginMPIIDs
from JuMonC.helpers.cmdArguments import parseCMDOptions
from JuMonC.helpers.PluginManager import addAllPathsAsPlugins, initPluginsREST



logger = logging.getLogger(__name__)

mpi4py.rc.threads = True
mpi4py.rc.thread_level = "serialized"

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def startJuMonC() -> None:
    parseCMDOptions(sys.argv[1:])
    
    logging.info("Running JuMonC with version: %s", __version__)
    logging.debug("Running JuMonC with REST-API version: %s", __REST_version__)
    logging.debug("Running JuMonC with DB version: %s", __DB_version__)
    
    addAllPathsAsPlugins()
    checkIfPluginsAreWorking()
    workingPlugins = communicateAvaiablePlugins()
    logging.debug("Pluggins communicated on node %i", rank)
    
    setPluginMPIIDs(workingPlugins)

    #pylint: disable=import-outside-toplevel
    if rank == 0:
        from JuMonC.handlers.base import RESTAPI
        from JuMonC.handlers import main
    
        from JuMonC.tasks import mpiroot, execute_planed_tasks
        from JuMonC.models.cache.database import Base, engine, db_session
        from JuMonC.handlers.base import setRESTVersion
        from JuMonC.authentication.tokens import registerTokens
    
        registerTokens()

        setRESTVersion()
        main.registerRestApiPaths()
        initPluginsREST()

        if settings.SSL_ENABLED:
            JuMonC_SSL = settings.SSL_MODE
        else:
            JuMonC_SSL = None

        flask_thread = Thread(target=RESTAPI.run, kwargs={'debug': True, 'port': settings.REST_API_PORT, 'use_reloader': False, 'ssl_context': JuMonC_SSL})
        flask_thread.start()
        
        from JuMonC.models.cache import dbmodel
        Base.metadata.create_all(bind=engine)
        dbmodel.check_db_version()

        @RESTAPI.teardown_appcontext
        def shutdown_session(exception:Any = None) -> None:
            db_session.remove()
            if exception:
                logging.warning("DB connection close caused exception: %s", str(exception))
        
        
        execute_planed_tasks.init_scheduling()
    
    
        mpiroot.waitForCommands()
    
    
        flask_thread.join()
    
    else:
        from JuMonC.tasks import mpihandler
    
        mpihandler.waitForCommands()
    #pylint: enable=import-outside-toplevel
        
