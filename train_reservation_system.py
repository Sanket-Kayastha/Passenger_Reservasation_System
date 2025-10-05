import random
import datetime

class Train:
    """
    Represents a train with its details.
    """
    def __init__(self, train_no, name, source, destination, total_seats):
        self.train_no = train_no
        self.name = name
        self.source = source
        self.destination = destination
        self.total_seats = total_seats
        self.available_seats = total_seats
        # Waiting list: Stores PNRs of tickets that are not confirmed.
        self.waiting_list = []

    def get_details(self):
        """Returns a formatted string of the train's details."""
        return (f"Train No: {self.train_no} | Name: {self.name} | "
                f"From: {self.source} To: {self.destination}")

    def check_availability(self):
        """Returns the number of available seats."""
        return self.available_seats

class Ticket:
    """
    Represents a ticket with its PNR, passengers, and status.
    """
    # Class-level counter for PNR generation
    pnr_counter = random.randint(1000000, 9999999)

    def __init__(self, train, passengers):
        Ticket.pnr_counter += 1
        self.pnr = str(Ticket.pnr_counter)
        self.train = train
        self.passengers = passengers  # List of passenger dictionaries
        self.status = "Confirmed" if train.check_availability() >= len(passengers) else "Waiting"
        self.booking_date = datetime.datetime.now()

    def get_details(self):
        """Returns a formatted string of the ticket's details."""
        passenger_details = "\n".join([f"  - {p['name']} ({p['age']})" for p in self.passengers])
        return (
            f"-----------------------------------\n"
            f"PNR: {self.pnr}\n"
            f"Train: {self.train.name} ({self.train.train_no})\n"
            f"From: {self.train.source} To: {self.train.destination}\n"
            f"Status: {self.status}\n"
            f"Booking Date: {self.booking_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Passengers:\n{passenger_details}\n"
            f"-----------------------------------"
        )

class ReservationSystem:
    """
    Manages the overall reservation process, including trains and tickets.
    """
    def __init__(self):
        # Using dictionaries to store trains and tickets for quick lookups
        self.trains = {}
        self.tickets = {}

    def add_train(self, train):
        """Adds a new train to the system."""
        self.trains[train.train_no] = train
        print(f"Train '{train.name}' added successfully.")

    def display_trains(self, source, destination):
        """Displays available trains between a source and destination."""
        print(f"\n--- Trains from {source.upper()} to {destination.upper()} ---")
        found_trains = False
        for train_no, train in self.trains.items():
            if train.source.lower() == source.lower() and train.destination.lower() == destination.lower():
                print(f"{train.get_details()} | Available Seats: {train.check_availability()}")
                found_trains = True
        if not found_trains:
            print("No trains found for the given route.")
        print("--------------------------------------------------")

    def book_ticket(self):
        """Handles the ticket booking process."""
        source = input("Enter source station: ")
        destination = input("Enter destination station: ")
        self.display_trains(source, destination)

        train_no = input("Enter the train number to book: ")
        if train_no not in self.trains:
            print("Error: Invalid train number.")
            return

        selected_train = self.trains[train_no]

        try:
            num_passengers = int(input("Enter the number of passengers: "))
            if num_passengers <= 0:
                print("Error: Number of passengers must be positive.")
                return
        except ValueError:
            print("Error: Invalid input. Please enter a number.")
            return

        passengers = []
        for i in range(num_passengers):
            name = input(f"Enter name for passenger {i + 1}: ")
            age = input(f"Enter age for passenger {i + 1}: ")
            passengers.append({"name": name, "age": age})

        new_ticket = Ticket(selected_train, passengers)
        self.tickets[new_ticket.pnr] = new_ticket

        if new_ticket.status == "Confirmed":
            selected_train.available_seats -= len(passengers)
            print("\nBooking Successful! Your ticket is confirmed.")
        else:
            selected_train.waiting_list.append(new_ticket.pnr)
            print(f"\nBooking Successful! Your ticket is on the waiting list (Position: {len(selected_train.waiting_list)}).")

        print(new_ticket.get_details())

    def cancel_ticket(self):
        """Handles the ticket cancellation process."""
        pnr_to_cancel = input("Enter PNR number to cancel: ")
        if pnr_to_cancel not in self.tickets:
            print("Error: Invalid PNR number.")
            return

        ticket_to_cancel = self.tickets[pnr_to_cancel]
        if ticket_to_cancel.status == "Cancelled":
            print("Error: This ticket has already been cancelled.")
            return

        train = ticket_to_cancel.train
        num_passengers = len(ticket_to_cancel.passengers)

        # Mark ticket as cancelled
        ticket_to_cancel.status = "Cancelled"
        print(f"\nTicket with PNR {pnr_to_cancel} has been cancelled.")

        # If the cancelled ticket was confirmed, try to confirm a waiting list ticket
        if ticket_to_cancel in self.tickets.values() and ticket_to_cancel.status != "Cancelled":
             train.available_seats += num_passengers

        if train.waiting_list:
            # Check if now there are enough seats for the first person on the waiting list
            pnr_from_wl = train.waiting_list[0]
            ticket_to_confirm = self.tickets[pnr_from_wl]
            
            if train.available_seats >= len(ticket_to_confirm.passengers):
                ticket_to_confirm.status = "Confirmed"
                train.available_seats -= len(ticket_to_confirm.passengers)
                train.waiting_list.pop(0) # Remove from waiting list
                print(f"A ticket from the waiting list (PNR: {pnr_from_wl}) has been confirmed.")


    def check_pnr_status(self):
        """Checks and displays the status of a ticket using its PNR."""
        pnr_to_check = input("Enter PNR number: ")
        if pnr_to_check in self.tickets:
            ticket = self.tickets[pnr_to_check]
            print("\n--- PNR Status ---")
            print(ticket.get_details())
            if ticket.status == "Waiting":
                position = ticket.train.waiting_list.index(pnr_to_check) + 1
                print(f"Current Waiting List Position: {position}")
        else:
            print("Error: Invalid PNR number.")


def main():
    """The main function to run the reservation system CLI."""
    system = ReservationSystem()

    # Pre-populating the system with some trains for demonstration
    system.add_train(Train("12028", "Shatabdi Express", "Bengaluru", "Chennai", 150))
    system.add_train(Train("12627", "Karnataka Express", "Bengaluru", "New Delhi", 200))
    system.add_train(Train("16526", "Kanyakumari Exp", "Bengaluru", "Kanyakumari", 180))
    system.add_train(Train("12007", "Mysuru Shatabdi", "Chennai", "Mysuru", 150))

    while True:
        print("\n===== Railway Reservation System =====")
        print("1. Book a Ticket")
        print("2. Cancel a Ticket")
        print("3. Check PNR Status")
        print("4. Display Available Trains")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice (1-5): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            system.book_ticket()
        elif choice == 2:
            system.cancel_ticket()
        elif choice == 3:
            system.check_pnr_status()
        elif choice == 4:
            source = input("Enter source station: ")
            destination = input("Enter destination station: ")
            system.display_trains(source, destination)
        elif choice == 5:
            print("Thank you for using the Railway Reservation System.")
            break
        else:
            print("Invalid choice. Please select from 1 to 5.")

if __name__ == "__main__":
    main()
