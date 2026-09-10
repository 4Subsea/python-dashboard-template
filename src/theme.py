"""4Subsea theme: registers the Plotly template from the design system.

The actual tokens, palettes and the Plotly template itself live in the
`4subsea-design-system` package (theme_4insight.py there, backed by
colors_and_type.css + dataviz.css) - see requirements.txt for how it's
installed. This file's only job is to register that template as Plotly's
default on import, and to publish COLORS so tests can assert the
registration held.

Importing this module registers the template as Plotly's default, so any
figure built afterwards picks it up without asking.
"""

import plotly.io as pio
from foursubsea_design_system.theme_4insight import plotly_template

TEMPLATE_NAME = "4subsea"


def register_theme(set_as_default: bool = True) -> None:
    """Register the design system's Plotly template."""
    pio.templates[TEMPLATE_NAME] = plotly_template()
    if set_as_default:
        pio.templates.default = TEMPLATE_NAME


# Register theme on import so that themes are available after import without needing to call register_theme()
register_theme()

COLORS = tuple(pio.templates[TEMPLATE_NAME].layout.colorway)
"""The registered template's colorway, read back from the template itself so
it can't drift from what got registered."""
