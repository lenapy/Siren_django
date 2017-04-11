from django import forms


class SearchForm(forms.Form):
    video_title = forms.CharField(max_length=50, initial='')

    def clean(self):
        cleaned_data = super().clean()
        video_title = cleaned_data['video_title']
        return cleaned_data
