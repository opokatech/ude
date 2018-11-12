import uselect as select
import usocket as socket
import utime as time

server = socket.socket()
server.setblocking(0)

ai = socket.getaddrinfo("0.0.0.0", 9999)
print("Bind address info:", ai)
addr = ai[0][-1]

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(addr)
server.listen(2)  # max waiting clients in the queue to connect

poller = select.poll()

poller.register(server, select.POLLIN)

# using plain list because usocket does not contain socket.fileno() which would allow
# a dictionary with fd as a key.
connections = []

MAX_CLIENTS = 4
TIMEOUT = 1000


def client_idx(a_socket):
    for c_idx, c in enumerate(connections):
        if c["socket"] == a_socket:
            return c_idx
    return -1


def add_client(a_socket, a_addr):
    connections.append({"socket": a_socket, "data": b"", "addr": a_addr})


def del_client(a_idx):
    connections.remove(connections[a_idx])


def write_to(a_idx, a_data):
    c = connections[a_idx]
    c["data"] = a_data
    poller.register(c["socket"], select.POLLIN | select.POLLOUT)


while True:
    # print("waiting for an event")
    for event in poller.ipoll(TIMEOUT):
        event_socket = event[0]
        event_flag = event[1]

        # input...
        if event_flag & select.POLLIN:
            # print("input")
            if event_socket is server:
                cl_socket, cl_addr = event_socket.accept()
                cl_socket.setblocking(0)

                if len(connections) >= MAX_CLIENTS:
                    print("too many clients")
                    cl_socket.close()
                else:
                    poller.register(cl_socket, select.POLLIN)
                    add_client(cl_socket, cl_addr)
                    print("accepted connection from {}. connected clients: {}".format(cl_addr, len(connections)))
            else:
                cl_idx = client_idx(event_socket)

                data = event_socket.read()

                if len(data) == 0:
                    poller.unregister(event_socket)
                    del_client(cl_idx)
                    event_socket.close()
                    print("client {} disconnected (still connected:{})".format(event_socket, len(connections)))
                else:
                    print("received: {}".format(data))
                    for c_idx, c in enumerate(connections):
                        if c_idx != cl_idx:
                            write_to(c_idx, data)
        elif event_flag & select.POLLOUT:
            cl_idx = client_idx(event_socket)
            # print("output")
            c = connections[cl_idx]
            if len(c["data"]) > 0:
                event_socket.write(c["data"])
                c["data"] = b""
            poller.modify(event_socket, select.POLLIN)

        elif event_flag & select.POLLHUP:
            print("client hung up")
            cl_idx = client_idx(event_socket)
            poller.unregister(event_socket)
            del_client(cl_idx)
            event_socket.close()

        elif event_flag & select.POLLERR:
            print("POLLERR - disconnecting client")
            cl_idx = client_idx(event_socket)
            poller.unregister(event_socket)
            del_client(cl_idx)
            event_socket.close()


    # print("after processing events")

