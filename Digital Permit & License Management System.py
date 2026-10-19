print("================================================================")
print("Digital Permit & License Management System - Government domain")
print("================================================================")
import calendar
from datetime import date


# ---------------------------------------------------------------- Class 1
class Permit:
    """One permit application and its license (Task 1: attributes + methods)."""

    PERMIT_TYPES = ("Business", "Driving", "Building", "Fishing", "Market stall", "Other")
    STATUSES = ("Applied", "Under review", "Approved", "Rejected")
    RENEWAL_WINDOW_DAYS = 60   # renewal opens this many days before expiry
    _counter = 0               # class attribute used to generate permit IDs
    _license_counter = 0       # class attribute used to generate license numbers

    def __init__(self, permit_type, holder_label, area):
        permit_type = self.normalize_type(permit_type)
        holder_label = holder_label.strip()
        area = area.strip()
        if not holder_label:
            raise ValueError("Holder label cannot be empty (use a business or stall name).")
        if len(holder_label) > 40:
            raise ValueError("Holder label must be 40 characters or fewer.")
        if not area:
            raise ValueError("Area cannot be empty (use a district or ward name).")
        Permit._counter += 1
        self.permit_id = f"PRM{Permit._counter:03d}"
        self.permit_type = permit_type
        self.holder_label = holder_label      # a label, not a legal name
        self.area = area                      # general area only, no street address
        self.license_number = None            # set when the permit is approved
        self.expiry_date = None               # set when the permit is approved
        # tuple of (date, status, note) tuples; it always holds the first entry
        self.status_log = ((date.today().isoformat(), "Applied", "Application received"),)

    # ---- instance methods (Task 3)
    def _add_entry(self, status, note=""):
        """Add a status entry as an immutable tuple: (date, status, note).
        Tuples cannot be changed, so a new tuple of entries is built."""
        entry = (date.today().isoformat(), status, note.strip())
        self.status_log = self.status_log + (entry,)

    def start_review(self, note=""):
        if self.stored_status() != "Applied":
            raise ValueError("Only a newly applied permit can be sent for review.")
        self._add_entry("Under review", note)

    def approve(self, note=""):
        if self.stored_status() != "Under review":
            raise ValueError("A permit must be under review before it can be approved.")
        self.license_number = Permit.next_license_number()
        self.expiry_date = self.add_months(date.today().isoformat(),
                                           self.validity_months(self.permit_type))
        self._add_entry("Approved", note or f"License {self.license_number} issued")

    def reject(self, reason):
        if self.stored_status() not in ("Applied", "Under review"):
            raise ValueError("Only a permit that is waiting for a decision can be rejected.")
        if len(reason.strip()) < 3:
            raise ValueError("Please give a short reason for the rejection.")
        self._add_entry("Rejected", reason)

    def renew(self):
        """Extend an approved permit by its normal validity period."""
        if self.stored_status() != "Approved":
            raise ValueError("Only an approved permit can be renewed.")
        if self.days_until_expiry() > Permit.RENEWAL_WINDOW_DAYS:
            raise ValueError(f"Renewal opens {Permit.RENEWAL_WINDOW_DAYS} days before expiry "
                             f"({self.days_until_expiry()} days left).")
        # extend from the old expiry date if still valid, otherwise from today
        base = date.today().isoformat() if self.is_expired() else self.expiry_date
        self.expiry_date = self.add_months(base, self.validity_months(self.permit_type))
        self._add_entry("Approved", f"Renewed until {self.expiry_date}")

    def update_record(self, holder_label=None, area=None):
        if holder_label:
            if len(holder_label.strip()) > 40:
                raise ValueError("Holder label must be 40 characters or fewer.")
            self.holder_label = holder_label.strip()
        if area:
            self.area = area.strip()

    def stored_status(self):
        return self.status_log[-1][1]

    def is_expired(self):
        return (self.expiry_date is not None
                and date.fromisoformat(self.expiry_date) < date.today())

    def days_until_expiry(self):
        """Days left (negative if already expired); only for approved permits."""
        return (date.fromisoformat(self.expiry_date) - date.today()).days

    def current_status(self):
        """Status shown to users: an approved permit past its date is 'Expired'."""
        if self.stored_status() == "Approved" and self.is_expired():
            return "Expired"
        return self.stored_status()

    def display_info(self):
        print(f"ID: {self.permit_id} | {self.permit_type} | {self.holder_label} | "
              f"{self.area} | Status: {self.current_status()}")
        if self.license_number:
            days = self.days_until_expiry()
            left = f"{days} days left" if days >= 0 else f"expired {-days} days ago"
            print(f"    License: {self.license_number} | Expires: {self.expiry_date} ({left})")
        for entry_date, status, note in self.status_log:
            print(f"    - {entry_date}: {status}" + (f" ({note})" if note else ""))

    # ---- class methods (Task 3)
    @classmethod
    def from_string(cls, text):
        """Create a Permit from 'type,holder label,area' e.g. 'Business, Aminata Shop, Kissy'."""
        parts = text.split(",")
        if len(parts) != 3:
            raise ValueError("Use the format: type,holder label,area")
        return cls(parts[0], parts[1], parts[2])

    @classmethod
    def next_license_number(cls):
        """Create the next license number, shared by every permit (e.g. LIC-2026-0001)."""
        cls._license_counter += 1
        return f"LIC-{date.today().year}-{cls._license_counter:04d}"

    @classmethod
    def type_options(cls):
        """Allowed permit types as text, for prompts and error messages."""
        return ", ".join(cls.PERMIT_TYPES)

    # ---- static methods (Task 3)
    @staticmethod
    def validity_months(permit_type):
        """How long each type of permit lasts, in months (general values)."""
        return {"Driving": 60, "Building": 24, "Market stall": 6}.get(permit_type, 12)

    @staticmethod
    def add_months(start_iso, months):
        """Add months to an ISO date, keeping the day valid (31 Jan + 1 month = 28/29 Feb)."""
        start = date.fromisoformat(start_iso)
        month_index = start.month - 1 + months
        year = start.year + month_index // 12
        month = month_index % 12 + 1
        day = min(start.day, calendar.monthrange(year, month)[1])
        return date(year, month, day).isoformat()

    @staticmethod
    def normalize_type(permit_type):
        """Check a permit type (any capitalisation) and return the standard form."""
        clean = permit_type.strip().capitalize()
        if clean not in Permit.PERMIT_TYPES:
            raise ValueError("Type must be one of: " + ", ".join(Permit.PERMIT_TYPES) + ".")
        return clean


# ---------------------------------------------------------------- Class 2
class PermitRegistry:
    """Stores many Permit objects in a dictionary keyed by permit ID
    (Task 2: one data structure + add/display functions)."""

    def __init__(self, office_name):
        self.office_name = office_name
        self.permits = {}  # {permit_id: Permit}

    def add_permit(self, permit):
        self.permits[permit.permit_id] = permit
        print(f"Application received. Permit ID: {permit.permit_id}.")

    def find(self, permit_id):
        return self.permits.get(permit_id.strip().upper())

    def find_by_license(self, license_number):
        """Public check: look a permit up by its license number."""
        wanted = license_number.strip().upper()
        for permit in self.permits.values():
            if permit.license_number == wanted:
                return permit
        return None

    def display_all(self):
        print(f"\n=== {self.office_name}: {len(self.permits)} permit(s) ===")
        if not self.permits:
            print("No permits yet.")
        for permit in self.permits.values():
            permit.display_info()

    def remove_permit(self, permit_id):
        """Delete a record (for example an application sent by mistake)."""
        removed = self.permits.pop(permit_id.strip().upper(), None)
        if removed is None:
            print("Permit not found.")
            return False
        print(f"Permit {removed.permit_id} removed.")
        return True

    def display_expiring(self, within_days=30):
        """Show approved permits that are expired or will expire soon."""
        print(f"\n=== Expiry alerts (next {within_days} days): {self.office_name} ===")
        found = 0
        for permit in self.permits.values():
            if permit.stored_status() == "Approved" and permit.days_until_expiry() <= within_days:
                found += 1
                days = permit.days_until_expiry()
                note = f"expires in {days} days" if days >= 0 else f"EXPIRED {-days} days ago"
                print(f"{permit.permit_id} | {permit.license_number} | {permit.permit_type} | "
                      f"{permit.holder_label} | {note}")
        if found == 0:
            print("No permits are expired or expiring soon.")
        return found

    def type_summary(self):
        """Count the permits of each type (uses the permit types tuple)."""
        print(f"\n=== Permit type summary: {self.office_name} ===")
        for permit_type in Permit.PERMIT_TYPES:
            total = sum(1 for p in self.permits.values() if p.permit_type == permit_type)
            print(f"{permit_type}: {total}")


# ---------------------------------------------------------------- Demo / menu
def demo(registry):
    """Optional sample data. Not run by default; call demo(registry) to load it."""
    p1 = Permit("Business", "Aminata Fresh Fish", "Kissy")
    p2 = Permit.from_string("Market stall, Fruit Stand 4, Wellington")   # class method
    registry.add_permit(p1)
    registry.add_permit(p2)
    p1.start_review("Documents checked")                                  # instance method
    p1.approve()
    p2.update_record(area="Kissy")
    registry.display_all()


def process_application(registry):
    permit = registry.find(input("Permit ID: "))
    if not permit:
        print("Permit not found.")
        return
    try:
        action = input("Action (review / approve / reject): ").strip().lower()
        if action == "review":
            permit.start_review(input("Short note (optional): "))
        elif action == "approve":
            permit.approve(input("Short note (optional): "))
        elif action == "reject":
            permit.reject(input("Reason for rejection: "))
        else:
            print("Please type review, approve or reject.")
            return
        print(f"Updated. {permit.permit_id} is now: {permit.current_status()}.")
    except ValueError as error:
        print(f"Error: {error}")


def menu(registry):
    while True:
        print("\n1. Apply for permit  2. Process application  3. Renew permit")
        print("4. Show all  5. Verify license  6. Expiry alerts  7. Type summary")
        print("8. Remove permit  9. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            try:
                print("Use a business or stall name. Do not enter personal ID or phone numbers.")
                text = input(f"Type,holder label,area (types: {Permit.type_options()}):\n")
                registry.add_permit(Permit.from_string(text))
            except ValueError as error:
                print(f"Error: {error}")
        elif choice == "2":
            process_application(registry)
        elif choice == "3":
            permit = registry.find(input("Permit ID: "))
            if permit:
                try:
                    permit.renew()
                    print(f"Renewed. New expiry date: {permit.expiry_date}.")
                except ValueError as error:
                    print(f"Error: {error}")
            else:
                print("Permit not found.")
        elif choice == "4":
            registry.display_all()
        elif choice == "5":
            permit = registry.find_by_license(input("License number: "))
            if permit:
                permit.display_info()
            else:
                print("No permit found with that license number.")
        elif choice == "6":
            registry.display_expiring()
        elif choice == "7":
            registry.type_summary()
        elif choice == "8":
            registry.remove_permit(input("Permit ID to remove: "))
        elif choice == "9":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    registry = PermitRegistry("District Permit Office")
    menu(registry)  # starts empty; use demo(registry) for sample data
