#files.py
import re
from django import forms
from profileapp.models import UserProfile
from django.contrib.auth.models import User
#from login.models import Registration
from django.utils.translation import ugettext_lazy as _
from django.db.models.lookups import IsNull
 
class ProfileForm(forms.ModelForm):

#     username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, readonly = True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
#     email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))

    

    class Meta:
        model = UserProfile
        fields = ('firstname', 'lastname', 'apt', 'street', 'city', 'state', 'zip', 'profle', 'photopath')

    
#     self.fields.keyOrder = ['username', 'email', 'firstname', 'lastname', 'apt', 'street', 'city', 'state','zip', 'profle']

    def clean_street(self):
        if 'street' in self.cleaned_data:
            if self.cleaned_data['street'] == "Street":
                raise forms.ValidationError(_("Please enter valid street"))
        return self.cleaned_data['street']
    
    def clean_city(self):
        if 'city' in self.cleaned_data:
            if self.cleaned_data['city'] == "City":
                raise forms.ValidationError(_("Please enter valid city"))
        return self.cleaned_data['city']
    
    def clean_state(self):
        if 'state' in self.cleaned_data:
            if self.cleaned_data['state'] == "State":
                raise forms.ValidationError(_("Please enter valid state"))
        return self.cleaned_data['state']
    
    def clean_zip(self):
        if 'zip' in self.cleaned_data:
            if self.cleaned_data['zip'] == "Zip" or len(self.cleaned_data['zip']) != 5:
                raise forms.ValidationError(_("Please enter valid zip"))
        return self.cleaned_data['zip']

    def clean_photopath(self):
        photopath = self.cleaned_data.get('photopath', False)
        if photopath:
            fileType = photopath.content_type
            if fileType in ['image/jpeg', 'image/png']: #png and jpeg
                return photopath
        raise forms.ValidationError('FileType not supported: only upload jpegs and pngs.')

class UserForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.HiddenInput(attrs=dict(required=True, readOnly = True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))

#     class Meta:
#         model = User
#         fields = ('username','email')

    def save(self):
        u = User.objects.get(username=self.cleaned_data['username'])
        u.email = self.cleaned_data['email']
        u.save()
        return u

#     self.fields.keyOrder = ['username', 'email', 'firstname', 'lastname', 'apt', 'street', 'city', 'state','zip', 'profle']

#     def clean_street(self):
#         if 'street' in self.cleaned_data:
#             if self.cleaned_data['street'] == "Street":
#                 raise forms.ValidationError(_("Please enter valid street"))
#         return self.cleaned_data['street']

# class LoginForm(forms.Form):
#  
#     #username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
#     email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
#     password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
