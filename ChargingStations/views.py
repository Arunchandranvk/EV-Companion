from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ChargingStationSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404
from UserAccounts.models import CustomUser
from ChargingStations.models import ChargingStation

# Create your views here.
class StationsAddView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            vehicles = ChargingStation.objects.all().order_by('?')
            serializer = ChargingStationSerializer(vehicles, many=True)

            return Response({
                'data': serializer.data,
                'status': 1,
                'message': 'Charging Station details fetched successfully'
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                'status': 0,
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

        
    def post(self, request):
        try:
            current_user = CustomUser.objects.get(id=request.user.id)
            print(current_user)
            if not current_user.is_superuser:
                return Response({
                    'status':0,
                    'message': 'You are not authorized to perform this action'
                }, status=status.HTTP_403_FORBIDDEN)
            data=request.data.copy()
            data['user']=request.user.id
            print(request.user)
            serializer=ChargingStationSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'status':0,
                    'message':'something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                    'data':serializer.data,
                    'status':1,
                    'message':'Station added successfully'
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({
                    'status':0,
                    'message':'something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
        try:
            data=request.data
            station=ChargingStation.objects.filter(uid=data.get('uid'))
            current_user = CustomUser.objects.get(id=request.user.id)
            if not station.exists():
                return Response({
                    'status':0,
                    'message':'Not a valid station id'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not current_user.is_superuser:
                return Response({
                    'status':0,
                    'message':'You are not authorized'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer=ChargingStationSerializer(station[0],data=data,partial=True)

            if not serializer.is_valid():
                return Response({
                    'status':0,
                    'message':'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                    'status':1,
                    'data':serializer.data,
                    'message':'Successfully updated'
                }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                    'status':0,
                    'message':'something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        try:
            data=request.data
            station=ChargingStation.objects.filter(uid=data.get('uid'))
            current_user = CustomUser.objects.get(id=request.user.id)
            if not station.exists():
                return Response({
                    'status':0,
                    'message':'Not a valid station id'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not current_user.is_superuser:
                return Response({
                    'status':0,
                    'message':'You are not authorized'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            station[0].delete()

            return Response({
                    'data':{},
                    'status':1,
                    'message':'Successfully deleted'
                }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                    'data':{},
                    'status':0,
                    'message':'something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)


class UserChargingStationListView(APIView):
    def get(self, request):
        try:
            # Filter charging stations by the user who added them
            user_stations = BookedChargingStation.objects.filter(user=request.user.id)
            serializer = BookedChargingStationSerializer(user_stations, many=True)
            print(serializer.data)
            return Response({
                'status':1,
                'data': serializer.data,
                'message': 'Charging stations added by the user fetched successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                'status':0,
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
            
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BookedChargingStation
from .serializers import BookedChargingStationSerializer

from rest_framework.permissions import IsAuthenticated

class BookedChargingStationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check if the user is an admin
        # if not request.user.is_staff:
        #     return Response({'status': 0, 'message': 'You are not authorized to view this data'}, status=status.HTTP_403_FORBIDDEN)

        # If the user is an admin, retrieve all booked charging stations
        booked_charging_stations = BookedChargingStation.objects.all()
        serializer = BookedChargingStationSerializer(booked_charging_stations, many=True)
        return Response({'status': 1, 'data': serializer.data})

    def post(self, request):
        print("Request data:", request.data) 
        serializer = BookedChargingStationSerializer(data=request.data)
        
        if serializer.is_valid():
            # Set the user for the booked charging station to the current user
            serializer.save(user=request.user)
            
            charging_station_id = request.data.get('charging_station')
            try:
                charging_station = ChargingStation.objects.get(pk=charging_station_id)
                charging_station.booked_status = True
                charging_station.save()
            except ChargingStation.DoesNotExist:
                return Response({'status': 0, 'message': 'Charging station not found'}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({'status': 1, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 0, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework import generics

class UserBookedChargingStationView(generics.ListAPIView):
    serializer_class = BookedChargingStationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter booked charging stations for the current user
        return BookedChargingStation.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add status code based on whether queryset is empty or not
        status_code = 1 if data else 0
        return Response({"status": status_code, "data": data}, status=status.HTTP_200_OK)

class BookedChargingStationDetailView(APIView):
    def get_object(self, pk):
        try:
            return BookedChargingStation.objects.get(pk=pk)
        except BookedChargingStation.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        booked_charging_station = self.get_object(pk)
        serializer = BookedChargingStationSerializer(booked_charging_station)
        return Response({'status':1,'data':serializer.data})

    def put(self, request, pk):
        booked_charging_station = self.get_object(pk)
        serializer = BookedChargingStationSerializer(booked_charging_station, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':1,'data':serializer.data})
        return Response({'status':0,'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class AssignChargingStationToUserAPIView(APIView):
    def post(self, request):
        delivery_boy_id = request.data.get('delivery_boy_id')
        user_id = request.data.get('user_id')
        
        try:
            booked_charging_station = BookedChargingStation.objects.get(user_id=user_id)
            booked_charging_station.delivery_boy_id = delivery_boy_id
            booked_charging_station.save()
            return Response({'status':1,'message': 'Delivery boy assigned successfully'}, status=status.HTTP_200_OK)
        except BookedChargingStation.DoesNotExist:
            return Response({'status':0,'message': 'Booked charging station not found'}, status=status.HTTP_404_NOT_FOUND)


