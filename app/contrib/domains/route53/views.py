from django.shortcuts import render

from .entries import Manager
from .models import HostedZone, RecordSet


def index(request):
    ctx = {"hosted_zones": HostedZone.objects.all()}

    return render(request, "route53/hosted_zone/list.html", ctx)


def detail(request, hosted_zone_id: str):
    hosted_zone_id = "/hostedzone/" + hosted_zone_id

    ctx = {
        "hosted_zone_id": hosted_zone_id,
        "records": RecordSet.objects.filter(hosted_zone_id=hosted_zone_id),
        "name_servers": [],
    }

    return render(request, "route53/hosted_zone/detail.html", ctx)


def record(request, hosted_zone_id: str, record_name: str, record_type: str):
    qs = Manager()
    hosted_zone_id = "/hostedzone/" + hosted_zone_id
    response = qs.test_dns_answer(hosted_zone_id, record_name, record_type)

    ctx = {"response": response}

    return render(request, "route53/hosted_zone/detail.html", ctx)
