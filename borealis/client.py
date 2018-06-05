import threading
import zmq
import pickle
import argparse

class Client(threading.Thread):

    def __init__(self, identity, remote_address="localhost", remote_port=55055):
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

def run_test(N=10, items=100, server=None):

    c = Client(1, remote_address=server)
    message = pickle.dumps(list(range(0,items)))
    start = time.time()
    rtts = []

    for i in range(N):
        _start = time.time()
        c.run(message=message)
        _delta = time.time() - _start
        rtts.append(_delta)

    c.run(message=b'end')
    delta = time.time() - start

    print("RTTs min:{} ms max:{} ms avg:{} ms".format(min(rtts)*1000, max(rtts)*1000, sum(rtts)*1000/len(rtts)))
    print("Launched {} requests in {}s with task rate of {}.Tasks/s".format(N, delta, float(N)/delta))


if __name__ == "__main__" :

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", default="localhost",
                        help="Remote server address")
    args = parser.parse_args()

    run_test(N=1000, server=args.server)
    run_test(N=10000, server=args.server)
    #run_test(N=100000, server=args.server)

