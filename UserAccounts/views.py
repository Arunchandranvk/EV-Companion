from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer,EditSerializer,UserProfileSerializer
from rest_framework import status
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class RegisterView(APIView):

    def post(self,request):
        try:
            data=request.data
            serializer=RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'status':0,
                    'data':serializer.errors,
                    'message':'something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                    'status':1,
                    'message':'Account created'
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                    'status':0,
                    'error':serializer.errors,
                    'message':'something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': 0,
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            response = serializer.get_jwt_token(data)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 0,
                'data': str(e),
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
            
class UserProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response({"status":1,"data":serializer.data})

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class EditProfile(APIView):
    # permission_classes=[IsAuthenticated]
    # authentication_classes=[JWTAuthentication]
    def get(self, request):
        try:
            user_details = CustomUser.objects.get(id=request.user.id)
            serializer=EditSerializer(user_details)
            return Response({
                    'status':1,
                    'data':serializer.data,
                    'message':'User details fetched successfully'
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
            current_user = CustomUser.objects.get(id=request.user.id)
            print(current_user)
            if not current_user:
                return Response({
                    'status':0,
                    'message':'Not a valid user id'
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != current_user:
                return Response({
                    'status':0,
                    'data':{},
                    'message':'You are not authorized'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = EditSerializer(current_user, data=data, partial=True)


            if not serializer.is_valid():
                return Response({
                    'status':0,
                    'data':{},
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
                    'data':{},
                    'message':'something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)


