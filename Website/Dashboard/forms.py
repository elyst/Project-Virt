from django import forms

CPU_Choices = [tuple([x,x]) for x in range(1,5)]
RAM_Choices = [
    (1000000, "1 GB"),
    (2000000, '2 GB'),
    (4000000, '4 GB'),
    (8000000, '8 GB'),
    ]

Disk_Choices = [
    (10, "10 GB"),
    (20, '20 GB'),
    (40, '40 GB'),
    (80, '80 GB'),
    ]   

class NewVMForm(forms.Form):
    VirtualMachineName = forms.CharField(label="Name")
    CPUCores = forms.IntegerField(label="CPU Cores", widget=forms.Select(choices=CPU_Choices))
    RAMAmount = forms.IntegerField(label="Amount of RAM", widget=forms.Select(choices=RAM_Choices))
    DiskSize = forms.IntegerField(label="Disk Size", widget=forms.Select(choices=Disk_Choices))
