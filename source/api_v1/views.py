import csv
import io

from datetime import timedelta

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Sum
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v1.models import Deal
from api_v1.serializers import FileUploadSerializer, TopClientSerializer


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
            Deals_objects.append(Deal(
                customer=line[0],
                item=line[1],
                total=total,
                qty=qty,
                date_time=make_aware(date),
            ))
        Deal.objects.bulk_create(Deals_objects)
        return Response("data is uploaded correct" if not wrong_strings['invalid_data_strings:'] else wrong_strings,
                        status=status.HTTP_200_OK)


class GetTopCustomers(APIView):
    def get(self, request, *args, **kwargs):
        try:
            last_request_time = Deal.objects.last().created_at
        except AttributeError:
            return Response({"response": "No data"}, 200)
        last_request_time_delta = last_request_time - timedelta(seconds=1)
        all_clients = Deal.objects.filter(created_at__range=(last_request_time_delta,
                                                             last_request_time))
        top_5_clients = all_clients.values('customer').annotate(gems=ArrayAgg('item', distinct=True),
                                                                total=Sum('total')).order_by('-total')[:5]
        for client in top_5_clients:
            same_gems = set()
            for _ in top_5_clients:
                gems_set = set(client['gems'])
                if client == _:
                    continue
                gems_set.intersection_update(_['gems'])
                same_gems.update(gems_set)
            client['gems'] = list(same_gems)
        slr = TopClientSerializer(top_5_clients, many=True)
        return Response({"response": slr.data}, 200)
