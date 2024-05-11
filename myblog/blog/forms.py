from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class WritePostForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, help_text="Title")
    content = forms.CharField(label="Content", max_length=5000, help_text="Write Something...")

class LeaveCommentForm(forms.Form):
    content = forms.CharField(help_text="Leave a comment...")

    def clean_content(self):
        data = self.cleaned_data['content']

        if len(data) > 200:
            raise ValidationError(_('Your comment is too long'))

        return data