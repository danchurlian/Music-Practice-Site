import verovio
import os

from jinja2 import Environment, Template, PackageLoader

# Setup Jinja environment
jinja_env: Environment = Environment(
    loader=PackageLoader("app")
)

tk = verovio.toolkit()
tk.setResourcePath(os.path.join(os.path.dirname(verovio.__file__), "data"))
tk.setOptions({
    "inputFrom": "xml",
    "svgViewBox": True,
    "scale": 100,

    "adjustPageHeight": True,
    "adjustPageWidth": True,
    "pageMarginTop": 0,
    "pageMarginBottom": 0,
})

type musicxml_str = str


def render_single_staff_template(additional_attributes_xml="", notes_xml="") -> str:
    """
    This function generates a MusicXML string using the single_staff_template
    template.
    The attributes for the resulting MusicXML have 1 division by default
    and appends additiona_attributes_xml to the attributes section of the XML.

    It inserts the notes_xml string into the template and returns
    the end result.
    """

    attributes_xml: str = "<divisions>1</divisions>"

    template: Template = jinja_env.get_template("single-staff-template.xml")
    total_xml: musicxml_str = template.render(
        attributes = attributes_xml + additional_attributes_xml, 
        notes = notes_xml)

    return total_xml


def render_to_svg(xml: musicxml_str) -> str:
    """
    This function returns a string representing an SVG HTML tag. 
    Params
    musixml -> a string in MusicXML format.
    """
    svg_result: str = ""
    tk.loadData(xml)
    svg_result = tk.renderToSVG(1)

    return svg_result