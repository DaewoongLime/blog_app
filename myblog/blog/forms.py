from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class WritePostForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, widget=forms.Textarea(attrs={'rows':1}))
    content = forms.CharField(label="Content", max_length=5000, widget=forms.Textarea(attrs={'rows':15}))

class LeaveCommentForm(forms.Form):
    content = forms.CharField(label="Comment")

    def clean_content(self):
        data = self.cleaned_data['content']

        if len(data) > 200:
            raise ValidationError(('Your comment is too long'))

        return data