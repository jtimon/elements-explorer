
from zmq import (
    ZMQError, DONTWAIT, 
    REQ, REP, PUB, PUSH, PULL, PUB, SUB, XREQ, XREP, 
    FORWARDER, STREAMER, QUEUE,
    SUBSCRIBE,
)

def Context(gevent=False, *args, **kwargs):
    if gevent:
        from zmq.green import Context        
    else:
        from zmq import Context        
    return Context(*args, **kwargs)

def device(device_type, frontend, backend, gevent=False):
    if gevent:
        from zmq.green import device        
    else:
        from zmq import device   
    device(device_type, frontend, backend)
