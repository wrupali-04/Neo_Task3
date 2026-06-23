"""
Bank Account System

Demonstrates:
1. Encapsulation
2. Inheritance
3. Polymorphism
4. Custom Exceptions
5. Transfer Between Accounts
"""

# -------------------------------
# Custom Exceptions
# -------------------------------

class InsufficientFundsError(Exception):
    """Raised when savings account goes below minimum balance."""
    pass


class OverdraftLimitError(Exception):
    """Raised when current account exceeds overdraft limit."""
    pass


# -------------------------------
# Base Class
# -------------------------------

class BankAccount:
    """
    Base class for all bank accounts.
    """

    def __init__(self, owner, opening_balance):
        """
        Initialize account.

        Args:
            owner (str): Account holder name
            opening_balance (float): Initial balance
        """
        self.__owner = owner
        self.__balance = opening_balance

        self.__transactions = [
            f"Opening deposit: +{opening_balance:.1f}"
        ]

    def deposit(self, amount):
        """
        Deposit money into account.

        Args:
            amount (float): Deposit amount
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self.__balance += amount

        self.__transactions.append(
            f"Deposit: +{amount:.1f}"
        )

    def withdraw(self, amount):
        """
        Basic withdrawal logic.

        Args:
            amount (float): Amount to withdraw
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if amount > self.__balance:
            raise InsufficientFundsError(
                "Insufficient balance."
            )

        self.__balance -= amount

        self.__transactions.append(
            f"Withdrawal: -{amount:.1f}"
        )

    def get_balance(self):
        """
        Returns current balance.
        """
        return self.__balance

    def get_owner(self):
        """
        Returns account owner.
        """
        return self.__owner

    def get_statement(self):
        """
        Prints transaction statement with running balance.
        """
        print("\nACCOUNT STATEMENT")
        print("-" * 40)

        running_balance = 0

        for transaction in self.__transactions:

            if "+" in transaction:
                amount = float(
                    transaction.split("+")[1]
                )
                running_balance += amount

            elif "-" in transaction:
                amount = float(
                    transaction.split("-")[1]
                )
                running_balance -= amount

            print(
                f"{transaction} | Bal: {running_balance:.1f}"
            )

    def transfer(self, amount, target_account):
        """
        Transfer money from one account to another.

        Args:
            amount (float): Amount to transfer
            target_account (BankAccount): Target account
        """
        self.withdraw(amount)
        target_account.deposit(amount)

        print(
            f"\nRs.{amount:.1f} transferred from "
            f"{self.get_owner()} to "
            f"{target_account.get_owner()}"
        )

    # Protected helpers for subclasses

    def _get_balance(self):
        return self.__balance

    def _set_balance(self, balance):
        self.__balance = balance

    def _add_transaction(self, transaction):
        self.__transactions.append(transaction)


# -------------------------------
# Savings Account
# -------------------------------

class SavingsAccount(BankAccount):
    """
    Savings Account with minimum balance rule.
    """

    MIN_BALANCE = 500

    def __init__(
        self,
        owner,
        opening_balance,
        interest_rate
    ):
        super().__init__(owner, opening_balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        """
        Withdraw while maintaining minimum balance.
        """

        new_balance = self._get_balance() - amount

        if new_balance < self.MIN_BALANCE:
            raise InsufficientFundsError(
                "Cannot withdraw. Min balance "
                "of Rs.500 must be maintained."
            )

        self._set_balance(new_balance)

        self._add_transaction(
            f"Withdrawal: -{amount:.1f}"
        )

    def add_interest(self):
        """
        Add annual interest.
        """

        interest = (
            self._get_balance()
            * self.interest_rate
        )

        self._set_balance(
            self._get_balance() + interest
        )

        self._add_transaction(
            f"Interest credit: +{interest:.1f}"
        )


# -------------------------------
# Current Account
# -------------------------------

class CurrentAccount(BankAccount):
    """
    Current account with overdraft facility.
    """

    def __init__(
        self,
        owner,
        opening_balance,
        overdraft_limit
    ):
        super().__init__(owner, opening_balance)

        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        """
        Withdraw with overdraft support.
        """

        new_balance = self._get_balance() - amount

        if new_balance < -self.overdraft_limit:
            raise OverdraftLimitError(
                f"Overdraft limit of "
                f"Rs.{self.overdraft_limit:.0f} exceeded."
            )

        self._set_balance(new_balance)

        self._add_transaction(
            f"Withdrawal: -{amount:.1f}"
        )


# -------------------------------
# User Input Section
# -------------------------------

def create_account():
    """
    Create account using user input.
    """

    print("\n1. Savings Account")
    print("2. Current Account")

    choice = int(input("Enter choice: "))

    owner = input("Enter account holder name: ")

    balance = float(
        input("Enter opening balance: ")
    )

    if choice == 1:

        rate = float(
            input("Enter interest rate: ")
        )

        account = SavingsAccount(
            owner,
            balance,
            rate
        )

    elif choice == 2:

        limit = float(
            input("Enter overdraft limit: ")
        )

        account = CurrentAccount(
            owner,
            balance,
            limit
        )

    else:
        print("Invalid choice.")
        return None

    return account


# -------------------------------
# Main Program
# -------------------------------

print("\nCREATE FIRST ACCOUNT")
account1 = create_account()

if account1:

    print(
        "\nCurrent Balance:",
        account1.get_balance()
    )

    deposit_amount = float(
        input("\nEnter deposit amount: ")
    )

    account1.deposit(deposit_amount)

    print(
        "Balance after deposit:",
        account1.get_balance()
    )

    try:
        withdraw_amount = float(
            input(
                "\nEnter withdrawal amount: "
            )
        )

        account1.withdraw(withdraw_amount)

        print(
            "Balance after withdrawal:",
            account1.get_balance()
        )

    except (
        InsufficientFundsError,
        OverdraftLimitError
    ) as error:

        print(error)

    account1.get_statement()


# -------------------------------
# Test Case 1
# -------------------------------

print("\n")
print("=" * 50)
print("TEST CASE 1")
print("=" * 50)

try:
    acc = SavingsAccount(
        "Alice",
        1000,
        0.05
    )

    acc.deposit(500)
    acc.withdraw(900)

    print(
        "Balance:",
        acc.get_balance()
    )

    acc.withdraw(200)

except Exception as e:
    print(e)


# -------------------------------
# Test Case 2
# -------------------------------

print("\n")
print("=" * 50)
print("TEST CASE 2")
print("=" * 50)

try:
    acc = CurrentAccount(
        "Bob",
        500,
        2000
    )

    acc.withdraw(2000)

    print(
        "Balance:",
        acc.get_balance()
    )

    acc.withdraw(600)

except Exception as e:
    print(e)


# -------------------------------
# Test Case 3
# -------------------------------

print("\n")
print("=" * 50)
print("TEST CASE 3")
print("=" * 50)

acc = SavingsAccount(
    "Carol",
    2000,
    0.05
)

acc.add_interest()

acc.get_statement()

print(
    "Balance:",
    acc.get_balance()
)


# -------------------------------
# Transfer Demonstration
# -------------------------------

print("\n")
print("=" * 50)
print("TRANSFER DEMO")
print("=" * 50)

acc1 = SavingsAccount(
    "Rahul",
    5000,
    0.05
)

acc2 = CurrentAccount(
    "Priya",
    1000,
    2000
)

acc1.transfer(1000, acc2)

print(
    "Rahul Balance:",
    acc1.get_balance()
)

print(
    "Priya Balance:",
    acc2.get_balance()
)