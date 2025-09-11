from django import forms


class ReminderForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label="Reminder text")
