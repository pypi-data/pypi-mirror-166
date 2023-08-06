from .websocket_server import WebsocketServer
from .serverRootHandlers import serverRootHandlers
from .serverInternalHandlers import serverInternalHandlers

class server:
    def __init__(self, parentCl, enable_logs=True):
        # Read the CloudLink version from the parent class
        self.version = parentCl.version

        # Init the server
        self.userlist = []
        self.motd_enable = False
        self.motd_msg = ""
        self.global_msg = ""
        self.roomData = {
            "default": set()
        }
        
        # Init modules
        self.supporter = parentCl.supporter(self, enable_logs, 1)
        self.serverRootHandlers = serverRootHandlers(self)
        self.serverInternalHandlers = serverInternalHandlers(self)
        
        # Load built-in commands (automatically generates attributes for callbacks)
        self.builtInCommands = []
        self.customCommands = []
        self.disabledCommands = []
        self.usercallbacks = {}
        self.supporter.loadBuiltinCommands(self.serverInternalHandlers)

        # Extra configuration
        self.ipblocklist = [] # Use to block IP addresses
        self.rejectClientMode = False # Set to true to reject future clients until false
        
        # Create API
        self.loadCustomCommands = self.supporter.loadCustomCommands
        self.disableCommands = self.supporter.disableCommands
        self.sendPacket = self.supporter.sendPacket
        self.sendCode = self.supporter.sendCode
        self.linkClientToRooms = self.supporter.linkClientToRooms
        self.unlinkClientFromRooms = self.supporter.unlinkClientFromRooms
        self.getAllUsersInRoom = self.supporter.getAllUsersInRoom
        self.getAllUsersInManyRooms = self.supporter.getAllUsersInManyRooms
        self.getAllRooms = self.supporter.getAllRooms
        self.getAllClientRooms = self.supporter.getAllClientRooms
        self.getUsernames = self.supporter.getUsernames
        self.setClientUsername = self.supporter.setClientUsername
        self.log = self.supporter.log
        self.callback = self.supporter.callback
        
        # Create callbacks, command-specific callbacks are not needed in server mode
        self.on_packet = self.serverRootHandlers.on_packet
        self.on_connect = self.serverRootHandlers.on_connect
        self.on_close = self.serverRootHandlers.on_close

        self.log("Cloudlink server initialized!")

    def run(self, port=3000, host="127.0.0.1"):
        # Initialize the Websocket Server
        self.log("Cloudlink server starting up now...")
        self.wss = WebsocketServer(host, port)

        # Bind built-in callbacks
        self.wss.set_fn_new_client(self.serverRootHandlers.on_connect)
        self.wss.set_fn_message_received(self.serverRootHandlers.on_packet)
        self.wss.set_fn_client_left(self.serverRootHandlers.on_close)

        # Create attributes
        self.all_clients = self.wss.clients

        # Run the CloudLink server
        self.wss.run_forever()
        self.log("Cloudlink server exiting...")

    def setMOTD(self, enable:bool, msg:str):
        self.motd_enable = enable
        self.motd_msg = msg

    
