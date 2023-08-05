import os
import logging
import eons as e
from dotdict import dotdict
from pathlib import Path

######## START CONTENT ########
# All errors
class FittingError(Exception): pass


# Exception used for miscellaneous errors.
class OtherFittingError(FittingError): pass



#Interface method for use in other python code.
def connect(fitting, input={}, **kwargs):
    connector = Connector()
    return connector(fitting, input, **kwargs)

class Connector(e.Executor):

    def __init__(this):
        super().__init__(name="Pipe Adapter", descriptionStr="An eons adapter for Pipedream")

        #Spoof args, since we won't be using this on the command line.
        this.args = dotdict({
            'no_repo': False,
            'verbose': 1,
            'quiet': 0,
            'config': None
        })

        #Outputs are consolidated from Fitting.
        this.output = {}


    #Configure class defaults.
    #Override of eons.Executor method. See that class for details
    def Configure(this):
        super().Configure()
        this.defaultRepoDirectory = str(Path("/tmp/fittings").resolve())

    #Override eons.UserFunctor Call method to add arguments when called by other python functions.
    def __call__(this, fitting, input={}, **kwargs) :
        this.fittingName = fitting
        this.input = input
        super().__call__(**kwargs)
        return this.output #set in UserFunction()

    #Disable argument parsing, since this will not be called from the command line.
    def ParseArgs(this):
        pass

    #Override of eons.Executor method. See that class for details
    def UserFunction(this):
        super().UserFunction()
        fitting = this.GetRegistered(this.fittingName, "fitting")
        fitting(executor=this, input=this.input, **this.kwargs)
        this.output = fitting.output

    # Will try to get a value for the given varName from:
    #    first: this.
    #    second: extra arguments provided to *this.
    #    third: the config file, if provided.
    #    fourth: the environment (if enabled).
    # RETURNS the value of the given variable or default.
    def Fetch(this, varName, default=None, enableThis=True, enableArgs=True, enableConfig=True, enableEnvironment=True):
        logging.debug(f"Fetching {varName}...")

        if (enableThis and hasattr(this, varName)):
            logging.debug(f"...got {varName} from {this.name}.")
            return getattr(this, varName)

        if (enableArgs):
            for key, val in this.kwargs.items():
                if (key == varName):
                    logging.debug(f"...got {varName} from argument.")
                    return val

        if (enableConfig and this.config is not None):
            for key, val in this.config.items():
                if (key == varName):
                    logging.debug(f"...got {varName} from config.")
                    return val

        if (enableEnvironment):
            envVar = os.getenv(varName)
            if (envVar is not None):
                logging.debug(f"...got {varName} from environment")
                return envVar

        logging.debug(f"...could not find {varName}; using default ({default})")
        return default

class Fitting(e.UserFunctor):
    def __init__(this, name=e.INVALID_NAME()):
        super().__init__(name)

        this.enableRollback = False

        # Populate this with anything you want to return.
        this.output = {}


    # Run inputs through *this fitting!
    # i.e. do work.
    # Override this or die.
    def Run(this):
        pass


    # Override this to perform whatever success checks are necessary.
    def DidRunSucceed(this):
        return True


    # API compatibility shim
    def DidUserFunctionSucceed(this):
        return this.DidRunSucceed()


    # Hook for any pre-run configuration
    def PreRun(this):
        pass


    # Hook for any post-run configuration
    def PostRun(this):
        pass


    # Override of eons.UserFunctor method. See that class for details.
    def ParseInitialArgs(this):
        super().ParseInitialArgs()
        this.input = this.kwargs.pop('input')


    # Override of eons.Functor method. See that class for details
    def UserFunction(this):
        this.PreRun()

        logging.debug(f"<---- Running {this.name} ---->")
        this.Run()
        logging.debug(f">---- Done running {this.name} ----<")

        this.PostRun()


    # Will try to get a value for the given varName from:
    #    first: this
    #    second: the input map provided
    #    third: the executor (args > config > environment)
    # RETURNS the value of the given variable or None.
    def Fetch(this,
        varName,
        default=None,
        enableThis=True,
        enableExecutor=True,
        enableArgs=True,
        enableExecutorConfig=True,
        enableEnvironment=True,
        enableInput=True):
            
        # Duplicate code from eons.UserFunctor in order to establish precedence.
        if (enableThis and hasattr(this, varName)):
            logging.debug("...got {varName} from self ({this.name}).")
            return getattr(this, varName)

        if (enableInput):
            for key, val in this.input.items():
                if (key == varName):
                    logging.debug(f"...got {varName} from input.")
                    return val

        return super().Fetch(varName, default, enableThis, enableExecutor, enableArgs, enableExecutorConfig, enableEnvironment)

