import json
import datetime
import collections

from django import http
from django.views import generic
from django.db import transaction

from . import models


DATETIME_FORMAT = "%Y-%m-%d %H:%M"


class AvailabilitySlotCreateView(generic.View):
    """
    Create availability timeslot for person

    Request:
    {
        "persion_id": <Person.id>,
        "time": "YYYY-MM-DD HH:MM"
    }

    Response:
    {}
    """
    def post(self, request):
        data = json.loads(request.body)

        person_id = int(data['person_id'])
        time = datetime.datetime.strptime(data['time'], DATETIME_FORMAT)
        assert time.minute == 0

        models.AvailabilitySlot.objects.create(person_id=person_id, time=time)

        return http.JsonResponse({})


class PersonsAvailabilitySlotListView(generic.View):
    """
    Get list of common to all given persons availability slots

    Request:
    {
        "persons": [<Peron.id>, <Persion.id>, ...],
        "time": "YYYY-MM-DD HH:MM"
    }

    Response:
    {
        "time": ["YYYY-MM-DD HH:MM", "YYYY-MM-DD HH:MM", ...]
    }
    """

    def post(self, request):
        data = json.loads(request.body)

        # skip validation, assume at least one id is passed, all ids
        # are valid and there is not duplicates
        persons = data['persons']

        all_slots = models.AvailabilitySlot.objects.filter(
            person__in=persons,
            time__gte=datetime.datetime.now(),
        ).values_list('time', flat=True)

        available_slots = sorted(
            time.strftime(DATETIME_FORMAT)
            for time, count in collections.Counter(all_slots).items()
            if count == len(persons)
        )

        return http.JsonResponse({
            "time": available_slots,
        })


class InterviewCreateView(generic.View):
    """
    Schedule interview sessions for given persons at given timeslot

    Request:
    {
        "persons": [<Person.id>, <Person.id>, ...],
        "time": "YYYY-MM-DD HH:MM"
    }

    Response:
    {}
    """

    @transaction.atomic
    def post(self, request):
        data = json.loads(request.body)

        persons = data['persons']
        assert len(persons) > 1

        time = datetime.datetime.strptime(data['time'], DATETIME_FORMAT)

        slots_qset = models.AvailabilitySlot.objects.filter(
            person__in=persons,
            time=time,
        ).select_for_update()

        if slots_qset.count() != len(persons):
            raise Exception("not all persons are available at specified time")

        slots_qset.delete()

        interview = models.Interview.objects.create(time=time)
        interview.persons.set(persons)

        return http.JsonResponse({})
