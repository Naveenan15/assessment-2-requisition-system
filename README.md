# Assessment 2 Purchase Requisition System

## How to run

```bash
python3 requestion.py
```

1. Type `y` to create a requisition. Enter the date, staff ID, and staff name.
2. Enter one or more items with their prices. Press Return at an empty item-name prompt to submit the requisition.
3. Repeat for each request. When you finish entering requests, type `n` to begin manager review.
4. For each pending request, choose `1` to approve, `2` to decline, or `3` to leave it pending.

Requests below $500 are approved automatically. Requests of $500 or more start as pending. The program displays the initial statistics before manager review and prints the final requisition details and updated statistics after review.

## Assessment 2 correction

### Original version

The original demonstration used predefined requisitions and manager decisions. The same example requests ran each time.

### What I changed

I added terminal prompts for staff details, items, prices, and manager decisions. The updated version accepts a variable number of items and validates prices before submitting a request. Automatic approval uses the stored total returned by `requisitions_details()`, and `requisition_statistics()` displays and returns all four counts.

### Design principles

I used **separation of concerns** by keeping terminal input in `main()` and placing requisition rules in the `Requisition` class. I used **encapsulation** by keeping price validation and approval decisions in the class and updating the approval reference together with the status.

### Verification

I entered five requisitions in one run, including requests totalling $499.99 and exactly $500.00, and used all three manager options.

| Stage | Submitted | Approved | Pending | Not approved |
| --- | ---: | ---: | ---: | ---: |
| Before manager review | 5 | 2 | 3 | 0 |
| After manager review | 5 | 3 | 1 | 1 |

In a separate validation test, I entered `abc` as an item price. The program displayed a message asking for a numeric price and returned to the requisition menu so I could try again.