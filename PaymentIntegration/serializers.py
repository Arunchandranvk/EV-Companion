from rest_framework import serializers
from  PaymentIntegration.models import Transaction


class RazorpayOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField()


class TransactionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["username","payment_id", "order_id", "signature", "amount"]