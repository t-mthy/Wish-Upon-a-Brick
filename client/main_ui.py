import os
import time
import zmq


class WishUponABrickMain:
    def __init__(self) -> None:
        """
        Data stored in dict/obj structure
        """
        self.wishlist = {}
        self.seed_example_data()

        # ZeroMQ setup
        self.context = zmq.Context()

        # Sockets to microservices
        self.sort_socket = self.context.socket(zmq.REQ)
        self.sort_socket.connect("tcp://localhost:5555")

        self.filter_socket = self.context.socket(zmq.REQ)
        self.filter_socket.connect("tcp://localhost:5556")

        self.search_socket = self.context.socket(zmq.REQ)
        self.search_socket.connect("tcp://localhost:5557")

        self.total_socket = self.context.socket(zmq.REQ)
        self.total_socket.connect("tcp://localhost:5558")

    def __del__(self):
        # Close sockets
        self.sort_socket.close()
        self.filter_socket.close()
        self.search_socket.close()
        self.total_socket.close()
        # Terminate context
        self.context.term()

    def seed_example_data(self):
        """
        Populate sample LEGO data
        """
        self.wishlist = {
            "75192": {
                "set_name": "Millennium Falcon",
                "set_price": "849.99",
                "set_age_group": "16+",
                "set_pieces": "7541",
                "set_description": "Make room to display the most famous starship in the galaxy!",
            },
            "75370": {
                "set_name": "Stormtrooper Mech",
                "set_price": "15.99",
                "set_age_group": "6+",
                "set_pieces": "138",
                "set_description": "The posable mech suit has an opening cockpit for the Stormtrooper LEGO minifigure!",
            },
            "75379": {
                "set_name": "R2-D2",
                "set_price": "99.99",
                "set_age_group": "10+",
                "set_pieces": "1050",
                "set_description": "This brick-built droid is ready to explore the galaxy!",
            },
        }

    def run(self):
        """
        Run the app in main
        """
        while True:
            self.home_screen()

            user_choice = input("Enter your choice: ").strip()

            if user_choice == "1":
                self.menu_screen()
            elif user_choice == "0":
                print("Thank you for using Wish Upon a Brick! See you soon :)")
                break
            else:
                print("Invalid choice...:( Please try again.")
                time.sleep(1)

    def home_screen(self):
        """
        Like a 'Start' screen, greet users, brief app description
        """
        # Clear screen
        os.system("cls" if os.name == "nt" else "clear")

        print(
            """
 _ _ _ _     _      _____                       _____     _     _
| | | |_|___| |_   |  |  |___ ___ ___    ___   | __  |___|_|___| |_
| | | | |_ -|   |  |  |  | . | . |   |  | .'|  | __ -|  _| |  _| '_|
|_____|_|___|_|_|  |_____|  _|___|_|_|  |__,|  |_____|_| |_|___|_,_|
                         |_|


        Welcome to Wish Upon a Brick!
        Got LEGO sets that you've been longing to buy?
        Keep track of them here with this wish list app with ease!


        Options:
        1. Go to menu
        0. Quit the app
        """
        )

    def menu_screen(self):
        """
        Main actions/options to interact with the app
        """
        while True:
            os.system("cls" if os.name == "nt" else "clear")

            print(
                """
                Menu:
                1. 👀  View all LEGO sets
                2. ➕  Add a LEGO set
                3. ⚡  Quick-add a LEGO set
                4. 🖊️   Edit a LEGO set
                5. 🗑️   Delete a LEGO set
                6. 💎   Sort LEGO sets
                7. 🎯   Filter LEGO sets
                8. 🌐   Search LEGO set on web
                9. 📊   Count LEGO sets totals
                0. ⬅️   Go back to home screen
                """
            )

            user_choice = input("Enter your choice: ").strip()

            if user_choice == "1":
                self.view_wishlist_screen()
            elif user_choice == "2":
                self.add_lego_set_screen()
            elif user_choice == "3":
                self.quick_add_lego_set()
            elif user_choice == "4":
                self.edit_lego_set_screen()
            elif user_choice == "5":
                self.delete_lego_set_screen()
            elif user_choice == "6":
                self.sort_lego_sets()
            elif user_choice == "7":
                self.filter_lego_sets()
            elif user_choice == "8":
                self.search_lego_set()
            elif user_choice == "9":
                self.count_lego_totals()
            elif user_choice == "0":
                break
            else:
                print("Invalid choice...:( Please try again.")
                time.sleep(1)

    def sort_lego_sets(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")

            print(
                """
                Sort LEGO Sets:
                1. Sort by Price (Low to High)
                2. Sort by Price (High to Low)
                0. Go back
                """
            )

            user_choice = input("Enter your choice: ").strip()

            if user_choice == "1":
                self.sort_socket.send_json(
                    {"command": "sort_low_to_high", "wishlist": self.wishlist}
                )
                response = self.sort_socket.recv_json()

                if response["status"] == "success":
                    sorted_wishlist = response["wishlist"]
                    self.display_sorted_wishlist(sorted_wishlist)
                else:
                    print("Error:", response["message"])
                    time.sleep(1)

            elif user_choice == "2":
                self.sort_socket.send_json(
                    {"command": "sort_high_to_low", "wishlist": self.wishlist}
                )
                response = self.sort_socket.recv_json()

                if response["status"] == "success":
                    sorted_wishlist = response["wishlist"]
                    self.display_sorted_wishlist(sorted_wishlist)
                else:
                    print("Error:", response["message"])
                    time.sleep(1)

            elif user_choice == "0":
                return
            else:
                print("Invalid choice...:( Please try again.")
                time.sleep(1)

    def display_sorted_wishlist(self, sorted_wishlist):
        os.system("cls" if os.name == "nt" else "clear")

        print("Sorted LEGO sets result:\n")

        for set_number, set_details in sorted_wishlist.items():
            print(
                f"[{set_number}] --- {set_details['set_name']}, ${set_details['set_price']}"
            )

        input("\nPress 'Enter' to continue...")

    def filter_lego_sets(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")

            print(
                """
                Filter LEGO Sets:
                1. Filter by Minimum Age Requirement
                2. Filter by Minimum Piece Count
                0. Go back
                """
            )

            user_choice = input("Enter your choice: ").strip()

            if user_choice == "1":
                min_age_str = input("Enter minimum age: ").strip()
                try:
                    min_age = int(min_age_str)
                    self.filter_socket.send_json(
                        {
                            "command": "filter_by_age",
                            "wishlist": self.wishlist,
                            "min_age": min_age,
                        }
                    )
                    response = self.filter_socket.recv_json()

                    if response["status"] == "success":
                        filtered_wishlist = response["wishlist"]
                        self.display_filtered_wishlist(filtered_wishlist)
                    else:
                        print("Error:", response["message"])
                        time.sleep(1)
                except ValueError:
                    print("Invalid age input. Please enter a number.")
                    time.sleep(1)

            elif user_choice == "2":
                min_pieces_str = input("Enter minimum piece count: ").strip()
                try:
                    min_pieces = int(min_pieces_str)
                    self.filter_socket.send_json(
                        {
                            "command": "filter_by_pieces",
                            "wishlist": self.wishlist,
                            "min_pieces": min_pieces,
                        }
                    )
                    response = self.filter_socket.recv_json()

                    if response["status"] == "success":
                        filtered_wishlist = response["wishlist"]
                        self.display_filtered_wishlist(filtered_wishlist)
                    else:
                        print("Error:", response["message"])
                        time.sleep(1)
                except ValueError:
                    print("Invalid piece count input. Please enter a number.")
                    time.sleep(1)

            elif user_choice == "0":
                return
            else:
                print("Invalid choice...:( Please try again.")
                time.sleep(1)

    def display_filtered_wishlist(self, filtered_wishlist):
        os.system("cls" if os.name == "nt" else "clear")

        if not filtered_wishlist:
            print("No LEGO sets match the filter criteria.")
        else:
            print("Filtered LEGO sets result:\n")

            for set_number, set_details in filtered_wishlist.items():
                print(f"[{set_number}] --- {set_details['set_name']}")

        input("\nPress 'Enter' to continue...")

    def search_lego_set(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")

            print(
                """
                Search LEGO Set on Web:
                1. Search by LEGO Set Number
                2. Search by LEGO Set Name
                0. Go back
                """
            )

            user_choice = input("Enter your choice: ").strip()

            if user_choice == "1":
                set_number = input("Enter LEGO Set Number: ").strip()
                if set_number:
                    self.search_socket.send_json(
                        {"command": "search_by_number", "set_number": set_number}
                    )
                    response = self.search_socket.recv_json()

                    if response["status"] == "success":
                        print(f"\n✔️  {response["result"]}.")
                        input("\nPress 'Enter' to continue...")
                    else:
                        print("Error:", response["message"])
                        time.sleep(1)
                else:
                    print("Please enter a LEGO set number.")
                    time.sleep(1)

            elif user_choice == "2":
                set_name = input("Enter LEGO Set Name: ").strip()
                if set_name:
                    self.search_socket.send_json(
                        {"command": "search_by_name", "set_name": set_name}
                    )
                    response = self.search_socket.recv_json()

                    if response["status"] == "success":
                        print(f"\n✔️  {response["result"]}.")
                        input("\nPress 'Enter' to continue...")
                    else:
                        print("Error:", response["message"])
                        time.sleep(1)
                else:
                    print("Please enter a LEGO set name.")
                    time.sleep(1)

            elif user_choice == "0":
                return
            else:
                print("Invalid choice...:( Please try again.")
                time.sleep(1)

    def count_lego_totals(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")

            print(
                """
                Count LEGO Sets Totals:
                1. Total Number of LEGO Sets
                2. Total Cost of LEGO Sets
                3. Total Number of Pieces
                0. Go back
                """
            )

            user_choice = input("Enter your choice: ").strip()

            if user_choice == "1":
                self.total_socket.send_json(
                    {"command": "total_number_of_sets", "wishlist": self.wishlist}
                )
                response = self.total_socket.recv_json()

                if response["status"] == "success":
                    total_sets = response["total_sets"]
                    print(f"\n📊  Total Number of LEGO Sets: {total_sets}")
                    input("\nPress 'Enter' to continue...")
                else:
                    print("Error:", response["message"])
                    time.sleep(1)

            elif user_choice == "2":
                self.total_socket.send_json(
                    {"command": "total_cost_of_sets", "wishlist": self.wishlist}
                )
                response = self.total_socket.recv_json()

                if response["status"] == "success":
                    total_cost = response["total_cost"]
                    print(f"\n📊  Total Cost of LEGO Sets: ${total_cost:.2f}")
                    input("\nPress 'Enter' to continue...")
                else:
                    print("Error:", response["message"])
                    time.sleep(1)

            elif user_choice == "3":
                self.total_socket.send_json(
                    {"command": "total_pieces_of_sets", "wishlist": self.wishlist}
                )
                response = self.total_socket.recv_json()

                if response["status"] == "success":
                    total_pieces = response["total_pieces"]
                    print(f"\n📊  Total Number of LEGO Pieces: {total_pieces}")
                    input("\nPress 'Enter' to continue...")
                else:
                    print("Error:", response["message"])
                    time.sleep(1)

            elif user_choice == "0":
                return
            else:
                print("Invalid choice...:( Please try again.")
                time.sleep(1)

    def view_wishlist_screen(self):
        """
        See all LEGO sets in the wish list app
        """
        while True:
            os.system("cls" if os.name == "nt" else "clear")

            if not self.wishlist:
                print("Empty wish list. Going back to the menu to add more!")
                time.sleep(2)
                return
            else:
                print("Here are the LEGO sets in your wish list:\n")
                # (key, value) tuple pairs, key->set_number, val->set_details
                for set_number, set_details in self.wishlist.items():
                    print(f"[{set_number}] --- {set_details['set_name']}")

            user_choice = input(
                "\nEnter 1 to view full details of a set, or 0 to go back: "
            ).strip()

            if user_choice == "1":
                user_set_number = input("Enter LEGO set number: ").strip()

                if user_set_number in self.wishlist:
                    self.view_set_detail_screen(user_set_number)
                else:
                    print("❌ LEGO set not found. Please try again.")
                    time.sleep(1)
            elif user_choice == "0":
                return
            else:
                print("Invalid choice...:( Please try again.")
                time.sleep(1)

    def view_set_detail_screen(self, set_number):
        """
        See full details of a LEGO set
        """
        while True:
            os.system("cls" if os.name == "nt" else "clear")

            set_details = self.wishlist[set_number]

            print(f"LEGO Set Name: {set_details['set_name']}")
            print(f"Price: ${set_details['set_price']}")
            print(f"Age Group: {set_details['set_age_group']}")
            print(f"Pieces: {set_details['set_pieces']}")
            print(f"LEGO Set Number: {set_number}")
            print(f"Description: {set_details['set_description']}")

            user_choice = input(
                "\nEnter 1 to [Edit], 2 to [Delete], or 0 to go back: "
            ).strip()

            if user_choice == "1":
                self.edit_lego_set(set_number)
            elif user_choice == "2":
                self.delete_lego_set(set_number)
                # Go back to view all only when deleted
                if not self.wishlist.get(set_number):
                    return
            elif user_choice == "0":
                return
            else:
                print("Invalid choice...:( Please try again.")
                time.sleep(1)

    def add_lego_set_screen(self):
        """
        Add a new LEGO set to wish list
        """
        os.system("cls" if os.name == "nt" else "clear")

        print("[Add a new LEGO set]\n")

        user_set_name = input("Enter LEGO set name: ").strip()
        user_set_price = input("Enter LEGO set price: $").strip()
        user_set_age_group = input("Enter LEGO set age group: ").strip()
        user_set_pieces = input("Enter number of pieces: ").strip()
        user_set_number = input("Enter LEGO set number: ").strip()
        user_set_description = input("Enter LEGO set description: ").strip()

        self.wishlist[user_set_number] = {
            "set_name": user_set_name,
            "set_price": user_set_price,
            "set_age_group": user_set_age_group,
            "set_pieces": user_set_pieces,
            "set_description": user_set_description,
        }

        print("\n ✔️  LEGO set added successfully!")
        time.sleep(1)

    def quick_add_lego_set(self):
        """
        Quickly add a new LEGO set to wish list with one line of input
        """
        os.system("cls" if os.name == "nt" else "clear")

        print("[Quick-add a new LEGO set]\n")

        user_input = input(
            "Enter details in format (Name, Price, Age, Pieces, Set Number, Description): "
        ).strip()

        try:
            (
                set_name,
                set_price,
                set_age_group,
                set_pieces,
                set_number,
                set_description,
            ) = map(str.strip, user_input.split(",", 5))

            self.wishlist[set_number] = {
                "set_name": set_name,
                "set_price": set_price,
                "set_age_group": set_age_group,
                "set_pieces": set_pieces,
                "set_description": set_description,
            }

            print("\n ✔️  LEGO set added successfully!")
        except ValueError:
            print("\n ❌  Invalid input format. Please try again.")
        time.sleep(1)

    def edit_lego_set_screen(self):
        """
        Access from menu screen only, leads to edit_lego_set func
        """
        while True:
            os.system("cls" if os.name == "nt" else "clear")

            if not self.wishlist:
                print("Empty wish list. Going back to the menu to add more!")
                time.sleep(2)
                return

            print("Here are the LEGO sets in your wish list:\n")
            for set_number, set_details in self.wishlist.items():
                print(f"[{set_number}] --- {set_details['set_name']}")

            user_set_number = input("\nEnter a LEGO set number to edit: ").strip()

            if user_set_number in self.wishlist:
                self.edit_lego_set(user_set_number)
                return
            else:
                print("❌ LEGO set not found. Please try again.")
                time.sleep(1)

    def edit_lego_set(self, set_number):
        """
        Update a LEGO set's details from wish list
        """
        while True:
            print(
                """
                \n
                Are you sure you want to update this set?

                ⚠️  Warning: previous data could be overwritten and unrecoverable!
                """
            )

            user_choice = input("\nEnter 1 to continue, or 0 to go back: ").strip()

            if user_choice == "1":
                break
            elif user_choice == "0":
                return
            else:
                print("Invalid choice...:( Please try again.")
                time.sleep(1)

        new_set_name = input(
            f"Enter new name for LEGO set #{set_number} (or press 'Enter' to skip): "
        ).strip()
        new_set_price = input(
            f"Enter new price for LEGO set #{set_number} (or press 'Enter' to skip): "
        ).strip()
        new_set_age_group = input(
            f"Enter new age group for LEGO set #{set_number} (or press 'Enter' to skip): "
        ).strip()
        new_set_pieces = input(
            f"Enter new number of pieces for LEGO set #{set_number} (or press 'Enter' to skip): "
        ).strip()
        new_set_description = input(
            f"Enter new description for LEGO set #{set_number} (or press 'Enter' to skip): "
        ).strip()

        if new_set_name:
            self.wishlist[set_number]["set_name"] = new_set_name
        if new_set_price:
            self.wishlist[set_number]["set_price"] = new_set_price
        if new_set_age_group:
            self.wishlist[set_number]["set_age_group"] = new_set_age_group
        if new_set_pieces:
            self.wishlist[set_number]["set_pieces"] = new_set_pieces
        if new_set_description:
            self.wishlist[set_number]["set_description"] = new_set_description

        print("\n ✔️  LEGO set updated successfully!")
        time.sleep(1)

    def delete_lego_set_screen(self):
        """
        Access from menu screen only, leads to delete_lego_set func
        """
        while True:
            os.system("cls" if os.name == "nt" else "clear")

            if not self.wishlist:
                print("Empty wish list. Going back to the menu to add more!")
                time.sleep(2)
                return

            print("Here are the LEGO sets in your wish list:\n")
            for set_number, set_details in self.wishlist.items():
                print(f"[{set_number}] --- {set_details['set_name']}")

            user_set_number = input("\nEnter a LEGO set number to delete: ").strip()

            if user_set_number in self.wishlist:
                self.delete_lego_set(user_set_number)
                return
            else:
                print("❌ LEGO set not found. Please try again.")
                time.sleep(1)

    def delete_lego_set(self, set_number):
        """
        Delete a LEGO set from wish list
        """
        while True:
            print(
                """
                \n
                Are you sure you want to delete this set?

                ⚠️  Warning: data erasure, re-add its data if you want this LEGO set back!
                """
            )

            user_choice = input("\nEnter 1 to continue, or 0 to go back: ").strip()

            if user_choice == "1":
                break
            elif user_choice == "0":
                return
            else:
                print("Invalid choice...:( Please try again.")
                time.sleep(1)

        del self.wishlist[set_number]

        print("\n ✔️  LEGO set deleted successfully!")
        time.sleep(1)


if __name__ == "__main__":
    app = WishUponABrickMain()
    app.run()
