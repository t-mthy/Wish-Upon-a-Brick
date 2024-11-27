import zmq


def filter_by_age(wishlist, min_age):
    filtered_wishlist = {}

    for set_number, set_details in wishlist.items():
        try:
            set_age = int(set_details["set_age_group"].rstrip("+"))

            if set_age >= min_age:
                filtered_wishlist[set_number] = set_details
        except ValueError:
            continue

    return filtered_wishlist


def filter_by_pieces(wishlist, min_pieces):
    filtered_wishlist = {}

    for set_number, set_details in wishlist.items():
        try:
            pieces = int(set_details["set_pieces"])

            if pieces >= min_pieces:
                filtered_wishlist[set_number] = set_details
        except ValueError:
            continue

    return filtered_wishlist


def main():
    context = zmq.Context()

    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")

    # Register socket with poller, use for 'Ctrl+C' stops
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    try:
        print("\nLEGO Filter Service running & listening for requests...")
        while True:
            sockets = dict(poller.poll(1000))  # Poll every 1 second

            if socket in sockets:
                message = socket.recv_json()
                print("\n🡺  Received request to filter LEGO sets...")
                command = message.get("command")
                wishlist = message.get("wishlist")

                if command == "filter_by_age":
                    min_age = message.get("min_age")
                    filtered_wishlist = filter_by_age(wishlist, min_age)
                    socket.send_json(
                        {"status": "success", "wishlist": filtered_wishlist}
                    )
                    print("🡸  Sent response of filtered wishlist by age!")
                elif command == "filter_by_pieces":
                    min_pieces = message.get("min_pieces")
                    filtered_wishlist = filter_by_pieces(wishlist, min_pieces)
                    socket.send_json(
                        {"status": "success", "wishlist": filtered_wishlist}
                    )
                    print("🡸  Sent response of filtered wishlist by pieces!")
                else:
                    socket.send_json({"status": "error", "message": "Invalid command"})

    except KeyboardInterrupt:
        print("\nLEGO Filter Service shutting down...")

    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
