from rest_framework.views import APIView
from accounts import serializers
from rest_framework.response import Response


class FcRegisterView(APIView):
    serializer_class = serializers.FcRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)