import json
import datetime

from django import test

from interviews import models
from interviews import views


class InterviewsTestCase(test.TestCase):
    def setUp(self):
        # Three persons enough for any test! (actually no)
        self.person_1 = models.Person.objects.create()
        self.person_2 = models.Person.objects.create()
        self.person_3 = models.Person.objects.create()

    def send_json(self, url, data):
        return self.client.post(
            url,
            json.dumps(data),
            "application/json",
        )

    def test_availability_slot_create(self):
        time_str = "2018-01-01 01:00"

        resp = self.send_json(
            "/api/slot/add/",
            {
                "person_id": self.person_1.id,
                "time": time_str,
            },
        )

        self.assertEqual(resp.status_code, 200)

        slots_qset = models.AvailabilitySlot.objects.filter(person=self.person_1)

        self.assertEqual(slots_qset.count(), 1)

        slot = slots_qset.get()
        self.assertEqual(
            slot.time.strftime(views.DATETIME_FORMAT),
            time_str,
        )

    def test_availability_slot_list_empty(self):
        resp = self.send_json("/api/slot/", {"persons": [self.person_1.id]})

        self.assertEqual(resp.json(), {"time": []})

    def test_availability_slot_list(self):
        models.AvailabilitySlot.objects.create(person=self.person_1, time=datetime.datetime(2100, 1, 1, 0, 0, 0))
        models.AvailabilitySlot.objects.create(person=self.person_1, time=datetime.datetime(2100, 1, 1, 1, 0, 0))
        models.AvailabilitySlot.objects.create(person=self.person_2, time=datetime.datetime(2100, 1, 1, 1, 0, 0))
        models.AvailabilitySlot.objects.create(person=self.person_2, time=datetime.datetime(2100, 1, 1, 2, 0, 0))

        resp = self.send_json("/api/slot/", {"persons": [self.person_1.id, self.person_2.id]})

        self.assertEqual(resp.json(), {"time": ["2100-01-01 01:00"]})

    def test_interview_create(self):
        models.AvailabilitySlot.objects.create(person=self.person_1, time=datetime.datetime(2100, 1, 1, 0, 0, 0))
        models.AvailabilitySlot.objects.create(person=self.person_1, time=datetime.datetime(2100, 1, 1, 1, 0, 0))
        models.AvailabilitySlot.objects.create(person=self.person_2, time=datetime.datetime(2100, 1, 1, 1, 0, 0))
        models.AvailabilitySlot.objects.create(person=self.person_2, time=datetime.datetime(2100, 1, 1, 2, 0, 0))

        person_ids = [self.person_1.id, self.person_2.id]
        resp = self.send_json(
            "/api/interview/add/",
            {
                "persons": person_ids,
                "time": "2100-01-01 01:00",
            },
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            models.Interview.objects.filter(
                persons__in=person_ids,
                time=datetime.datetime(2100, 1, 1, 1, 0, 0),
            ).distinct().count(),
            1,
        )

        with self.assertRaises(Exception):
            self.send_json(
                "/api/interview/add/",
                {
                    "persons": person_ids,
                    "time": "2100-01-01 01:00",
                },
            )

        self.assertEqual(models.Interview.objects.all().count(), 1)
