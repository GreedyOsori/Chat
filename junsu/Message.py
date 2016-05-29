class Message:
    def __init__(self, num_room, name):
        self.num_room = num_room
        self.name = name

    def set_msg(self, msg):
        self.msg = msg

    def get_msg_str(self):
        return self.num_room+"#"+self.name+"#"+self.msg
    def get_msg_info(self):
        return self.num_room, self.name, self.msg