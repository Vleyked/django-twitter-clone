from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 1,
                    "style": "resize:none; overflow:hidden;",
                    "oninput": 'this.style.height = "";this.style.height = this.scrollHeight + "px"',
                }
            ),
        }
