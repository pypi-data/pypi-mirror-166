import uuid
from simple_report.core.components.base import BaseElement
from simple_report.structure.html.templates import jinja2_env


class Table(object):

    def __init__(self, dataframe, title=None, use_striped_style=True, use_jquery=False, caption=None):
        self.dataframe = dataframe
        self.title = title
        self.use_striped_style = use_striped_style
        self.use_jquery = use_jquery
        self.caption = caption

# if self.use_jquery:
#     foo += """
#         <script
#             type="text/javascript"
#             charset="utf8"
#             src="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/jquery.dataTables.min.js">
#         </script>
        
#         <script>
#             $(function() {
#             $("#<<table_id>>").dataTable();
#             });
#         </script>
#         """ \
#         .replace('<<table_id>>', table_id)


    def to_html(self):
        table_id = uuid.uuid4().hex[:10].upper()
        table = self.dataframe.to_html(
            table_id=table_id,
            classes=['table', 'table-striped'] if self.use_striped_style else ['table'],
            border=0,
            )

        content = {
            'title': self.title,
            'caption': self.caption,
            'table': table,
        }
        template = jinja2_env.get_template('table.html')
        rendered_template = template.render(content)
        return rendered_template


# https://github.com/pandas-dev/pandas/blob/734db4f1fde2566a02b3c7ff661a479b0a71633c/pandas/io/formats/html.py
# _classes.extend(self.classes)

        # self.write(
        #     f'<table{border_attr} class="{" ".join(_classes)}"{id_section}>',
        #     indent,
        # )
