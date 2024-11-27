import zmq
import webbrowser


def search_lego_on_google(lego_set_spec):
    query = f"LEGO {lego_set_spec}"
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(url)


def search_by_number(set_number):
    search_lego_on_google(set_number)


def search_by_name(set_name):
    search_lego_on_google(set_name)


def main():
    context = zmq.Context()

    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5557")

    # Register socket with poller, use for 'Ctrl+C' stops
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    try:
        print("\nLEGO Web Search Service running & listening for requests...")
        while True:
            sockets = dict(poller.poll(1000))  # Poll every 1 second

            if socket in sockets:
                message = socket.recv_json()
                print("\n🡺  Received request to search LEGO sets...")
                command = message.get("command")

                if command == "search_by_number":
                    set_number = message.get("set_number")
                    search_by_number(set_number)
                    socket.send_json(
                        {
                            "status": "success",
                            "result": "Browser opened with search results by LEGO set number",
                        }
                    )
                    print("🡸  Sent response of search by number!")
                elif command == "search_by_name":
                    set_name = message.get("set_name")
                    search_by_name(set_name)
                    socket.send_json(
                        {
                            "status": "success",
                            "result": "Browser opened with search results by LEGO set name",
                        }
                    )
                    print("🡸  Sent response of search by name!")
                else:
                    socket.send_json({"status": "error", "message": "Invalid command"})

    except KeyboardInterrupt:
        print("\nLEGO Web Search Service shutting down...")

    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
