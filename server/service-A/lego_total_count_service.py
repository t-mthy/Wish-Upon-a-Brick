import zmq


def total_number_of_sets(wishlist):
    return len(wishlist)


def total_cost_of_sets(wishlist):
    total_cost = 0.0

    for set_details in wishlist.values():
        try:
            total_cost += float(set_details["set_price"])
        except ValueError:
            continue

    return total_cost


def total_pieces_of_sets(wishlist):
    total_pieces = 0

    for set_details in wishlist.values():
        try:
            total_pieces += int(set_details["set_pieces"])
        except ValueError:
            continue

    return total_pieces


def main():
    context = zmq.Context()

    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5558")

    # Register socket with poller, use for 'Ctrl+C' stops
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    try:
        print("\nLEGO Total Count Service running & listening for requests...")
        while True:
            sockets = dict(poller.poll(1000))  # Poll every 1 second

            if socket in sockets:
                message = socket.recv_json()
                print("\n🡺  Received request to count LEGO sets...")
                command = message.get("command")
                wishlist = message.get("wishlist")

                if command == "total_number_of_sets":
                    total_sets = total_number_of_sets(wishlist)
                    socket.send_json({"status": "success", "total_sets": total_sets})
                    print("🡸  Sent response of total number of sets!")
                elif command == "total_cost_of_sets":
                    total_cost = total_cost_of_sets(wishlist)
                    socket.send_json({"status": "success", "total_cost": total_cost})
                    print("🡸  Sent response of total cost of sets!")
                elif command == "total_pieces_of_sets":
                    total_pieces = total_pieces_of_sets(wishlist)
                    socket.send_json(
                        {"status": "success", "total_pieces": total_pieces}
                    )
                    print("🡸  Sent response of total pieces of sets!")
                else:
                    socket.send_json({"status": "error", "message": "Invalid command"})

    except KeyboardInterrupt:
        print("\nLEGO Total Count Service shutting down...")

    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
