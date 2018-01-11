from Virtualizer.VirtualMachine import VM
from Virtualizer.Manager import VirtualManager

import json

# Easy status reporting to the caller
class Status():
    SUCCESS = "success"
    FAILURE = "failure"

class Response():
    status = Status.FAILURE
    reason = ""

    def __init__(self, status, message, data={}):
        self.status = status
        self.message = message      
        self.data = data


    # Function for creating a response json that can be send back to
    # the requester
    def respond(self):
        resp = json.dumps(
            {
                "status": self.status,
                "message": self.message,
                "data": self.data
            }
        )
        return resp

class API:

    # Ready Config.ini for all of the data
    def __init__(self, data):
        settings = data['GENERAL']
        resources = data['RESOURCES']

        self.name = settings['app_name']
        self.version = settings["api_version"]
        self.cores = int(resources['cores'])
        self.memory = int(resources['memory'])
        self.storage = int(resources['storage'])
        self.vmstack = []
        self.manager = VirtualManager()

    # Returns the API info in json format
    def getAPIInfo(self):
        info = {
            "appname": self.name,
            "version": self.version,
            "resources": {
                "cores": self.cores,
                "memory": self.memory,
                "storage": self.storage
            }
        }

        return info
    
    # Calculates the total resources used by the existing vm's and
    # returns True or False based on if the new vm will still fit on
    # this server
    def doesItFit(self, toAllocate):
        totalUsedCores = 0
        totalUsedMemory = 0
        totalUsedStorage = 0


        for vm in self.vmstack:
            totalUsedCores += vm.cores
            totalUsedMemory += vm.memory
            totalUsedStorage += vm.storage
        
        return self.cores - totalUsedCores > toAllocate[0] and \
        self.memory - totalUsedMemory > toAllocate[1] and \
        self.storage - totalUsedStorage > toAllocate[2]

    # Wrapper function that tries to match the uuid with a vm and
    # executes the given function with the found vm
    def VMFunctionWrapper(self, function, data):
        try:
            # Try to match the 
            for vm in self.vmstack:
                if vm.matchUUID(data['uuid']):
                    kwargs = {"vm": vm}
                    res = getattr(self.manager, function)(**kwargs)
                    return Response(Status.SUCCESS, "Action succesfully applied: " + function).respond()

            return Response(Status.FAILURE, "VM Not Found").respond()
            
        except Exception as e:
            return Response(Status.FAILURE, "Exception while trying to " + function, {"exception": str(e)}).respond()

    # Function for cerating a vm using provided data, it creates an object
    # and gives VirtualManager a signal to create the VM
    def createVM(self, data):
        vm = VM(data)
        try:
            self.vmstack.append(
                vm
            )
        except ValueError:
            return "Missing tag in data, please check if you specify the following:"
        
        # Tell the manager to creatae the vm
        self.manager.createVM(vm)

        return Response(Status.SUCCESS, "VM Succesfully created", {"uuid": vm.uuid}).respond()

    def rebootVM(self, data):
        return self.VMFunctionWrapper("rebootVM", data)

    def shutdownVM(self, data):
        return self.VMFunctionWrapper("shutdownVM", data)

    def startVM(self, data):
        return self.VMFunctionWrapper("startVM", data)

    def destroyVM(self, data):
        return self.VMFunctionWrapper("destroyVM", data)

