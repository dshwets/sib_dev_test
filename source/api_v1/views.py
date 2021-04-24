import csv
import io

from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v1.models import Deals
from api_v1.serializers import FileUploadSerializer


class UploadDealsView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        try:
            decoded_file = file.read().decode()
            if not file.name.endswith('.csv'):
                raise ValueError
        except (UnicodeDecodeError, ValueError):
            return Response({"desc": "Ошибка декодирования файла, не верный формат, необходим .csv"},
                            status.HTTP_400_BAD_REQUEST, )
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)
        Deals_objects = []
        wrong_strings = {
            "invalid_data_strings:": "",
        }
        for line in reader:
            if reader.line_num == 1:
                continue
            try:
                total = int(line[2])
                qty = int(line[3])
                date = parse_datetime(line[4])
            except ValueError:
                wrong_strings["invalid_data_strings:"] += str(reader.line_num) + " "
                continue
            if date is None or total < 0 or qty < 0:
                wrong_strings["invalid_data_strings:"] += str(reader.line_num) + " "
                continue
            Deals_objects.append(Deals(
                customer=line[0],
                item=line[1],
                total=line[2],
                qty=line[3],
                date_time=make_aware(date),
            ))
        Deals.objects.bulk_create(Deals_objects)
        return Response("data is uploaded correct" if not wrong_strings else wrong_strings, status=status.HTTP_200_OK)
