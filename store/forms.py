from django import forms
from .models import ReviewRating

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs['placeholder'] = 'Enter Subject'
        self.fields['review'].widget.attrs['placeholder'] = 'Enter Review'
        self.fields['rating'].widget.attrs['placeholder'] = 'Enter Rating'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
