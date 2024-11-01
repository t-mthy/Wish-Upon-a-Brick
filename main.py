import os
import time


class WishUponABrickMain:
    def __init__(self) -> None:
        """
        Data stored in dict/obj structure
        """
        self.wishlist = {}
        self.seed_example_data()

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
            elif user_choice == "0":
                break
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

            user_set_number = input(
                "\nEnter a LEGO set number to edit: "
            ).strip()

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

            user_choice = input(
                "\nEnter 1 to continue, or 0 to go back: "
            ).strip()

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

            user_set_number = input(
                "\nEnter a LEGO set number to delete: "
            ).strip()

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

            user_choice = input(
                "\nEnter 1 to continue, or 0 to go back: "
            ).strip()

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
