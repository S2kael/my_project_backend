from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse

from rest_framework import viewsets
from rest_framework import permissions

import pika


# Create your views here.

class ShopView(viewsets.ViewSet):
    pass


def test(request):
    connection = pika.BlockingConnection(pika.URLParameters('amqp://rabbitmq:rabbitmq@rabbit:5672/'))
    channel = connection.channel()
    channel.exchange_declare(exchange='music', exchange_type='direct', durable=False, auto_delete=False)
    result = channel.queue_declare(queue='soundcloud_queue', durable=False, exclusive=False, auto_delete=False)
    queue_name = result.method.queue
    channel.queue_bind(exchange='music', queue=queue_name, routing_key='soundcloud')
    mystring = "Hello world"
    data = mystring.encode('utf-8')
    channel.basic_publish(exchange='music', routing_key='soundcloud', body=data)

    channel.close()
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    return HttpResponse("Test")
