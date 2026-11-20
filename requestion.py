from decimal import Decimal
from itertools import count


requisition_ids = count(10001)


class Requisition:
    def __init__(self, date, staff_id, staff_name):
        self.date = date.strip()
        self.staff_id = staff_id.strip()
        self.staff_name = staff_name.strip()

        if not all((self.date, self.staff_id, self.staff_name)):
            raise ValueError("Enter the date, staff ID and staff name.")

        self.status = "Pending"
        self.requisition_id = next(requisition_ids)

    def add_requisition(self, items):
        self.total = sum(price for _, price in items)
        return self.total

    def approve_requisition(self, total):
        if total < Decimal("500.00"):
            self.status = "Approved"
        return self.status

    def respond_to_requisition(self, choice):
        if self.status == "Pending":
            if choice == "1":
                self.status = "Approved"
            elif choice == "2":
                self.status = "Not approved"
        return self.status

    @staticmethod
    def display_requisitions(requisitions):
        print("\nPrinting requisitions")
        for request in requisitions:
            reference = "Not available"
            if request.status == "Approved":
                reference = f"{request.staff_id}{str(request.requisition_id)[-3:]}"

            print(f"\nDate: {request.date}")
            print(f"Requisition ID: {request.requisition_id}")
            print(f"Staff ID: {request.staff_id}")
            print(f"Staff Name: {request.staff_name}")
            print(f"Total: ${request.total:.2f}")
            print(f"Status: {request.status}")
            print(f"Approval Reference Number: {reference}")

    @staticmethod
    def requisition_statistics(requisitions):
        counts = {"Approved": 0, "Pending": 0, "Not approved": 0}

        for request in requisitions:
            counts[request.status] += 1

        print("\nDisplaying the Requisition Statistics")
        print(f"The total number of requisitions submitted: {len(requisitions)}")
        for status, total in counts.items():
            print(f"The total number of {status.lower()} requisitions: {total}")

        return counts


requisitions = []

while input("\nCreate a requisition? (y/n): ").strip().lower() == "y":
    date = input("Enter the date (DD/MM/YYYY): ")
    staff_id = input("Enter the staff ID: ")
    staff_name = input("Enter the staff name: ")

    request = Requisition(date, staff_id, staff_name)
    print(f"Requisition ID: {request.requisition_id}")
    print(f"Staff ID: {request.staff_id}")

    items = []
    for number in range(1, 3):
        name = input(f"Enter item {number} name: ")
        price = Decimal(input(f"Enter item {number} price: "))
        items.append((name, price))

    total = request.add_requisition(items)
    print(f"Total: ${total:.2f}")
    request.approve_requisition(total)
    print(f"Initial status: {request.status}")

    requisitions.append(request)

print("\nBefore manager review")
Requisition.requisition_statistics(requisitions)

for request in requisitions:
    if request.status != "Pending":
        continue

    print(f"\nManager review for requisition {request.requisition_id}")
    print("1. Approve")
    print("2. Do not approve")
    print("3. Leave pending")

    choice = input("Choose 1, 2 or 3: ").strip()
    while choice not in ("1", "2", "3"):
        choice = input("Please enter 1, 2 or 3: ").strip()

    request.respond_to_requisition(choice)
    print(f"Final status: {request.status}")

print("\nAfter manager review")
Requisition.display_requisitions(requisitions)
Requisition.requisition_statistics(requisitions)