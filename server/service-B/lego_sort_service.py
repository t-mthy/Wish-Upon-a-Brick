import zmq


def sort_wishlist(wishlist, order):
    # Convert wishlist dict to a list of dicts with prices (floats)
    wishlist_list = []

    for set_number, set_details in wishlist.items():
        set_price = float(set_details["set_price"])

        set_details_copy = set_details.copy()
        set_details_copy["set_price"] = set_price
        set_details_copy["set_number"] = set_number

        wishlist_list.append(set_details_copy)

    # Sort list based on set_price
    is_reverse = True if order == "desc" else False
    sorted_list = sorted(
        wishlist_list, key=lambda lego_set: lego_set["set_price"], reverse=is_reverse
    )

    # Convert back to dict
    sorted_wishlist = {}

    for set_details in sorted_list:
        set_details["set_price"] = str(set_details["set_price"])
        set_number = set_details.pop("set_number")
        sorted_wishlist[set_number] = set_details

    return sorted_wishlist


def main():
    context = zmq.Context()

    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    # Register socket with poller, use for 'Ctrl+C' stops
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    try:
        print("\nLEGO Sort Service running & listening for requests...")
        while True:
            sockets = dict(poller.poll(1000))  # Poll every 1 second

            if socket in sockets:
                message = socket.recv_json()
                print("\n🡺  Received request to sort LEGO sets...")
                command = message.get("command")
                wishlist = message.get("wishlist")

                if command == "sort_low_to_high":
                    sorted_wishlist = sort_wishlist(wishlist, "asc")
                    socket.send_json({"status": "success", "wishlist": sorted_wishlist})
                    print("🡸  Sent response of sorted wishlist!")
                elif command == "sort_high_to_low":
                    sorted_wishlist = sort_wishlist(wishlist, "desc")
                    socket.send_json({"status": "success", "wishlist": sorted_wishlist})
                    print("🡸  Sent response of sorted wishlist!")
                else:
                    socket.send_json({"status": "error", "message": "Invalid command"})

    except KeyboardInterrupt:
        print("\nLEGO Sort Service shutting down...")

    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
