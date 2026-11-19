"""Assessment 2 purchase requisition system."""

from decimal import Decimal, InvalidOperation

requisition_counter = 10000


class Requisition:
    """Store one staff member's purchase request."""

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
        """Submit item names and prices, then return their total."""
        global requisition_counter

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
                raise ValueError("Enter a numeric price.") from error

            if not amount.is_finite() or amount < 0:
                raise ValueError("Enter a finite, non-negative price.")

            try:
                cents = amount.quantize(Decimal("0.01"))
            except InvalidOperation as error:
                raise ValueError("The price is too large.") from error

            if amount != cents:
                raise ValueError("Enter a price with at most two decimal places.")

            validated_items.append((name, cents))

        if not validated_items:
            raise ValueError("Add at least one item.")

        total = sum(price for _, price in validated_items)
        requisition_counter += 1
        self.requisition_id = requisition_counter
        self.items = validated_items
        self.total = total
        self.approve_requisition()
        return self.total

    def requisitions_details(self):
        """Return the total used for the approval decision."""
        return self.total

    def approve_requisition(self):
        """Automatically approve submitted requests below $500."""
        if self.requisition_id is None:
            raise ValueError("Submit the requisition first.")

        if self.status == "Pending" and self.requisitions_details() < 500:
            self._set_status("Approved")
        return self.status

    def _set_status(self, status):
        """Update the status and its approval reference together."""
        self.status = status
        self.approval_reference = "Not available"

        if status == "Approved":
            self.approval_reference = self.staff_id + str(self.requisition_id)[-3:]


    def respond_to_requisition(self, decision):
        """Apply a manager's decision to a submitted, pending request."""
        if self.requisition_id is None or self.status != "Pending":
            raise ValueError("Only submitted pending requisitions can be reviewed.")

        if decision not in ("Approved", "Not approved", "Pending"):
            raise ValueError("Choose Approved, Not approved or Pending.")

        self._set_status(decision)
        return self.status

    @staticmethod
    def display_requisitions(requisitions):
        """Print the details of each submitted requisition."""
        print("\nPrinting requisitions")
        for requisition in requisitions:
            if requisition.requisition_id is None:
                continue

            print(f"Date: {requisition.date}")
            print(f"Requisition ID: {requisition.requisition_id}")
            print(f"Staff ID: {requisition.staff_id}")
            print(f"Staff Name: {requisition.staff_name}")
            print(f"Total: ${requisition.total:.2f}")
            print(f"Status: {requisition.status}")
            print(f"Approval Reference Number: {requisition.approval_reference}")
            print()

    @staticmethod
    def requisition_statistics(requisitions):
        """Print and return counts based on current submitted statuses."""
        counts = {"Submitted": 0, "Approved": 0, "Pending": 0, "Not approved": 0}

        for requisition in requisitions:
            if requisition.requisition_id is not None:
                counts["Submitted"] += 1
                counts[requisition.status] += 1

        print("\nDisplaying the Requisition Statistics")
        print(f"The total number of requisitions submitted: {counts['Submitted']}")
        for status in ("Approved", "Pending", "Not approved"):
            print(f"The total number of {status.lower()} requisitions: {counts[status]}")

        return counts

def main():
    examples = [
        ("03/04/2024", "FN19", "John Paul", [("Coffee", 200), ("Paper", 150)]),
        ("05/04/2024", "FN20", "Tracy Brown", [("Desk", 500)]),
        ("07/05/2024", "FN15", "Emma Wellington", [("Equipment", 3500)]),
        ("03/05/2024", "FN02", "Catlin White", [("Supplies", "499.99")]),
        ("08/05/2024", "FN21", "Alex Lee", [("Monitor", 1000)]),
    ]

    requisitions = []
    for date, staff_id, staff_name, items in examples:
        requisition = Requisition(date, staff_id, staff_name)
        requisition.add_requisition(items)
        requisitions.append(requisition)

    print("BEFORE MANAGER REVIEW")
    Requisition.display_requisitions(requisitions)
    before = Requisition.requisition_statistics(requisitions)
    assert before == {"Submitted": 5, "Approved": 2, "Pending": 3, "Not approved": 0}

    requisitions[1].respond_to_requisition("Approved")
    requisitions[2].respond_to_requisition("Not approved")
    requisitions[4].respond_to_requisition("Pending")

    print("\nAFTER MANAGER REVIEW")
    Requisition.display_requisitions(requisitions)
    after = Requisition.requisition_statistics(requisitions)
    assert after == {"Submitted": 5, "Approved": 3, "Pending": 1, "Not approved": 1}

    print("\nAll demonstration checks passed.")


if __name__ == "__main__":
    main()