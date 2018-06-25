import threading
import zmq

class Union(object):
    """ Worker Union



    ----Control---------> Monitor
                          |     |
                          V     V
    ====Tasks======> Worker ... Worker


    """

    def __init__(self, server_ip,
                 worker_port=55056,
                 control_port=55057,
                 workers=4):

        self._stop = threading.Event()
        self.control_port = control_port
        self.worker_port = worker_port

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):

        context = zmq.Context()

        frontend = context.socket(zmq.DEALER)
        frontend.bind('tcp://*:{}'.format(self.service_port))
        count = 0
        backend = context.socket(zmq.DEALER)
        backend.bind('tcp://*:{}'.format(self.worker_port))
        poll = zmq.Poller()
        poll.register(frontend, zmq.POLLIN)

        while not self.stopped():
            sockets = dict(poll.poll(1000))
            if frontend in sockets:
                if sockets[frontend] == zmq.POLLIN:
                    _id = frontend.recv()
                    msg = frontend.recv()
                    count += 1
                    if msg == b'end':
                        print("Got messages : ", count)
                        count = 0

                    frontend.send(_id, zmq.SNDMORE)
                    frontend.send(b'Hello')
                    del msg


        print("Got messages : ", count)
        frontend.close()
        context.term()


if __name__ == "__main__":

    s = Server()
    s.run()
