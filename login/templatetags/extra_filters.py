from django import template
import re

register = template.Library()

#########################
####INICIO DE FILTROS####
#########################
@register.filter(name='ifusergroup')
def ifusergroup(value, arg):
    return value.groups.filter(name = arg)

@register.filter(name='contains')
def contains(value, arg):
    return containsValue(value, arg)

@register.filter(name='containsNegative')
def containsNegative(value, arg):
    arg = "-%s" % arg
    return containsValue(value, arg)

@register.filter(name='containsValue')
def containsValue(value, arg):
    if value == None:
        value = ""
    return arg in value

@register.filter(name='replaceDecimal')
def replaceDecimal(value, arg):
    if value == None or value == '':
        value = "null"
    return str(value).replace(",", arg)

@register.filter(name='replaceNone')
def replaceNone(value, arg):
    if value == None or value == '':
        return 0
    return value

@register.filter(name='replaceTextNone')
def replaceTextNone(value, arg):
    if value == None or value == '':
        return ''
    return value

@register.filter(name='cutUrlFilter')
def cutUrlFilter(value, arg):
    return urlFilter(value, arg, ".")

@register.filter(name='cancelUrlFilter')
def cancelUrlFilter(value, arg):
    return urlFilter(value, arg, "")

def urlFilter(value, arg, punto):
    if value == None:
        value = ""
    value = re.sub(r'^\.?-?(' + arg + ')\.?', '', value)
    value = re.sub(r'\.?-?(' + arg + ')', '', value)
    if value != "":
        value = "%s%s" % (punto, value)
    return value

@register.filter(name='filterKeyValue')
def filterKeyValue(dict, key):
    return dict.get(key, "")

@register.filter(name='addCss')
def addCss(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='addHidden')
def addCss(value):
    return value.as_widget(attrs={'type': 'hidden'})

@register.filter(name='addNumber')
def addCss(value):
    return value.as_widget(attrs={'type': 'number','min':'0', 'max':'100','step':'1','class':'text-field form-control'})

@register.filter(name='labelAddCss')
def labelAddCss(value, arg):
    return value.label_tag(attrs={'class': arg})

@register.filter(name='getField')
def getField(value, arg):
    return getattr(value, arg)

@register.filter(name='getTitleField')
def getTitleField(value, arg):
    arg = arg.split("__")
    return value.model._meta.get_field(arg[0]).verbose_name.title()

@register.filter(name='getTitleFieldDetail')
def getTitleFieldDetail(value, arg):
    return getattr(value, '_meta').get_field(arg).verbose_name.title()