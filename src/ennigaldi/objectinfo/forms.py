from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.shortcuts import get_object_or_404
from historicdate.models import HistoricDate
from .models import *

# The TitleForm form populates the preferred_title OneToOneField
# in the ObjectRegister. It needs to be a separate form,
# not an inlineformset, as per
# http://stackoverflow.com/questions/27832076/modelform-with-onetoonefield-in-django
class TitleForm(ModelForm):
    class Meta:
        model = ObjectName
        fields = ['title', 'title_type', 'lang', 'translation', 'currency', 'level', 'note', 'source']

class ObjectEntry(ModelForm):
    def __init__(self, *args, **kwargs):
        objectname_id = kwargs.pop('objectname_id', None)
        super(ObjectEntry, self).__init__(*args, **kwargs)

        self.fields['preferred_title'].initial = get_object_or_404(ObjectName, pk=int(objectname_id))

    class Meta:
        model = ObjectRegister
        fields = ['preferred_title', 'snapshot', 'work_type', 'source', 'brief_description', 'description_source', 'comments', 'distinguishing_features', 'normal_unit']


class InscriptionForm(ModelForm):
    class Meta:
        model = Inscription
        fields = ['inscription_type', 'inscription_position', 'inscription_text', 'inscription_language', 'inscription_script', 'inscription_notes', 'inscription_method']

inscription_formset = inlineformset_factory(ObjectRegister, Inscription, form=InscriptionForm, extra=3)

class NumberForm(ModelForm):
    class Meta:
        model = OtherNumber
        fields = ['object_number', 'object_number_type']

number_formset = inlineformset_factory(ObjectRegister, OtherNumber, form=NumberForm, extra=2)

class ProductionForm(ModelForm):
    class Meta:
        model = Production
        fields = []

class SpecimenForm(ModelForm):
    class Meta:
        model = Specimen
        fields = ['physical_description', 'colour', 'description_display', 'specimen_age', 'specimen_age_qualification', 'specimen_age_unit', 'phase', 'sex', 'object_date']

class ArtifactForm(ModelForm):
    class Meta:
        model = Artifact
        fields = ['physical_description', 'colour', 'technical_attribute', 'description_display']

class InstanceForm(ModelForm):
    class Meta:
        model = WorkInstance
        fields = ['physical_description', 'colour', 'technical_attribute', 'description_display']

class DimensionForm(ModelForm):
    class Meta:
        model = Dimension
        fields = ['dimension_part', 'dimension_type', 'dimension_value', 'dimension_value_qualifier', 'dimension_deprecated']

dimension_formset = inlineformset_factory(ObjectRegister, Dimension, form=DimensionForm, extra=4)


###########################################################
# The following is part of Description---commented here
# just so we remember to put it where it belongs later on.

# Colour as a M2M field is not being used for now.
# class ColourEntry(ModelForm):
    # class Meta:
        # model = Colour
        # fields = ['colour']

# colour_formset = inlineformset_factory(ObjectRegister, Colour, form=ColourEntry, extra=2)

# class MaterialTypeEntry(ModelForm):
    # class Meta:
        # model = MaterialType
        # fields = ['material_type', 'material']

# materialtype_formset = inlineformset_factory(ObjectRegister, MaterialType, form=MaterialTypeEntry, extra=2)

# class TechnicalAttributeEntry(ModelForm):
    # class Meta:
        # model = TechnicalAttribute
        # fields = ['attribute_type', 'attribute_value']

# technicalattribute_formset = inlineformset_factory(ObjectRegister, TechnicalAttribute, form=TechnicalAttributeEntry, extra=1)


###########################################################
# The following information shall be added in separate forms,
# because it is unlikely this will be available when filling
# a field survey:
#
# - ObjectName (i.e. alternate object names)
# - OtherNumber
# - Production
# - Description > Specimen, Artifact, or WorkInstance
# - Inscription (certain fields only)
# - Rights
# - AssociatedObject
# - Ownership
# - Hierarchy (figure out a way to automatically
#   create this relationship through a button to add child
#   objects.
# - RelatedObject
# - TextRef
