from django import template, forms
from django.utils.html import format_html
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.template.loader import get_template
import markdown
from ..models import Post
# from ..models import FeaturedContent


register = template.Library()


@register.filter(name="article")
def article_format(content, class_string=""):
    # if class_string:
    #     content = content.replace("\t", f'<p class={class_string}>')
    # else:
    #     content = content.replace('\t', '<p>')
    class_string += " indented"
    content = content.replace('\t', f'<p class="{class_string}">')
    content = content.replace('\n', '</p>')
    if not content.endswith('</p>'):
        content += "</p>"

    return format_html(content)



@register.filter
def bulma_label(field, classes=""):
    label = field.label
    id_for_label = field.id_for_label or ""
    if is_file(field):
        classlist = "file-label " + classes
        html = f'''
            <span class="file-cta">
                <span class="file-icon">
                    <i class="fa-regular fa-upload"></i>
                </span>
                <span class="{classes}">
                    {label}
                </span>
            </span>
            <span id="fileNames" class="file-name">
                Choose a file...
            </span>
        '''
        return format_html(html)
    else:
        classlist = "label " + classes
        return format_html(
            f'<label for="{id_for_label}" class="{classlist}">{label}</label>'
        )
    

@register.filter
def bulma_input(field, classes=""):
    existing = field.field.widget.attrs.get("class", '')
    classes = 'input '+ existing + classes
    return field.as_widget(attrs={"class": classes})


@register.filter
def bulma_text(field, classes=""):
    existing = field.field.widget.attrs.get('class', '')
    classes = 'textarea '+ existing + classes
    return field.as_widget(attrs={
        'class': classes,
        'rows': '10'
    })


@register.filter
def bulma_select(field, classes=''):
    existing = field.field.widget.attrs.get('class', '')
    classes = 'select ' + existing + classes
    return field.as_widget(attrs={'class': classes})


@register.filter
def bulma_checkbox(field, classes=''):
    existing = field.field.widget.attrs.get('class', '')
    classes = 'checkbox ' + existing + classes 

    return field.as_widget(attrs={'class': classes})


@register.filter
def bulma_file(field, classes=''):
    existing = field.field.widget.attrs.get('class', '')
    classes = 'file-input ' + existing + classes 
    return field.as_widget(attrs={'class': classes})


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def is_textarea(field):
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)



@register.filter
def is_select(field):
    return isinstance(field.field.widget, forms.widgets.Select)


@register.filter
def bulma_form(form_obj, label_class=""):
    return render(form_obj, label_class)



def render(obj, classes):
    if isinstance(obj, forms.BoundField):
        template = get_template('forms/_field.html')
        context = {
            'field': obj,
            'form': obj.form,
            'classes': classes
        }
    else:
        has_management = getattr(obj, 'management_form', None)
        if has_management:
            template = get_template('forms/_formset.html')
            context = {
                'formset': obj,
                'classes': classes
            }

        else:
            template = get_template('forms/_form.html')
            context = {
                'form': obj,
                'classes': classes
            }
    return template.render(context)



@register.simple_tag 
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {
        'latest_posts': latest_posts
    }


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]