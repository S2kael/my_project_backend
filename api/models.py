from django.db import models


# Create your models here.

class PendingStore(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.TextField()
    status = models.CharField(max_length=15)
    total_products = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pending_stores"


class Store(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.TextField()
    status = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stores"


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=15)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tags"


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    url = models.TextField()
    image = models.JSONField()
    price = models.TextField()
    attribute = models.JSONField(null=True)
    description = models.TextField(default="", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"


class ProductTag(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_tags"


class DataPendingToSync(models.Model):
    id = models.BigAutoField(primary_key=True)
    object = models.ForeignKey(Product, on_delete=models.CASCADE)
    index = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    parent_type = models.CharField(max_length=10)
    parent = models.IntegerField()
    data = models.JSONField()
    is_synced = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "data_pending_to_sync"
