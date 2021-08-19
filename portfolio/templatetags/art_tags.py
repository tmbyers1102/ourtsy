from django.template import Context, Template
from django import template

# register = template.Library()


# class RenderCustom(template.Node):

#     @classmethod
#     def handle_token(cls, parser, token):
#         tokens = token.split_contents()

#         field = tokens[1]

#         return cls(parser.compile_filter(field))

#     def __init__(self, field):
#         self.field = field

#     def render(self, context):
#         render_field = self.field.resolve(context)

#         render_template = Template(render_field)

#         rendered = render_template.render(Context())

#         return rendered


# @register.tag
# def render_this(parser, token):
#     return RenderCustom.handle_token(parser, token)