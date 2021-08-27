import requests

from handlers.abstract import BaseHtmlHandler, BaseApiHandler
from handlers.helpers.xpath import (
    copy_first_element_matching,
    assert_get_one,
    first_element_matching
)

from lxml.html import HtmlElement

class GovUKHandler(BaseHtmlHandler):
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

    def proxy_page(self, content: HtmlElement, url: str) -> (HtmlElement):
        """
        Content insertion for pages of this url pattern.
        """
        from lxml import html

        # If there's no declared transformed datasets for this particular page, just return as-is.
        supplementary_content = self.db.get_mapped_resource_from_landing_page(url)
        if not supplementary_content:
            return content
        else:
            # COPY the html representing an existing download
            download_section_element = copy_first_element_matching(content, "//section[contains(@class, 'attachment embedded')]")

           # Rewrite title and link
            element_a: HtmlElement = assert_get_one(download_section_element, "./div/h3/a")
            element_a.set("href", supplementary_content.csvw)
            element_a.text = element_a.text.replace('Excel', 'CSVW')

            # Rewrite metdata
            element_p: HtmlElement = assert_get_one(download_section_element, "./div/p/span[contains(@class, 'type')]")
            element_p.text = 'CSVW'
            element_p: HtmlElement = assert_get_one(download_section_element, "./div/p/span[contains(@class, 'file-size')]")
            element_p.text = ''

            # Insert it as just another child of the download section
            parent: HtmlElement = first_element_matching(content, "//div[contains(@class, 'gem-c-govspeak govuk-govspeak direction-ltr')]")
            parent.insert(-1, download_section_element)

            return content

class GovUKApiContentHandler(BaseApiHandler):

        # TODO: properly
        def proxy_api(self, url):
            return requests.get(url).json()

