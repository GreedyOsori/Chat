import json

##tmp
PORT = 1111

## client & server
ACTION_VAL = 'action_value'
ACTION = 'action'
ID = 'id'

CREATE = 'create'
JOIN = 'join'
SEND_MSG = 'send_msg'
BROADCAST = 'broadcast'
OUT = 'out'
EXIT = 'exit'

## server only
SYS_MSG = 'sys_msg'

ACCEPTED = 'accepted'
DENIED = 'denied'

############
BUF_SIZE = 256
DELIM = '#'


def dump(c_id, message):
    p = str(message).split('#', 1)

    if (p[0] == OUT) | (p[0] == EXIT) | (p[0] == BROADCAST) | (p[0] == CREATE) | (p[0] == JOIN) | (p[0] == SYS_MSG):
        if len(p) == 1:
            return json.dumps({ID: '', ACTION: SYS_MSG, ACTION_VAL: DENIED})
        return json.dumps({ID: c_id, ACTION: p[0], ACTION_VAL: p[1]})
    else:
        return json.dumps({ID: c_id, ACTION: SEND_MSG, ACTION_VAL: p[0]})


def load(message):
    return json.loads(message)

