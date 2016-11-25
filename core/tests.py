# encoding: utf-8

from django.test import TestCase


class UserTest(TestCase):

    fixtures = ['users.json', ]

    def test_user(self):
        pass

