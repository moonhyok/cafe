from django.forms import ModelForm, CharField, Form, ChoiceField, DateField, Textarea, TextInput,PasswordInput, Select
from opinion_core.models import UserDemographics
from opinion.settings import CATEGORIES

"""
class ContactForm(forms.Form):
    message = forms.CharField()
"""

class UserDemographicsForm(ModelForm):
	def clean_location(self):
		if 'location' in self.cleaned_data and self.cleaned_data['location'] == 'null':
			self.cleaned_data['location'] = ''
		return self.cleaned_data['location']
	class Meta:
		model = UserDemographics

class ConfigurationForm(Form):
    def __init__(self):
        super(ConfigurationForm, self).__init__()
        
    def create_form(self, configurables):
        config_list = []
        for category in CATEGORIES:
            for item in category[1]:
                config_list.append(item.replace(' ','_'))
        for config in config_list:
            if 'choices' in configurables[config]:
                self.fields[config] = ChoiceField(help_text=configurables[config]['name'],choices=configurables[config]['choices'], initial=configurables[config]['default'], widget=Select(attrs={'style':'width:355px'}))
            elif 'display' in configurables[config] and configurables[config]['display'] == 'TEXTAREA':
                self.fields[config] = CharField(help_text=configurables[config]['name'],initial=configurables[config]['default'], widget=Textarea(attrs={'style':'width:350px'}))
            else:
                self.fields[config] = CharField(help_text=configurables[config]['name'],initial=configurables[config]['default'], widget=TextInput(attrs={'style':'width:350px'}))
        return self
		
class InstallForm(Form):
	def __init__(self):
		super(InstallForm, self).__init__()
		
	def create_form(self, data):
		for d in data:
			if d['type'] == 'question':
				self.fields['Discussion Question'] = CharField(initial=d['text'], widget=Textarea(attrs={'style':'width:350px;height:75px'}))
			elif d['type'] == 'squestion':
				self.fields['Discussion Question Spanish'] = CharField(initial=d['text'], widget=Textarea(attrs={'style':'width:350px;height:75px'}))
			else:
				self.fields[str(d['id'])] = CharField(initial=d['text'], widget=Textarea(attrs={'style':'width:350px;height:75px'}))
				self.fields['s'+str(d['id'])] = CharField(initial=d['spanish'], widget=Textarea(attrs={'style':'width:350px;height:75px'}))
		return self
		
class ProofreadForm(Form):
	def __init__(self):
		super(ProofreadForm, self).__init__()
		
	def create_form(self, data):
		for d in data:
			self.fields[d['type']] = CharField(initial=d['text'], widget=Textarea(attrs={'style':'width:600px;height:300px'}))
		return self
		
class AdminPanelLoginForm(Form):
	def __init__(self):
		super(AdminPanelLoginForm, self).__init__()

	def create_form(self, data):
		self.fields['Username'] = CharField(widget=TextInput(attrs={'style':'width:150px'}))
		self.fields['Password'] = CharField(widget=PasswordInput(attrs={'style':'width:150px'}))
		return self

class SeedForm(Form):
    def __init__(self):
        super(SeedForm, self).__init__()
        
    def create_form(self,initial):
        self.fields['Idea 1'] = CharField(initial=initial[0],widget=Textarea(attrs={'style':'width:350px; height:100px;'}))
        self.fields['Idea 2'] = CharField(initial=initial[1],widget=Textarea(attrs={'style':'width:350px; height:100px;'}))
        self.fields['Idea 3'] = CharField(initial=initial[2],widget=Textarea(attrs={'style':'width:350px; height:100px;'}))
        self.fields['Idea 4'] = CharField(initial=initial[3],widget=Textarea(attrs={'style':'width:350px; height:100px;'}))
        return self
        
        