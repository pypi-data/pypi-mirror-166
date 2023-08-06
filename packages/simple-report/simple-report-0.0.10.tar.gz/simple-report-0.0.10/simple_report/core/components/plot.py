import io
from simple_report.core.components.base import BaseElement
from matplotlib.figure import Axes, Figure
from seaborn.axisgrid import Grid
from plotly.graph_objs._figure import Figure as PFigure
import base64

from plotly.io import to_html

from simple_report.utils.utils import plot_360_n0sc0pe


class Image(BaseElement):
    def __init__(
        self,
        figure,
        image_format, #: ImageType,
        # alt: str,
        # caption = None, #: Optional[str] 
        **kwargs,
    ):
        # if figure is None:
        #     raise ValueError(f"Image may not be None (alt={alt}, caption={caption})")

        # super().__init__(
        #     "image",
        #     {
        #         "image": image,
        #         "image_format": image_format,
        #         "alt": alt,
        #         "caption": caption,
        #     },
        #     **kwargs,
        # )
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return "Image"

    def render(self): # -> Any:
        raise NotImplementedError()


class Plot(BaseElement):
    def __init__(self, figure, page=None, **kwargs):
        super().__init__(**kwargs)
        self.figure = figure
        self.page = page

    # @singledispatchmethod
    def to_html(self):
        if Axes in type(self.figure).__mro__:
            print('Adding Axes (axes) as plot')
            return self.add_matplotlib_axes(self.figure, self.page)
        elif Grid in type(self.figure).__mro__:
            print('Adding Grid (axes) as plot')
            return self.add_matplotlib_axes(self.figure, self.page)
        elif Figure in type(self.figure).__mro__:
            print('Adding Figure (figure) as plot')
            return self.add_matplotlib_figure(self.figure, self.page)
        elif PFigure in type(self.figure).__mro__:
            return self.add_plotly_figure(self.figure, self.page)
        # elif Chart in type(self.figure).__mro__:
        #     return self.add_altair_figure(self.figure, self.page)
        else:
            raise NotImplementedError(f"Plot type '{type(self.figure).__name__}' not supported")

    # @to_html.register
    # def add_altair_figure(self, figure: Chart, page=None):
    #     figure_id = f"a{uuid.uuid4().hex[:10].upper()}"

    #     return """
    #         <div id="<<figure_id>>"></div>
    #         <script type="text/javascript">
    #             vegaEmbed("#<<figure_id>>", <<figure>>).catch(console.error);
    #         </script>
    #         """ \
    #         .replace('<<figure_id>>', figure_id) \
    #         .replace('<<figure>>', figure.to_json())

    def add_matplotlib_figure(self, figure: Figure, image_format='png', page=None):
        # tmpfile = io.StringIO()
        image_format = 'png'
        tmpfile = io.BytesIO()
        figure_type = type(figure).__name__
        if figure_type == 'FacetGrid':
            figure.savefig(tmpfile, format='png')
        elif figure_type == 'AxesSubplot':
            figure.figure.savefig(tmpfile, format='png')
            result_string = plot_360_n0sc0pe(figure.figure, image_format)
        elif figure_type == 'Figure':
            figure.savefig(tmpfile, format='png')
            result_string = plot_360_n0sc0pe(figure.figure, image_format)

        encoded_figure = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return f"""<img class="img-fluid text-center" src=\'{result_string}\'>"""
        # return f"""<img class="img-fluid" src=\'data:image/png;base64,{encoded_figure}\'>"""

    def add_matplotlib_axes(self, figure: Axes, page=None):
        image_format = 'png'
        figure_type = type(figure).__name__
        if figure_type == 'FacetGrid':
            print(".... Adding FacetGrid")
            result_string = plot_360_n0sc0pe(figure, image_format)
        elif figure_type == 'AxesSubplot':
            print(".... Adding AxesSubplot")
            result_string = plot_360_n0sc0pe(figure.figure, image_format)

        if image_format == 'svg':
            return f"""<div class="text-center">
                {result_string.replace('<svg', '<svg class="img-fluid text-center"')}
            </div>"""
            # return result_string.replace('<svg', '<svg class="img-fluid text-center"')
        else:
            # encoded_figure = base64.b64encode(result_string).decode('utf-8')
            return f"""<img class="img-fluid text-center" src=\'{result_string}\'>"""
            # return f"""<img class="img-fluid text-center" src=\'data:image/png;base64,{result_string}\'>"""

        # return f"""<div class="img-fluid text-center">
        #         {result_string}
        #     </div>"""

        # tmpfile = BytesIO()
        # figure_type = type(figure).__name__
        # if figure_type == 'FacetGrid':
        #     figure.savefig(tmpfile, format='png')
        # elif figure_type == 'AxesSubplot':
        #     figure.figure.savefig(tmpfile, format='png')
        # encoded_figure = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        # self.body[page] += f"""<img src=\'data:image/png;base64,{encoded_figure}\'>"""


# {% if image_format.value == 'svg' and not image.endswith('.svg') %}
#     {{- image.replace('svg ','svg class="img-responsive center-img"') }}
# {% else %}
#     <img class="img-responsive center-img" src="{{ image }}" alt="{{ alt }}">
# {% endif %}

    # # @to_html.register
    # def add_matplotlib_figure(self, figure: Figure, page=None):
    #     # tmpfile = BytesIO()
    #     tmpfile = io.StringIO()
    #     figure_type = type(figure).__name__
    #     if figure_type == 'FacetGrid':
    #         figure.savefig(tmpfile, format='svg')
    #     elif figure_type == 'AxesSubplot':
    #         figure.figure.savefig(tmpfile, format='svg')
    #     encoded_figure = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    #     return f"""<img src=\'data:image/png;base64,{encoded_figure}\'>"""


    # @to_html.register
    def add_plotly_figure(self, figure: PFigure, page=None):
        encoded_figure = to_html(figure, include_plotlyjs=False, full_html=False)
        # return encoded_figure
        return f"""<div class="container">{encoded_figure}</div>"""
