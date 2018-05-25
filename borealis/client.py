import threading
import zmq
import pickle

class Client(threading.Thread):

    def __init__(self, identity, remote_address="localhost", remote_port=5570):
        threading.Thread.__init__(self)
        self.identity = ('{}{}'.format('id_', identity)).encode()
        self.remote_address = remote_address
        self.remote_port = remote_port

        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        socket.setsockopt(zmq.IDENTITY, self.identity)
        socket.connect('tcp://{}:{}'.format(self.remote_address, self.remote_port))
        #socket.connect("inproc://1")
        print('Client {} started\n'.format(self.identity))
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        self.poll = poll
        self.socket = socket
        self.context = context

    def run(self, message=None):

        self.socket.send(message)
        #print('Req from client {} sent.\n'.format(self.identity))
        return
        received_reply = False
        while not received_reply:
            sockets = dict(self.poll.poll(1000))
            if self.socket in sockets:
                if sockets[self.socket] == zmq.POLLIN:
                    msg = self.socket.recv()
                    #print('Client {} received reply: {}\n'.format(self.identity, msg))
                    del msg
                    received_reply = True

    def close(self):

        self.socket.close()
        self.context.term()

import time

def run_test(N=10, items=100):

    c = Client(1)
    message = pickle.dumps(list(range(0,items)))
    start = time.time()
    for i in range(N):
        c.run(message=message)
    c.run(message=b'end')
    delta = time.time() - start

    print("Launched {} requests in {}s with task rate of {}.Tasks/s".format(N, delta, float(N)/delta))


if __name__ == "__main__" :

    run_test(N=1000)
    run_test(N=10000)
    run_test(N=100000)

