"""
Forms and validation code for user registration.

"""


from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from registration.models import RegistrationProfile

import opinion.settings

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = { 'class': 'required' }


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should either preserve the base ``save()`` or implement
    a ``save()`` which accepts the ``profile_callback`` keyword
    argument and passes it through to
    ``RegistrationProfile.objects.create_inactive_user()``.
    
    """
    username = forms.EmailField(min_length=opinion.settings.MIN_USERNAME_LENGTH,
                                max_length=75,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u'username'),
								required=opinion.settings.REGISTRATION_FIELD_TABLE['username']['required'])

    email = forms.EmailField(max_length=75,
                             widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'email address'),
                             required=opinion.settings.REGISTRATION_FIELD_TABLE['email']['required'])
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'password (again)'))

    # Changed first name to support multiple words
    first_name = forms.RegexField(regex=r'^[\w \t]+$',
                                max_length=30, widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u'first name'),
                                required=opinion.settings.REGISTRATION_FIELD_TABLE['first_name']['required'])
    
    url = forms.URLField(max_length=1024, required=opinion.settings.REGISTRATION_FIELD_TABLE['url']['required'])

    question = forms.CharField(max_length=512, label=(u'question'), required=opinion.settings.REGISTRATION_FIELD_TABLE['question']['required']) 

    answer = forms.CharField(max_length=512, label=(u'answer'), required=opinion.settings.REGISTRATION_FIELD_TABLE['answer']['required']) 

    zipcode = forms.CharField(max_length=5, label=(u'zipcode'), required=True)
	
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'Sorry! That username is already taken, please choose another.'))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
		Verify there is a matching question and answer

        """
        from opinion.opinion_core.models import *

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))

        if 'question' in self.cleaned_data:
			if self.cleaned_data['question'] != "":	
				if 'answer' not in self.cleaned_data:
					raise forms.ValidationError(_(u'You must type in an answer'))
				if self.cleaned_data['answer'] == "":
					raise forms.ValidationError(_(u'You must type in an answer'))

        if 'answer' in self.cleaned_data:
			if self.cleaned_data['answer'] != "":
				if 'question' not in self.cleaned_data:
					raise forms.ValidationError(_(u'You must type in a question'))
				if self.cleaned_data['question'] == "":
					raise forms.ValidationError(_(u'You must type in a question'))

        if 'zipcode' in self.cleaned_data:
            if not len(self.cleaned_data['zipcode']) == 5:
                raise forms.ValidationError(_(u'Zipcode must be 5 digits'))

        return self.cleaned_data
    
    def save(self, profile_callback=None):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User``.
        
        This is essentially a light wrapper around
        ``RegistrationProfile.objects.create_inactive_user()``,
        feeding it the form data and a profile callback (see the
        documentation on ``create_inactive_user()`` for details) if
        supplied.
        
        """
        # create_inactive_user changed to create_active_user for Opinion Space
        new_user = RegistrationProfile.objects.create_active_user(username=self.cleaned_data['username'],
                                                                  password=self.cleaned_data['password1'],
                                                                  email=self.cleaned_data['email'],
                                                                  first_name=self.cleaned_data['first_name'],
                                                                  profile_callback=profile_callback)
        return new_user


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    
    """
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={ 'required': u"You must agree to the terms to register" })


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    
    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if not (self.cleaned_data['email'] == ""):
			if User.objects.filter(email__iexact=self.cleaned_data['email']):
				raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']


class RegistrationFormNoFreeEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.
    
    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.
    
    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com']
    
    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.
        
        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_(u'Registration using free email addresses is prohibited. Please supply a different email address.'))
        return self.cleaned_data['email']
