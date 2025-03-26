from rest_framework import serializers
from .models import AdoptionApplication, MatchingTool, AdoptionAgreement


class AdoptionApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionApplication
        fields = '__all__'
        read_only_fields = ('id', 'user', 'submitted_at')

    def validate(self, data):
        # Example: Add any additional validation if needed
        if data.get('own_or_rent') == 'rent' and not data.get('landlord_permission'):
            raise serializers.ValidationError("Landlord permission is required if renting.")
        return data

class AdoptionApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionApplication
        fields = ['id', 'status', 'updated_at']
        read_only_fields = ['id', 'updated_at']

class MatchingToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingTool
        fields = '__all__'
        read_only_fields = ['adopter', 'created_at']

class AdoptionAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionApplication
        fields = ['id', 'agreement_text']

    def update(self, instance, validated_data):
        instance.agreement_text = validated_data.get("agreement_text", instance.agreement_text)
        pdf_file = instance.generate_agreement_pdf()
        instance.agreement_pdf.save(pdf_file.name, pdf_file, save=True)
        instance.save()
        return instance

class AdoptionAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionAgreement
        fields = '__all__'
