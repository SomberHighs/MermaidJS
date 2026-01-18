from typing import Any, Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound as JinjaTemplateNotFound
from src.core.interfaces import TemplateRenderer
from src.core.exceptions import TemplateNotFoundError

class JinjaRenderer(TemplateRenderer):
    def __init__(self, template_dir: str):
        # autoescape=True is critical for security (prevents XSS if rendering HTML)
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render(self, template_id: str, context: Dict[str, Any]) -> str:
        try:
            # We assume template_id matches the filename, e.g., "welcome.html"
            template = self.env.get_template(template_id)
            return template.render(**context)
        except JinjaTemplateNotFound:
            raise TemplateNotFoundError(f"Template '{template_id}' not found in {self.env.loader.searchpath}")
