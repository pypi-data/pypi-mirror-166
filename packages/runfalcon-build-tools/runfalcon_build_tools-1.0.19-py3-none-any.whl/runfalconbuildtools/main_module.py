from array import array

class MainCommand:

    def __init__(self, command:str, operation:str):
        self.command = command
        self.operation = operation

class ModuleMain:

    def __init__(self, commnad_args:array):
        self.command_args = commnad_args

    def run(self):
        for arg in self.command_args:
            print('>>>>>>>> ' + arg)
