from handlers.abstract import AbstractHandler
from lxml.html import HtmlElement

GOVUK = "https://www.gov.uk"

class GovUKHandler(AbstractHandler):
    """
    handles urls beginning: https://www.gov.uk
    """

    def proxy_site(self, content: HtmlElement) -> (HtmlElement):
        """Basic interventions required to proxy gov.uk"""
        content = self.proxy.all_relative_to_absolute_href_of_a(content)
        content = self.proxy.all_relative_to_absolute_href_of_link_css(content)
        content = self.proxy.all_relative_to_absolute_src_of_img(content)
        content = self.proxy.all_relative_to_absolute_srcset_of_img(content)
        content = self.proxy.all_relative_to_absolute_script_js(content)
        return content


class GovUKStatisticsHandler(GovUKHandler):
    """
    Supplementary handling for gov.uk urls specifically beginning: https://www.gov.uk/government/statistics
    """

    def proxy_page(self, content: HtmlElement) -> (HtmlElement):
        """
        Content insertion for pages of this url pattern.
        """
        return content
