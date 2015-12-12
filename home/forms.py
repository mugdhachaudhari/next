
#files.py
import re
from django import forms
from django.contrib.auth.models import User
from login.models import Registration
from django.utils.translation import ugettext_lazy as _


#class accpetfrndForm(forms.Form):
#	widgets = {'review':form.HiddenInput()}
#Choices = (
#			('1','a friend'),
#			('2','a neighbour'),
#			('3','block'),
#			('4','neighbourhood'),
#			('5','all friends'),
#	)
 
class MessageForm(forms.Form):
	choice = forms.ChoiceField(choices = [("f","a friend"),
										("n","a neighbour"),
										("b","block"),
										("ne","neighbourhood"),
										("a","all friends")],
									widget=forms.Select(), required = True)
	#username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
	#title = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=50, render_value=True)), label=_("Title"))
	#textbody = forms.CharField(widget=forms.Textarea(attrs=dict(required=True, max_length=500, render_value=True)), label=_("Textbody"))
	
	
class NewmessageForm(forms.Form):
	username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
	title = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=50, render_value=True)), label=_("Title"))
	textbody = forms.CharField(widget=forms.Textarea(attrs=dict(required=True, max_length=500, render_value=True)), label=_("Textbody"))
	
	
class NewmessagesForm(forms.Form):
	title = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=50, render_value=True)), label=_("Title"))
	textbody = forms.CharField(widget=forms.Textarea(attrs=dict(required=True, max_length=500, render_value=True)), label=_("Textbody"))
	
	
	def save(self):
		u = messages.objects.get(title = self.cleaned_data['title'])
		u.textbody = self.clean_data['textbody']
		u.save()
		return u
	