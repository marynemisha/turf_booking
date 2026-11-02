from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from turfapp.models import *
from turfapp.serializers import *
from datetime import datetime, timedelta
# Create your views here.
class TurfListCreateView(APIView):
    def get(self, request):
        qs = TurfDb.objects.all()
        serializer_instance = TurfSerializer(qs, many=True)
        return Response(data=serializer_instance.data)
    def post(self, request):
        form_data = request.data
        serializer_instance = TurfSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)


class TurfRetrieveUpdateDeleteView(APIView):
    def get(self, request, pk):
        qs = get_object_or_404(TurfDb, id=pk)
        serializer_instance = TurfSerializer(qs)
        return Response(data=serializer_instance.data)
    def put(self, request, pk):
        form_data = request.data
        turf_object = get_object_or_404(TurfDb, id=pk)
        serializer_instance = TurfSerializer(
            data=form_data,
            instance=turf_object
        )
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
    def delete(self, request, pk):
        turf_object = get_object_or_404(TurfDb, id=pk)
        turf_object.delete()
        return Response(
            data={"message": "Deleted successfully..!"}
        )


class BookingListCreateView(APIView):
    def get(self, request):
        qs = BookingDb.objects.all()
        serializer_instance = BookingSerializer(qs, many=True)
        return Response(data=serializer_instance.data)
    def post(self, request):
        form_data = request.data
        serializer_instance = BookingSerializer(data=form_data)
        if serializer_instance.is_valid():
            print(serializer_instance.validated_data)
            turf = serializer_instance.validated_data.get("turf")
            print("Turf:", turf)
            print("Validated data:", serializer_instance.validated_data)
            booking_date = serializer_instance.validated_data.get(
                "booking_date"
            )
            duration = serializer_instance.validated_data.get("duration")
           

            if not turf.is_available:
                return Response(
                    data={"message": "Turf is not available..!"}
                )
            last_booking = BookingDb.objects.filter(
                turf_id=turf.id,
                booking_date=booking_date
            ).order_by("-booking_time").first()

            if last_booking is None:
                next_time = turf.opening_time
            else:
                current_time = datetime.combine(booking_date,last_booking.booking_time)
                next_time = (current_time +timedelta(hours=last_booking.duration)).time()

            # Checking closing time
            booking_datetime = datetime.combine(booking_date,next_time)
            closing_datetime = datetime.combine(booking_date,turf.closing_time)
            completion_time = booking_datetime + timedelta(hours=duration)
            if completion_time > closing_datetime:
                return Response(
                    data={"message": "No slots available today..!"}
                )

            # Setting automatic booking time
            form_data["booking_time"] = next_time

            # Calculating amount
            form_data["amount"] = turf.price_per_hour * duration
            form_data["turf"]=turf
            qs = BookingDb.objects.create(**form_data)
            return Response(data={
                    "Message": "Booked successfully..!",
                    "Turf Name": turf.turf_name,
                    "Booking Date": form_data["booking_date"],
                    "Booking Time": form_data["booking_time"],
                    "Duration":form_data["duration"],
                    "Amount":form_data["amount"]
                    })
        else:
            return Response(data=serializer_instance.errors)

