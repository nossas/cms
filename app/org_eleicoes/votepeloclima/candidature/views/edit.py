from .base import CandidatureBaseView

class EditCandidatureView(CandidatureBaseView):
    
    def get_current_user(self):
        return self.request.user