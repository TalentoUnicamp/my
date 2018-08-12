from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api, views

router = DefaultRouter()
router.register(r'company', api.CompanyViewset)
router.register(r'employee', api.EmployeeViewset)
router.register(r'scan', api.ScanViewset)

apipatterns = router.urls

apipatterns += [
    path('fetch_scan_hacker/', api.FetchScanHacker.as_view(), name='fetch_scan_hacker'),
    path('scan_hacker', api.ScanHacker.as_view(), name='scan_hacker'),
    path('fetch_checkin_employee/', api.FetchCheckinEmployee.as_view(), name='fetch_checkin_employee'),
    path('checkin_employee', api.CheckinEmployee.as_view(), name='checkin_employee')
]

app_name = 'company'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api'),
    path('', views.CompanyView.as_view(), name='index')
]
