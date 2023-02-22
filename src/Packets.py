class Packets:
    def __init__(self):
        self.received_message_info = None
        self.received_message_ip = None
        self.received_message_port = None
        self.isUpdated = False

    def set(self, **kwargs):
        self.received_message_info = kwargs["info"]
        self.received_message_ip = kwargs["ip"]
        self.received_message_port = kwargs["port"]
        self.isUpdated = True
        print("packette info:", self.received_message_info)
        print("packette ip:", self.received_message_ip)
        print("packette port:", self.received_message_port)
        print("packette isUpdated:", self.isUpdated)
