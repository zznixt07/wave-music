from django import forms
from user.models import Playlist

class ViewPlaylistForm(forms.ModelForm):

    class Meta:
        model = Playlist
        fields = ['name']
        widgets = {}