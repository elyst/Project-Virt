from uuid import uuid4

class VM:

    def __init__(self, data):
        # Check if all the needed tags are present
        if 'cores' not in data:
            raise ValueError("No tag for cores found in data")
        if 'memory' not in data:
            raise ValueError("No tag for memory found in data")
        if 'storage' not in data:
            raise ValueError("No tag for storage found in data")
        if 'name' not in data:
            raise ValueError("No tag for name found in data")

        self.cores = data['cores']
        self.memory = data['memory']
        self.storage = data['storage']
        self.name = data['name']
        self.uuid = str(uuid4().urn).replace("urn:uuid:", "")

        print(self.uuid)

    def matchUUID(self, uuid):
        print(uuid)
        print(self.uuid)

        if uuid == self.uuid:
            return True
        return False

    def getProperties(self):
        return {
            "name": self.name,
            "cores": self.cores,
            "memory": self.memory,
            "storage": self.storage,
            "uuid": self.uuid
        }