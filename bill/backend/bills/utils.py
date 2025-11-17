import calendar
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

import random


class BillStatus(Enum):
    PROCESSING = (
        "Processing",
        "This bill is currently in processing, it can take approx. 1-2 hours depending on the time of day.",
    )
    SCHEDULED = (
        "Scheduled",
        "This bill is scheduled to be paid and will be paid on the due date, you're in good hands!, etc.)",
    )
    UNABLE_TO_PAY = (
        "Unable to pay",
        "This bill can't be paid at the moment, please contact our support team for more information.",
    )
    PAID = "Paid", "This bill has been paid successfully, thank you for using Deferit!"

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: str, description: str = None):
        self._description = description

    def __str__(self):
        return self.value

    def to_dict(self):
        return {"status": self.value, "description": self._description}

    @property
    def description(self):
        return self._description


class InstalmentStatus(Enum):
    UNPAID = "Unpaid"
    PAID = "Paid"


biller_names: list[str] = [
    "Mobile Co.",
    "Gas Co.",
    "Energy Co.",
    "Internet Co.",
    "Water Co.",
    "Council Co.",
    "Insurance Co.",
]


@dataclass
class Instalment:
    """A bill is split into multiple instalments to be paid over time.
    The due date of the instalments is typically every 14 days and the amount is
    the total bill amount divided by the number of instalments.
    """

    amount: float
    due: datetime
    status: InstalmentStatus

    def to_dict(self):
        return {"amount": self.amount, "due": self.due, "status": self.status.value}


@dataclass
class Bill:
    """Represents a bill uploaded by a customer and it's current status.
    Some notes about the bill status:
    1. Once created, the bill status should be set to PROCESSING.
      This status indicates the bill is being checked for issues.
    2. Once we have checked the bill for issues:
        - If the bill has no issues then:
            - The bill status should be set to SCHEDULED to indicate
                the bill will be paid by a scheduled task.
            - The instalments should be generated based on the bill amount
              with an UNPAID status.
        - If the bill has issues then:
            - The bill status should be set to UNABLE_TO_PAY to indicate
                the bill can't be paid.
    3. We take payment from the customer for the first instalment:
        - If the payment succeeds then:
            - The first instalment status should be set to PAID.
            - The bill status should be set to PAID to indicate the customers bill
              has been paid. Note that not all instalments have been paid yet.
        - If the payment fails then:
            - The first instalment status should remain UNPAID.
            - The bill status should be set to UNABLE_TO_PAY.
    """

    id: int  # unique identifier for the bill
    biller: str  # Name of the biller
    images: list[str]  # list of URLs to images of the bill
    amount: float  # Total amount to be paid
    due: datetime  # The date the bill is due
    status: BillStatus  # The current status of the bill
    instalments: list[Instalment]  # List of instalments to be paid

    def to_dict(self):
        return {
            "id": self.id,
            "biller": self.biller,
            "images": self.images,
            "amount": self.amount,
            "due": self.due,
            "status": self.status.to_dict(),
            "instalments": [x.to_dict() for x in self.instalments],
        }


def generate_instalments(
    bill_amount: float, start_date: datetime, num_instalments=4
) -> list[Instalment]:
    instalments = []
    instalment_amount = bill_amount / num_instalments
    for x in range(num_instalments):
        instalments.append(
            Instalment(
                amount=instalment_amount,
                due=start_date + timedelta(days=14 * x),
                status=InstalmentStatus.UNPAID,
            )
        )
    return instalments


def generate_bills(num_bills=10) -> list[Bill]:
    random.seed(42)
    year = 2024
    bills = []
    for bill_id in range(num_bills):
        month = random.randint(1, 12)
        day_of_month = calendar.monthrange(year, month)
        day = random.randint(1, day_of_month[1])
        bill_due = datetime.strptime(f"2024-{month:02}-{day:02}", "%Y-%m-%d")
        bill_amount = random.randint(100, 100000) / 100
        bill_status = random.choice(list(BillStatus))
        bill_images = ["https://via.placeholder.com/150"]
        bills.append(
            Bill(
                bill_id,
                random.choice(biller_names),
                bill_images,
                bill_amount,
                bill_due,
                bill_status,
                generate_instalments(bill_amount=bill_amount, start_date=bill_due),
            )
        )
    return bills
