# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from mainsite.models import Service
from mainsite.models import GlobalRequestCancellation
from mainsite.models import GlobalRequestTracer


from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

import json


class ServiceTestCase(TestCase):
	def setUp(self):
		Service.objects.create(name='1')
		Service.objects.create(name='2')
		Service.objects.create(name='3')
		Service.objects.create(name='4')
		pass;

	def test_service(self):
		"""Animals that can speak are correctly identified"""
		cnt = Service.objects.all().count()
		self.assertEqual(cnt, 4)

class ServiceDiscoveryTestCase(TestCase):
	"""Test suite for the api views."""

	def setUp(self):
		"""Define the test client and other test variables."""
		self.client = APIClient()
		self.url = reverse('api.service_register_view',kwargs={'version': 1 })
		service_data = {"name": "test"}
		response = self.client.post(self.url, data=service_data,
			format='json')

	def test_servicediscovery_post_service(self):
		"""Test the api has bucket creation capability."""
		service_data = {"name": "test2"}
		response = self.client.post(self.url, data=service_data,
			format='json')
		self.assertEqual(response.status_code, 200)

	def test_servicediscovery_get_service(self):
		"""Test the api can get a given bucketlist."""

		# service_obj=Service(name="test")
		# service_obj.save()
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)


	def test_servicediscovery_put_service(self):
		"""Test the api has bucket creation capability."""
		service_data = {"name": "test"}
		response = self.client.post(self.url, data=service_data,
			format='json')
		service_data = {"name": "test","old_name": "test"}
		response = self.client.put(self.url, data=service_data,
			format='json')
		self.assertEqual(response.status_code, 200)


	def test_servicediscovery_delete_service(self):
		"""Test the api has bucket creation capability."""

		service_data = {"name": "test"}
		response = self.client.post(self.url, data=service_data,
			format='json')
		response = self.client.delete(self.url, data=service_data,
			format='json')

		self.assertEqual(response.status_code, 200)


class ServiceInvokerTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.service_data ={"request_id": "test-4","company_id": "1","service_id": 5,"response": "response-1","response_status": "200"}
        service_register= {"name": "test"}
        service_url=reverse('api.service_register_view',kwargs={'version': 1 })

        response = self.client.post(service_url, data=service_register,
        	format='json')
        self.service_data["service_id"]=response.content["id"]
        self.url = reverse('api.request_invoker',kwargs={'version': 1 })

    def test_service_invoker_can_invoke_a_service(self):
        """Test the api has bucket creation capability."""
        self.response = self.client.post(self.url, data=self.service_data,
            format='json')

        self.assertEqual(self.response.status_code, 200)



class GlobalCancellationTestCase(TestCase):
	"""Test suite for the api views."""

	def setUp(self):
		"""Define the test client and other test variables."""
		self.client = APIClient()
		self.url = reverse('api.global_cancellation_view',kwargs={'version': 1 })

	def test_cancellation_post_service(self):
		"""Test the api has bucket creation capability."""
		service_data ={"request_id": "test-4","request_status": "2"}
		response = self.client.post(self.url, data=service_data,
			format='json')

		self.assertEqual(response.status_code, 200)

	def test_cancellation_get_service(self):
		"""Test the api can get a given bucketlist."""
		service_data ={"request_id": "test-4"}

		response = self.client.get(self.url, service_data,
		format='json')
		self.assertEqual(response.status_code, 200)
		# self.assertContains(response, bucketlist)


	def test_cancellation_put_service(self):
		"""Test the api has bucket creation capability."""
		service_data ={"request_id": "test-4","request_status": "1"}
		response = self.client.put(self.url, data=service_data,
			format='json')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, service_data)

	def test_cancellation_delete_service(self):
		"""Test the api has bucket creation capability."""
		service_data ={"request_id": "test-4","request_status": "1"}
		response = self.client.delete(self.url, data=service_data,
			format='json')

		self.assertEqual(response.status_code, 200)


