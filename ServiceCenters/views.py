from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ServiceCenterSerializer
from rest_framework import status
from django.http import Http404
from django.core.paginator import Paginator
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .models import DeliveryBoy, ServiceCenter,ServiceCenterBooking
from .serializers import DeliveryBoySerializer,ServiceCenterBookingSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

class CenterAddView(APIView):

    def get(self, request):
        try:
            centers = ServiceCenter.objects.all().order_by('?')
            serializer = ServiceCenterSerializer(centers, many=True)

            return Response({
                'data': serializer.data,
                'message': 'Service Center details fetched successfully'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'data': {},
                'message': 'Something went wrong: ' + str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        try:
            if not request.user.is_superuser:
                return Response({
                    'message': 'You are not authorized to perform this action'
                }, status=status.HTTP_403_FORBIDDEN)

            data = request.data
            serializer = ServiceCenterSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'Service Center added successfully'
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'data': {},
                'message': 'Something went wrong: ' + str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            



# class ServiceAddView    (APIView):
#     def get(self, request):
#         services = Service.objects.all()
#         serializer = ServiceSerializer(services, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ServiceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ServiceDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Service.objects.get(pk=pk)
#         except Service.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         service = self.get_object(pk)
#         serializer = ServiceSerializer(service)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         service = self.get_object(pk)
#         serializer = ServiceSerializer(service, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         service = self.get_object(pk)
#         service.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import ServiceCenter
# from .serializers import ServiceCenterSerializer

# class UserServiceCenterListView(APIView):
#     def get(self, request):
#         try:
#             # Filter service centers by the user who added them
#             user_service_centers = ServiceCenter.objects.filter(user=request.user)
#             serializer = ServiceCenterSerializer(user_service_centers, many=True)
#             return Response({
#                 'data': serializer.data,
#                 'message': 'Service centers added by the user fetched successfully'
#             }, status=status.HTTP_200_OK)
#         except Exception as e:
#             print(e)
#             return Response({
#                 'data': {},
#                 'message': 'Something went wrong'
#             }, status=status.HTTP_400_BAD_REQUEST)



class DeliveryAddView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        delivery_boys = DeliveryBoy.objects.all()
        serializer = DeliveryBoySerializer(delivery_boys, many=True)
        return Response({"status":1,"data":serializer.data})

    def post(self, request):
        serializer = DeliveryBoySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status":0,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class DeliveryView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return DeliveryBoy.objects.get(pk=pk)
        except DeliveryBoy.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        delivery_boy = self.get_object(pk)
        serializer = DeliveryBoySerializer(delivery_boy)
        return Response(serializer.data)

    def put(self, request, pk):
        delivery_boy = self.get_object(pk)
        serializer = DeliveryBoySerializer(delivery_boy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        delivery_boy = self.get_object(pk)
        delivery_boy.delete()
        return Response({"status":1},status=status.HTTP_204_NO_CONTENT)
    
    
# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AssignedDelivery
from .serializers import AssignedDeliverySerializer

class AssignedDeliveryView(APIView):
    def get(self, request):
        assigned_deliveries = AssignedDelivery.objects.all()
        serializer = AssignedDeliverySerializer(assigned_deliveries, many=True)
        return Response({"status":1,"data":serializer.data})

    def post(self, request):
        serializer = AssignedDeliverySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status":0,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AssignedDeliveryDetailView(APIView):
    def get_object(self, pk):
        try:
            return AssignedDelivery.objects.get(pk=pk)
        except AssignedDelivery.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        assigned_delivery = self.get_object(pk)
        serializer = AssignedDeliverySerializer(assigned_delivery)
        return Response({"status":1,"data":serializer.data})

    def put(self, request, pk):
        assigned_delivery = self.get_object(pk)
        serializer = AssignedDeliverySerializer(assigned_delivery, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":1,"data":serializer.data})
        return Response({"status":0,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
class AssignedDeliveryViewByUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        assigned_deliveries = AssignedDelivery.objects.filter(user=user)
        serializer = AssignedDeliverySerializer(assigned_deliveries, many=True)
        return Response({"status":1,"data":serializer.data})

class ServiceCenterBookingAPIView(APIView):
    def get(self, request):
        bookings = ServiceCenterBooking.objects.all()
        serializer = ServiceCenterBookingSerializer(bookings, many=True)
        return Response(data={"status":1,"data":serializer.data})

    def post(self, request):
        serializer = ServiceCenterBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"status":1,"data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(data={"status":0,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)