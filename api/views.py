from django.shortcuts import render
from django.http.response import HttpResponse

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import Response
import pika
import json

from .models import PendingStore, Store, Product
from django.core import serializers

# Create your views here.
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        request_data = request.query_params
        search = request_data.get("q")
        if search:
            self.queryset = Product.objects.filter(name__contains=search)

        return super().list(request, *args, **kwargs)


@api_view(['POST'])
def propose(request):
    string = request.body.decode("utf-8")
    objectJson = json.loads(string)
    url = "https://{}.myshopify.com".format(objectJson['name'])
    try:
        store = PendingStore.objects.get(url=url)
        if store is not None:
            return Response({"message": "This store exists", "success": False})
    except PendingStore.DoesNotExist:
        connection = pika.BlockingConnection(pika.URLParameters('amqp://rabbitmq:rabbitmq@rabbit:5672/'))
        channel = connection.channel()
        channel.exchange_declare(exchange='store', exchange_type='direct', durable=False, auto_delete=False)
        result = channel.queue_declare(queue='propose', durable=False, exclusive=False, auto_delete=False)
        queue_name = result.method.queue
        channel.queue_bind(exchange='store', queue=queue_name, routing_key='propose')
        body = request.body
        channel.basic_publish(exchange='store', routing_key='propose', body=body)
        channel.close()
        return Response({"message": "Done", "success": True})


@api_view(['POST'])
def add(request):
    string = request.body.decode("utf-8")
    objectJson = json.loads(string)
    name = objectJson['name']
    url = "https://{}.myshopify.com".format(name)
    try:
        pendingStore = PendingStore.objects.get(url=url)
        if pendingStore.status != "approved":
            pendingStore.status = "approved"
            pendingStore.save()
    except PendingStore.DoesNotExist:
        print("continue")

    try:
        store = Store.objects.get(url=url)
        return Response({"message": "This store exists", "success": False})
    except Store.DoesNotExist:
        store = Store(url=url, name=name, status="pending")
        store.save()
        connection = pika.BlockingConnection(pika.URLParameters('amqp://rabbitmq:rabbitmq@rabbit:5672/'))
        channel = connection.channel()
        channel.exchange_declare(exchange='store', exchange_type='direct', durable=False, auto_delete=False)
        result = channel.queue_declare(queue='add', durable=False, exclusive=False, auto_delete=False)
        queue_name = result.method.queue
        channel.queue_bind(exchange='store', queue=queue_name, routing_key='add')
        body = json.dumps({"id": store.id, "url": store.url}).encode("utf-8")
        channel.basic_publish(exchange='store', routing_key='add', body=body)
        channel.close()
        return Response({"message": "Done", "success": True})
