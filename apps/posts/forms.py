from django import forms

from apps.posts.models import Tag


class PostLikeForm(forms.Form):
    post_id = forms.IntegerField()


class PostCreateForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )
    videos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
