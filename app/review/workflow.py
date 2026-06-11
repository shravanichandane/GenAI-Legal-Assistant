from enum import Enum
from datetime import datetime

class ReviewStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    MODIFIED = "MODIFIED"

class ReviewWorkflow:
    """
    A simple state machine that tracks a document's review status.
    Transitions states from PENDING -> APPROVED | REJECTED | MODIFIED.
    """
    def __init__(self, document_id: str, current_status: ReviewStatus = ReviewStatus.PENDING):
        self.document_id = document_id
        self.status = current_status
        self.last_updated = datetime.now()
        
    def transition_to(self, new_status: ReviewStatus) -> bool:
        """
        Transition the document to a new status.
        """
        self.status = new_status
        self.last_updated = datetime.now()
        return True
        
    def approve(self) -> bool:
        return self.transition_to(ReviewStatus.APPROVED)
        
    def reject(self) -> bool:
        return self.transition_to(ReviewStatus.REJECTED)
        
    def modify(self) -> bool:
        return self.transition_to(ReviewStatus.MODIFIED)

    def get_status(self) -> str:
        """
        Get the current string value of the review status.
        """
        return self.status.value
