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