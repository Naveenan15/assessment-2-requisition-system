"""Assessment 2 purchase requisition system."""

from decimal import Decimal, InvalidOperation
from itertools import count


requisition_ids = count(10001)
APPROVAL_LIMIT = Decimal("500.00")
CENT = Decimal("0.01")


class Requisition:
    """Store and manage one staff member's purchase request."""

    def __init__(self, date, staff_id, staff_name):
        self.date = date.strip()
        self.staff_id = staff_id.strip()
        self.staff_name = staff_name.strip()

        if not all((self.date, self.staff_id, self.staff_name)):
            raise ValueError("Enter the date, staff ID and staff name.")

        self.requisition_id = None
        self.items = []
        self.total = Decimal("0.00")
        self.status = "Pending"
        self.approval_reference = "Not available"

    def add_requisition(self, items):
        """Validate and submit the items, then return their total."""
        if self.requisition_id is not None:
            raise ValueError("This requisition has already been submitted.")

        validated_items = []
        for name, price in items:
            name = name.strip()
            if not name:
                raise ValueError("Enter a name for each item.")

            try:
                amount = Decimal(str(price))
            except InvalidOperation as error:
                raise ValueError(f"Enter a numeric price for {name}.") from error

            if not amount.is_finite() or amount < 0:
                raise ValueError(f"Enter a finite, non-negative price for {name}.")

            try:
                amount_in_cents = amount.quantize(CENT)
            except InvalidOperation as error:
                raise ValueError(f"The price for {name} is too large.") from error

            if amount != amount_in_cents:
                raise ValueError(f"Enter a price with up to two decimal places for {name}.")

            validated_items.append((name, amount_in_cents))

        if not validated_items:
            raise ValueError("Add at least one item.")

        self.total = sum((price for _, price in validated_items), Decimal("0.00"))
        self.items = validated_items
        self.requisition_id = next(requisition_ids)
        self.approve_requisition()
        return self.total

    def requisitions_details(self):
        """Return the stored total used for automatic approval."""
        return self.total

    def approve_requisition(self):
        """Automatically approve submitted requests below $500."""
        if self.requisition_id is None:
            raise ValueError("Submit the requisition first.")

        if self.status == "Pending" and self.requisitions_details() < APPROVAL_LIMIT:
            self._set_status("Approved")

        return self.status

    def respond_to_requisition(self, decision):
        """Apply a manager's decision to a submitted, pending request."""
        if self.requisition_id is None or self.status != "Pending":
            raise ValueError("Only submitted pending requisitions can be reviewed.")

        if decision not in ("Approved", "Not approved", "Pending"):
            raise ValueError("Choose Approved, Not approved or Pending.")

        self._set_status(decision)
        return self.status

    def _set_status(self, status):
        """Keep the status and approval reference in sync."""
        self.status = status
        self.approval_reference = "Not available"

        if status == "Approved":
            suffix = str(self.requisition_id)[-3:]
            self.approval_reference = f"{self.staff_id}{suffix}"

    @staticmethod
    def display_requisitions(requisitions):
        """Print the details of each submitted requisition."""
        print("\nPrinting requisitions")

        for request in requisitions:
            if request.requisition_id is None:
                continue

            print(f"\nDate: {request.date}")
            print(f"Requisition ID: {request.requisition_id}")
            print(f"Staff ID: {request.staff_id}")
            print(f"Staff Name: {request.staff_name}")
            print(f"Total: ${request.total:.2f}")
            print(f"Status: {request.status}")
            print(f"Approval Reference Number: {request.approval_reference}")

    @staticmethod
    def requisition_statistics(requisitions):
        """Print and return the submitted count and all three status counts."""
        counts = {"Submitted": 0, "Approved": 0, "Pending": 0, "Not approved": 0}

        for request in requisitions:
            if request.requisition_id is not None:
                counts["Submitted"] += 1
                counts[request.status] += 1

        print("\nDisplaying the Requisition Statistics")
        print(f"The total number of requisitions submitted: {counts['Submitted']}")

        for status in ("Approved", "Pending", "Not approved"):
            print(f"The total number of {status.lower()} requisitions: {counts[status]}")

        return counts


def main():
    requisitions = []
    print("PURCHASE REQUISITION SYSTEM")

    while True:
        create = input("\nCreate a requisition? (y/n): ").strip().lower()

        if create == "n":
            break
        if create != "y":
            print("Please enter y or n.")
            continue

        date = input("Enter the date (DD/MM/YYYY): ")
        staff_id = input("Enter the staff ID: ")
        staff_name = input("Enter the staff name: ")

        try:
            request = Requisition(date, staff_id, staff_name)
        except ValueError as error:
            print(error)
            continue

        items = []
        while True:
            name = input("Enter an item name (or press Enter to finish): ").strip()
            if not name:
                break

            price = input("Enter the item price: ").strip()
            items.append((name, price))

        try:
            total = request.add_requisition(items)
        except ValueError as error:
            print(f"Requisition could not be submitted. {error}")
            continue

        requisitions.append(request)
        print(f"Requisition ID: {request.requisition_id}")
        print(f"Staff ID: {request.staff_id}")
        print(f"Total: ${total:.2f}")
        print(f"Initial status: {request.status}")

    print("\nBefore manager review")
    Requisition.requisition_statistics(requisitions)

    decisions = {"1": "Approved", "2": "Not approved", "3": "Pending"}

    for request in requisitions:
        if request.status != "Pending":
            continue

        print(f"\nManager review for requisition {request.requisition_id}")
        print(f"Staff: {request.staff_name}")
        print(f"Total: ${request.total:.2f}")
        print("1. Approve")
        print("2. Do not approve")
        print("3. Leave pending")

        choice = input("Choose 1, 2 or 3: ").strip()
        while choice not in decisions:
            choice = input("Please enter 1, 2 or 3: ").strip()

        request.respond_to_requisition(decisions[choice])
        print(f"Final status: {request.status}")

    print("\nAfter manager review")
    Requisition.display_requisitions(requisitions)
    Requisition.requisition_statistics(requisitions)


if __name__ == "__main__":
    main()