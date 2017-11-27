from django import forms

from .models import UserInfo

class NewVMForm(forms.Form):
    VirtualMachineName = forms.CharField(label="Name")
    CPUCores = forms.IntegerField(label="CPU Cores")
    RAMAmount = forms.IntegerField(label="Amount of RAM")
    DiskSize = forms.IntegerField(label="Disk Size")

class UpdateUserForm(forms.Form):
    class Meta(forms.ModelForm):
        model = UserInfo
        fields = ["name", "surname", "birthdate", "iban", "adres", "postalcode", "phonenumber", "company", "country"]