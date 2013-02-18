# -*- encoding:utf-8 -*-

from jinja2 import Template
template = Template("hello{{name}}!")
template.render(name="けいた")

