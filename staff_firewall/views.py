from rest_framework import viewsets
from .models import FwStaff
from .serializers import FwStaffSerializer, FwStaffDetailSerializer

class StaffFirewall(viewsets.ModelViewSet):
    queryset = FwStaff.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return FwStaffDetailSerializer
        return FwStaffSerializer