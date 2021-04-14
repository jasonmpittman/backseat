class ServerRestartException(Exception):
    def __init__(self, message='Server Restart!'):
        super(ServerRestartException, self).__init__(message)