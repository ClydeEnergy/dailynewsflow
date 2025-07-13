import re
from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def truncate_html(value, length=100):
    """
    Truncate HTML content while preserving basic formatting.
    Removes HTML tags but keeps text content, then truncates.
    """
    if not value:
        return ""
    
    # Strip HTML tags but preserve the text content
    text_content = strip_tags(value)
    
    # Truncate the text
    if len(text_content) <= length:
        return mark_safe(value)
    
    truncated_text = text_content[:length].rsplit(' ', 1)[0]
    if truncated_text != text_content[:length]:
        truncated_text += '...'
    else:
        truncated_text = text_content[:length] + '...'
    
    return truncated_text

@register.filter
def truncate_html_words(value, word_count=20):
    """
    Truncate HTML content by word count while preserving some formatting.
    """
    if not value:
        return ""
    
    # Strip HTML tags but preserve text
    text_content = strip_tags(value)
    words = text_content.split()
    
    if len(words) <= word_count:
        return mark_safe(value)
    
    truncated_words = words[:word_count]
    truncated_text = ' '.join(truncated_words) + '...'
    
    return truncated_text

@register.filter
def smart_truncate_html(value, length=100):
    """
    Smart truncate that preserves basic HTML formatting like <strong>, <em>, <ul>, <li>
    while truncating content to specified character length.
    """
    if not value:
        return ""
    
    # Allow basic formatting tags
    allowed_tags = ['strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li', 'p']
    
    # Remove disallowed HTML tags but keep allowed ones
    clean_html = re.sub(r'<(?!/?(?:' + '|'.join(allowed_tags) + r')\b)[^>]*>', '', value)
    
    # Get text content for length calculation
    text_content = strip_tags(clean_html)
    
    if len(text_content) <= length:
        return mark_safe(clean_html)
    
    # Truncate while trying to preserve word boundaries
    truncated_text = text_content[:length].rsplit(' ', 1)[0]
    if truncated_text != text_content[:length]:
        truncated_text += '...'
    else:
        truncated_text = text_content[:length] + '...'
    
    # Try to preserve basic formatting for the truncated portion
    # This is a simple approach - for more complex needs, you'd want a proper HTML parser
    if '<' in clean_html and len(clean_html) > len(text_content):
        # Has HTML formatting, try to preserve it
        words_to_keep = len(truncated_text.rstrip('...').split())
        html_words = re.findall(r'<[^>]+>|\S+', clean_html)
        
        result_parts = []
        word_count = 0
        
        for part in html_words:
            if part.startswith('<'):
                result_parts.append(part)
            else:
                if word_count < words_to_keep:
                    result_parts.append(part)
                    word_count += 1
                else:
                    break
        
        result = ' '.join(result_parts)
        if word_count >= words_to_keep:
            result += '...'
        
        return mark_safe(result)
    
    return truncated_text

@register.filter
def strip_html_tags(value):
    """
    Strip all HTML tags from the content.
    """
    if not value:
        return ""
    return strip_tags(value)
