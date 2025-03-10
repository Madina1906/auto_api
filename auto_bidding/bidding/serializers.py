from rest_framework import serializers
from .models import AutoPlate, Bid

class AutoPlateSerializer(serializers.ModelSerializer):
    highest_bid = serializers.SerializerMethodField()

    class Meta:
        model = AutoPlate
        fields = ['id', 'plate_number', 'description', 'deadline', 'is_active', 'highest_bid']

    def get_highest_bid(self, obj):
        highest = obj.bids.order_by('-amount').first()
        return highest.amount if highest else None

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'amount', 'plate', 'created_at']
