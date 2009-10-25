from django.db.models.signals import pre_save
from trustedhtml import pretty
from trustedhtml.signals import rule_done
from trustedhtml.classes import Uri
from modelurl.utils import ReplaceByView
from pages.models import Content
from django.template import defaultfilters
from django.utils.safestring import mark_safe

def content_save(sender, instance, **kwargs):
    if instance.type == 'main_content':
        instance.body = pretty.validate(instance.body)

pre_save.connect(content_save, sender=Content)

def url_done(sender, rule, value, source, **kwargs):
    return ReplaceByView(silent=True).url(value)

rule_done.connect(url_done, sender=Uri)

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import re
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^.\w\s-]', '', value).strip().lower())
    return mark_safe(re.sub('[-\s]+', '-', value))
slugify.is_safe = True
slugify = defaultfilters.stringfilter(slugify)
defaultfilters.slugify = slugify
