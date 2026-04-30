from django import forms


class CKEditorWidget(forms.Textarea):
    class Media:
        js = (
            "https://cdn.ckeditor.com/ckeditor5/41.4.2/classic/ckeditor.js",
            "js/admin/ckeditor-init.js",
        )

    def __init__(self, attrs=None):
        default_attrs = {"class": "ckeditor-textarea"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
