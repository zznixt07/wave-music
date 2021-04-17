from django import forms
from .models import Playlist

class ViewPlaylistForm(forms.ModelForm):

    class Meta:
        model = Playlist
        fields = ['name']
        widgets = {}