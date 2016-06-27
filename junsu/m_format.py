import json

##tmp
PORT = 1111

ACTION_VAL = 'action_value'

ACTION = 'action'

ID = 'id'

SYS_MSG = 'sys_msg'
CREATE = 'create'
JOIN = 'join'
SEND_MSG = 'send_msg'
BROADCAST = 'broadcast'
OUT = 'out'
EXIT = 'exit'

ACCEPTED = 'accepted'
DENIED = 'denied'

############
BUF_SIZE = 256

def dump(id, message):
    p = str(message).split('#')

    if (p[0] == 'out') | (p[0] == 'exit') | (p[0] == 'broadcast') | (p[0] == 'create') | (p[0] == 'join') | (p[0] == 'sys_msg'):
        return json.dumps({ID: id, ACTION: p[0], ACTION_VAL: p[1]})
    else:
        return json.dumps({ID: id, ACTION: SEND_MSG, ACTION_VAL: p[0]})

def load(message):
    return json.loads(message)

