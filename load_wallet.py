"""Cellphone Load Wallet
A program to manage a subscriber's prepaid load balance.

Run with:  python load_wallet.py
"""

import math


class LoadWallet:
    """A prepaid load wallet with an owner, mobile number, and balance."""

    SERVICE_FEE = 2.00  # charge for sending load to a different network

    def __init__(self, owner, mobile_number, balance=0.0):
        self.owner = owner
        self.mobile_number = mobile_number
        self.balance = balance

    def top_up(self, amount):
        """Add load to the wallet."""
        if amount <= 0:
            print("Error: top-up amount must be greater than zero.")
            return False
        self.balance += amount
        print(f"New balance: P{self.balance:,.2f}")
        return True

    def send_load(self, recipient, amount):
        """Send load to another number on the same network (no fee)."""
        if recipient == self.mobile_number:
            print("Error: you cannot send load to your own number.")
            return False
        if amount <= 0:
            print("Error: amount must be greater than zero.")
            return False
        if amount > self.balance:
            print(f"Error: insufficient balance. You only have P{self.balance:,.2f}.")
            return False
        self.balance -= amount
        print(f"Sent P{amount:,.2f} to {recipient}.")
        print(f"New balance: P{self.balance:,.2f}")
        return True

    def send_with_fee(self, recipient, amount):
        """Send load to a different network, with a service charge."""
        if recipient == self.mobile_number:
            print("Error: you cannot send load to your own number.")
            return False
        if amount <= 0:
            print("Error: amount must be greater than zero.")
            return False
        total = amount + self.SERVICE_FEE
        if total > self.balance:
            print(f"Error: insufficient balance. You need P{total:,.2f} "
                  f"(P{amount:,.2f} + P{self.SERVICE_FEE:,.2f} fee) "
                  f"but only have P{self.balance:,.2f}.")
            return False
        self.balance -= total
        print(f"Sent P{amount:,.2f} to {recipient} "
              f"(service fee: P{self.SERVICE_FEE:,.2f}).")
        print(f"New balance: P{self.balance:,.2f}")
        return True

    def show_balance(self):
        """Display the wallet details."""
        print(f"Owner         : {self.owner}")
        print(f"Mobile Number : {self.mobile_number}")
        print(f"Balance       : P{self.balance:,.2f}")


# ---------- safe input helpers ----------
def get_name(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def get_mobile(prompt):
    """Mobile number must be 11 digits starting with 09."""
    while True:
        value = input(prompt).strip()
        if value.isdigit() and len(value) == 11 and value.startswith("09"):
            return value
        print("Invalid number. Enter 11 digits starting with 09 (e.g. 09171234567).")


def get_amount(prompt, allow_zero=False):
    """Accepts amounts like 50, 50.5 or P50. Rejects letters and negatives."""
    while True:
        raw = input(prompt).strip().upper().lstrip("P").replace(",", "")
        try:
            value = float(raw)
        except ValueError:
            print("Invalid amount. Please enter a number (e.g. 50 or P50).")
            continue
        if not math.isfinite(value) or value < 0 or (value == 0 and not allow_zero):
            print("Amount must be a valid number greater than zero."
                  if not allow_zero else "Amount cannot be negative.")
            continue
        return value


def main():
    owner = get_name("Enter owner name: ")
    mobile = get_mobile("Enter mobile number: ")
    balance = get_amount("Enter starting balance: P", allow_zero=True)
    wallet = LoadWallet(owner, mobile, balance)

    while True:
        print("\n----- MENU -----")
        print("1. Top Up Load")
        print("2. Send Load (same network)")
        print("3. Send Load (other network, with fee)")
        print("4. Show Balance")
        print("5. Exit")

        choice = input("\nChoose an option (1-5): ").strip()

        if choice == "1":
            amount = get_amount("Enter top-up amount: P")
            wallet.top_up(amount)
        elif choice == "2":
            recipient = get_mobile("Enter recipient number: ")
            amount = get_amount("Enter amount to send: P")
            wallet.send_load(recipient, amount)
        elif choice == "3":
            print(f"Note: a service fee of P{LoadWallet.SERVICE_FEE:,.2f} applies.")
            recipient = get_mobile("Enter recipient number: ")
            amount = get_amount("Enter amount to send: P")
            wallet.send_with_fee(recipient, amount)
        elif choice == "4":
            wallet.show_balance()
        elif choice == "5":
            print("Thank you for using Cellphone Load Wallet. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting program. Goodbye!")
