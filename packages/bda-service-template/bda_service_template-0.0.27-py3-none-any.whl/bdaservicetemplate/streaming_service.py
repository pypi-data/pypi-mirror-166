from .generic_service import GenericService
from bdaserviceutils import HttpHealthServer

class StreamingService(GenericService):

    def __init__(self):
        super().__init__()
        HttpHealthServer.run_thread()
