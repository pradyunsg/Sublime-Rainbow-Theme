"""The Main Command that runs the show.
"""

from . import core
from .theme_manager import ThemeManager
from .context_manager import ContextManager
from .preferences_manager import PreferencesManager


class RainbowThemeAdapter(object):
    """Run the entire re-generation procedure for the theme
    """

    def __init__(self):
        super().__init__()
        self.ctx_man = ContextManager()
        self.th_man = ThemeManager()
        self.prefs = PreferencesManager()

    def run(self):
        # Extract colours from the colour schemes
        scheme_colours = self.prefs.get_current_scheme_colours()

        # Detect what the type of theme is active
        variant, theme_name = self.prefs.get_theme_variant_and_name()

        if variant is None:
            core.logger.debug("Skipping generation due to inactive theme")
            return False

        # Generate other colours for the theme from what we know
        context = self.ctx_man.generate_theme_context(
            scheme_colours, variant, theme_name
        )

        # Generate the theme and supporting files
        rendered = self.th_man.get_rendered_theme_parts(
            context, scheme_colours, variant
        )

        # Write the generated theme in the Package
        self.th_man.write_theme_parts(context, rendered)

        return True

    def clear_cache(self):
        self.th_man.cache.clear()
