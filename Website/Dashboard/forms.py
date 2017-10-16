from django import forms

class NewVMForm(forms.Form):
    VirtualMachineName = forms.CharField(label="Name")
    CPUCores = forms.IntegerField(label="CPU Cores")
    RAMAmount = forms.IntegerField(label="Amount of RAM")
    DiskSize = forms.IntegerField(label="Disk Size")