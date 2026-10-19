# Digital Permit & License Management System

A simple Python program that lets a district office receive permit applications, review and approve them, issue license numbers, and warn when licenses are about to expire. Anyone can verify a license using only its license number. Built with Object-Oriented Programming (OOP) concepts.

**Domain:** Government  
**Problem:** Paper permit records are slow to check, easy to lose, and hard to track for expiry. Businesses forget to renew, and officers cannot quickly confirm whether a license is real. This tool gives every application a clear workflow, every approved permit a license number, and every office an expiry alert list, on any computer with Python.

## Features

- Apply for a permit (type, holder label and area) and receive a permit ID
- A clear workflow: Applied, Under review, then Approved or Rejected (a rejection needs a reason)
- Approval issues a license number (for example `LIC-2026-0001`) and an expiry date based on the permit type
- Renew an approved permit; renewal opens 60 days before expiry and also works after expiry
- Verify a license by its license number
- Expiry alerts for permits that are expired or expire within 30 days
- Summary count of permits by type
- Remove a record (for example an application sent by mistake)
- Checks every input and shows clear error messages instead of crashing

## How to Run

1. Install Python 3.8 or later.
2. Download or clone this repository:
3. Run the program:

The program starts empty and opens a menu. You add your own applications:

```
1. Apply for permit  2. Process application  3. Renew permit
4. Show all  5. Verify license  6. Expiry alerts  7. Type summary
8. Remove permit  9. Exit
```

To apply, type the permit type, holder label and area on one line, separated by commas:

```
Business,Aminata Fresh Fish,Kissy
```

Sample data is available but does not run by default: call `demo(registry)` in the last lines of the file to load it.

## Project Structure

| File | Purpose |
|------|---------|
| `digital_permit_system.py` | Classes, demo and menu |
| `README.md` | Documentation |
| `LICENSE` | MIT open-source licence |

## OOP Concepts Used

###  Classes and Objects
- **`Permit`**: attributes `permit_id`, `permit_type`, `holder_label`, `area`, `license_number`, `expiry_date`, `status_log`; methods `start_review()`, `approve()`, `reject()`, `renew()`, `update_record()`, `stored_status()`, `is_expired()`, `days_until_expiry()`, `current_status()`, `display_info()`
- **`PermitRegistry`**: attributes `office_name`, `permits`; methods `add_permit()`, `find()`, `find_by_license()`, `display_all()`, `remove_permit()`, `display_expiring()`, `type_summary()`
- The registry holds and manages `Permit` objects, which demonstrates interaction between objects. For example, `display_expiring()` asks each permit for its status and `days_until_expiry()`, and `find_by_license()` checks each permit's license number.

###  Data Structure
- A **dictionary** (`{permit_id: Permit}`) stores all permits, so any record can be found instantly by its ID.
- `add_permit()` and `display_all()` add and display records.
- **Bonus (tuples):** each status change is a **tuple** `(date, status, note)`, and a permit's `status_log` is a tuple of these. Tuples cannot be changed, so each update builds a new tuple and the history of a permit cannot be rewritten by accident. The lists of allowed permit types and statuses are also tuples. The dictionary is the only data structure holding the permit objects.

###  Methods
| Type | Method | Purpose |
|------|--------|---------|
| Instance | `start_review()`, `approve()`, `reject()`, `renew()`, `update_record()`, `is_expired()`, `days_until_expiry()`, `current_status()`, `display_info()` | Work on one permit's data and enforce the workflow |
| Class (`@classmethod`) | `Permit.from_string("Business, Aminata Fresh Fish, Kissy")` | Alternative way to create a permit from one line of text |
| Class (`@classmethod`) | `Permit.next_license_number()` | Creates the next license number, using a counter shared by every permit |
| Class (`@classmethod`) | `Permit.type_options()` | Gives the allowed permit types as text for prompts and errors |
| Static (`@staticmethod`) | `Permit.validity_months()` | Gives how long each type of permit lasts |
| Static (`@staticmethod`) | `Permit.add_months()` | Adds months to a date and keeps the day valid (31 Jan plus 1 month gives 28 Feb) |
| Static (`@staticmethod`) | `Permit.normalize_type()` | Checks a permit type typed in any capitalisation |

## Digital Public Goods (DPG) Alignment

| DPG Principle | How this project meets it |
|---------------|---------------------------|
| **Open-source** | The full source code is public on GitHub under the MIT licence, so anyone can use, study, modify and share it. |
| **Inclusive and accessible design** | Plain-language prompts, a numbered menu, and clear error messages that say how to fix a mistake. Input is accepted in any capitalisation. It runs on any low-spec computer, needs no internet connection and has no cost. Anyone can verify a license without an account. |
| **Privacy-respecting** | No sensitive personal data is stored. A permit holder is a short label such as a business or stall name, never a legal name, phone number, address or ID number, and the prompt reminds users of this. Only the permit type, a general area and a status history are kept. Data is kept in memory only and is not sent anywhere. A record can be removed at any time. |
| **Modular and reusable** | `Permit` and `PermitRegistry` are separate, self-contained classes. They can be imported into other projects, for example a complaint tracker or a market fee system, without changing the code. The start block means importing the file does not run the menu. |

## Sample Output

```
Choose: 1
Use a business or stall name. Do not enter personal ID or phone numbers.
Type,holder label,area (types: Business, Driving, Building, Fishing, Market stall, Other):
business,Aminata Fresh Fish,Kissy
Application received. Permit ID: PRM001.

Choose: 2
Permit ID: prm001
Action (review / approve / reject): review
Short note (optional): Documents checked
Updated. PRM001 is now: Under review.

Choose: 2
Permit ID: PRM001
Action (review / approve / reject): approve
Short note (optional):
Updated. PRM001 is now: Approved.

Choose: 5
License number: lic-2026-0001
ID: PRM001 | Business | Aminata Fresh Fish | Kissy | Status: Approved
    License: LIC-2026-0001 | Expires: 2027-10-18 (365 days left)
    - 2026-10-18: Applied (Application received)
    - 2026-10-18: Under review (Documents checked)
    - 2026-10-18: Approved (License LIC-2026-0001 issued)
```

## Limitations and Future Improvements

- Records are lost when the program closes (kept in memory for privacy). A future version could add optional local storage.
- Anyone who has the program can approve or reject an application. A future version could add a staff login.
- Validity periods are general values. Each office could set its own, and fees could be added.
- Add a graphical interface and local-language support (e.g. Krio).

## Author

osman Junior Kamara

## Licence

Released under the [MIT Licence](LICENSE).
