## How to run

```bash
python3 requestion.py
```

Type `y` to create a requisition and follow the prompts to enter staff details
and two items with their prices. Repeat for each requisition, then type `n`
to finish entering requests.

Requests below $500 are approved automatically. Requests of $500 or more
start as pending. After entry, the program prints the initial statistics,
prompts for manager decisions, and displays the final details and statistics.


## Assessment 2 correction

**Before:** The original version ran predefined requisitions and manager
decisions. Users could not enter their own requests or choose the outcome
of a pending request.

**What I changed:** I added terminal prompts for staff details, items,
prices, and manager decisions. Requests below $500 are approved automatically.
Requests of $500 or more start as pending. The program prints the statistics
before review, then displays the final requisition details and updated counts.

**Design principle:** I separated the terminal prompts from the `Requisition`
class. The class handles totals, approval decisions, and reporting.

**Verification:** I entered five requisitions in one run and used all three
manager options. Before review, there were 2 approved and 3 pending.
After review, there were 3 approved, 1 pending, and 1 not approved.