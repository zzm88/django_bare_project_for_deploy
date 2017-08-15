# coding:utf-8
from django import forms


class AddForm(forms.Form):
    query = forms.CharField(label='关键词',max_length=10)
    start_price = forms.IntegerField(label='价格从',required=False)
    end_price = forms.IntegerField(label='到',required=False)