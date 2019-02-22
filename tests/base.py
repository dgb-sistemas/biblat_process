# coding: utf-8
import uuid
import unittest


class BaseTestCase(unittest.TestCase):

    def generate_uuid_32_string(self):
        return str(uuid.uuid4().hex)
