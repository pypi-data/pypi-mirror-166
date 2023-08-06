from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from wagtail_honeypot.models import HoneypotMixin

try:
    from wagtail.fields import RichTextField
except ImportError:
    from wagtail.core.fields import RichTextField


try:
    from wagtail.models import Page
except ImportError:
    from wagtail.core.models import Page


try:
    from wagtail.admin.panels import (
        FieldPanel,
        FieldRowPanel,
        InlinePanel,
        MultiFieldPanel,
        ObjectList,
        TabbedInterface,
    )
except ImportError:
    from wagtail.admin.edit_handlers import (
        FieldPanel,
        FieldRowPanel,
        InlinePanel,
        MultiFieldPanel,
        ObjectList,
        TabbedInterface,
    )


class HomePage(Page):
    template = "home_page.html"


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", related_name="form_fields")


class FormPage(HoneypotMixin):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro", classname="full"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text", classname="full"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(HoneypotMixin.honeypot_panels, heading="Honeypot"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )
