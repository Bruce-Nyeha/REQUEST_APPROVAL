import enum

"""Setting up the Role-Based-Access-Control. This checks roles and protects routes."""
class UserRole(enum.Enum):
    requester = "REQUESTER"
    finance = "FINANCE"
    pastor = "PASTOR"
    admin = "ADMIN"
    

class RequestStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    

class FinanceStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    paid = "paid"


class ApprovalStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    