from django import forms
from .models import Operation, Shipping


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = "__all__"

        # def __int__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields[]

