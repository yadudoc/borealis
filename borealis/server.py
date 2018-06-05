import threading
import zmq

class Server(threading.Thread):

    def __init__(self, service_port=55055, worker_port=55056):

        self._stop = threading.Event()
        self.service_port = service_port
        self.worker_port = worker_port
        threading.Thread.__init__(self)

    def stop(self):
        self._stop.set()


    def stopped(self):
        return self._stop.isSet()

    def run(self):

        context = zmq.Context()

        frontend = context.socket(zmq.ROUTER)
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
