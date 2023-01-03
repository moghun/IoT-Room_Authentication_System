import server
import frameStream
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "multiple_devices":
            server.start_server(True)
        else:
            print("Wrong argument")
            exit(1)
    else:
        server.start_server()