import os
import server
import frameStream

if __name__ == "__main__":

    if os.sys.argv[1] == "remote_machine":
        server.start_server(True)
    else:
        server.start_server()