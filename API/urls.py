from django.urls import path
from UserAccounts.views import RegisterView, LoginView, EditProfile,UserProfileView
from VehicleInfo.views import VehiclesAddView
from ChargingStations.views import StationsAddView
from PaymentIntegration.views import RazorpayOrderAPIView, TransactionAPIView
from ServiceCenters.views import CenterAddView, DeliveryAddView, DeliveryView, AssignedDeliveryView, ServiceCenterBookingAPIView,AssignedDeliveryDetailView, AssignedDeliveryViewByUser
from ChargingStations.views import UserChargingStationListView, BookedChargingStationView,BookedChargingStationDetailView,AssignChargingStationToUserAPIView, UserBookedChargingStationView
urlpatterns = [
    #User APIs
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('edit/', EditProfile.as_view()),
    path('addVehicle/', VehiclesAddView.as_view()),
    path('viewprofile/',UserProfileView.as_view()),
    
    #Charging Station APIs
    path('addStations/', StationsAddView.as_view()),
    # path('userChargingStations/', UserChargingStationListView.as_view()),
    path('bookedChargingStations/', BookedChargingStationView.as_view()),
    path('user-booked-charging-stations/', UserBookedChargingStationView.as_view(), name='user-booked-charging-stations'),
    path('bookedChargingStations/<int:pk>/', BookedChargingStationDetailView.as_view()),
    # path('assignChargingStationtoUser/', AssignChargingStationToUserAPIView.as_view()),

    
    #Payments APIs
    path('createOrder/', RazorpayOrderAPIView.as_view()),
    path('completeOrder/', TransactionAPIView.as_view()),
    
    #Service Center APIs
    path('addServiceCenter/', CenterAddView.as_view()),
    path("servicebook/",ServiceCenterBookingAPIView.as_view()),
    # path('user_service_centers/', UserServiceCenterListView.as_view()),
    # path('addServices/', ServiceAddView.as_view()),
    # path('showService/<int:pk>/', ServiceDetail.as_view()),
     
    #Delivery APIs
    path('addDeliveryBoy/', DeliveryAddView.as_view()),
    path('showDeliveryBoy/<int:pk>/', DeliveryView.as_view()),
    
    path('assignedDeliveries/', AssignedDeliveryView.as_view()),
    path('assignedDeliveries/<int:pk>/', AssignedDeliveryDetailView.as_view()),
    path('assignDeliveryBoytoUser/', AssignedDeliveryViewByUser.as_view()),
    
   

]