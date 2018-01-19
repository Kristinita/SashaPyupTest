r"""ASCII Decorator swan font.

.   .           .                 .       .            .        .              .
|  /     o     _|_   o         o _|_      |            |        |      o       |
|-'  .--..  .--.|    .  .--.   .  |  .-.  |    .  . .-.|.-. .  .|      .  .--. |.-.
|  \ |   |  `--.|    |  |  |   |  | (   ) |    |  |(   |-.' |  ||      |  |  | |-.'
'   `' -' `-`--'`-'-' `-'  `--' `-`-'`-'`-'---'`--`-`-''  `-`--|'---'-' `-'  `-'  `-
                                                              ;
                                                           `-'
"""

import os
import sublime_plugin
import sys


# PYTHONPACKAGES path:
# https://stackoverflow.com/a/4907053/5951529
# Disable duplicate paths:
# https://stackoverflow.com/a/42656754/5951529
site_packages = (os.environ['PYTHONPACKAGES'])
if site_packages not in sys.path:
    sys.path.append(site_packages)

# [BUG] StopIteration error
# https://docs.python.org/3/library/exceptions.html#StopIteration
# Append site_packages folder:
# https://stackoverflow.com/a/31384782/5951529
# site_packages = next(p for p in sys.path if 'site-packages' in p)
# sys.path.append(site_packages)


from duckduckgo import query  # noqa
from pygoogling.googling import GoogleSearch  # noqa


class KristinitaLuckyLinkDuckDuckGoCommand(sublime_plugin.TextCommand):
    """Get first link from DuckDuckGo SERP and wrap selected to Markdown link construction.

    Word wrap to Markdown link with first DuckDuckGo SERP result.
    For example, Поиск Кристиниты → [Поиск Кристиниты](http://kristinita.ru/).

    Extends:
        sublime_plugin.TextCommand
    """

    def get_selection(self):
        """Get selection text.

        Get selection text in Sublime Text 3.
        That not use duplicate code.
        See @facelessuser comment:
        http://bit.ly/2m8Gn9W

        Returns:
            object -- return selection region.

        """
        # Get selection text
        select = self.view.sel()
        selection_region = select[0]
        return self.view.substr(selection_region), selection_region

    def replace_selection(self, edit, selection_region, replaced_text):
        """Replace selection text.

        Replace selection text.
        See @facelessuser comment: http://bit.ly/2m8Gn9W

        Arguments:
            edit {str} -- edit text in Sublime Text 3
            selection_region {str} -- selection region in Sublime Text 3
            replaced_variable {str} -- variable, that we can after all actions

        """
        self.view.replace(
            edit, selection_region, replaced_text)

    def run(self, edit):
        """Run KristinitaLuckyLink for DuckDuckGo.

        Using DuckDuckGo module, ported to Sublime Text 3:
            https://github.com/Kristinita/python-duckduckgo
        If use duckduckpy, not all results display correct:
            https://stackoverflow.com/q/11722465/5951529
        That to know, how it works, see:
            https://stackoverflow.com/a/12027009/5951529

        Arguments:
            edit {str} -- edit text in Sublime Text.
        """
        selection_text, selection_region = self.get_selection()
        print('KristinitaLuckyLink DuckDuckGo called')

        # [DEPRECATED] Long way to get DuckDuckGo url:
        #
        # Reasons:
        #
        # 1. Long; new way is short;
        # 2. Additional problems with paths, see http://bit.ly/2CVZizl ,
        # 3. HTML structure of DuckDuckGo SERP can change.
        #
        # import re
        # import sys
        # import urllib
        #
        # from w3lib.url import safe_url_string
        # from bs4 import BeautifulSoup
        # # ASCII link for solved encoding problems —
        # # http://stackoverflow.com/a/40654295/5951529
        # ascii_duckduckgo_link = safe_url_string(
        #     u'http://duckduckgo.com/html/?q=' + (selection_text),
        #     encoding="UTF-8")
        # print(ascii_duckduckgo_link)
        # # SERP DuckDuckGo
        # duckduckgo_serp = urllib.request.urlopen(ascii_duckduckgo_link)
        # # Reading SERP
        # read_duckduckgo_serp = duckduckgo_serp.read()
        # # BeautifulSoup — http://stackoverflow.com/a/11923803/5951529
        # parsed_duckduckgo = BeautifulSoup(read_duckduckgo_serp, "lxml")
        # # Parsed first link
        # first_duckduckgo_link = parsed_duckduckgo.findAll(
        #     'div', {'class': re.compile('links_main*')})[0].a['href']
        # # Remove DuckDuckGo specific characters —
        # # http://stackoverflow.com/a/3942100/5951529
        # remove_duckduckgo_symbols = first_duckduckgo_link.replace(
        #     "/l/?kh=-1&uddg=", "")
        # # Final link — http://stackoverflow.com/a/32451970/5951529
        # final_duckduckgo_link = (
        #     urllib.parse.unquote(remove_duckduckgo_symbols))
        final_duckduckgo_link = query('! ' + selection_text).redirect.url
        print(final_duckduckgo_link)
        markdown_duckduckgo_link = '[' + selection_text + ']' + \
            '(' + final_duckduckgo_link + ')'

        # Replace selected text to Markdown link
        self.replace_selection(
            edit, selection_region, markdown_duckduckgo_link)


class KristinitaLuckyLinkGoogleCommand(KristinitaLuckyLinkDuckDuckGoCommand):
    """Get first link from Google SERP and wrap selected to Markdown link construction.

    Word wrap to Markdown link with first Google SERP result.
    For example, Поиск Кристиниты → [Поиск Кристиниты](http://kristinita.ru/).

    Using pygoogling module:
        https://pypi.python.org/pypi/pygoogling

    google module works with bugs.

    xgoogle module not compatible with Python 3.3, see:
        http://bit.ly/2CURRIx

    python-gsearch not compatible with Python 3.3, see:
        https://github.com/aviaryan/python-gsearch/issues/3
    """

    def run(self, edit):
        """Run KristinitaLuckyLink for Google.

        Arguments:
            edit {str} -- edit text in Sublime Text
        """
        selection_text, selection_region = self.get_selection()
        print('KristinitaLuckyLink Google called')

        # [DEPRECATED] google module:
        #
        # Reason — bugs for:
        #
        # 1. Multiple results («Кристина Кива» query),
        # 2. No result («Python Google» query),
        # 3. News, not SERP («Carmelo Anthony» query),
        # 4. HTML metadata links («YAML» query).
        #
        # About google module:
        # http://archive.li/TaC8V
        # http://archive.li/59pbq
        #
        # from google import search
        # Add pause, because multiple results may appear
        # and user may be blocked
        # for final_google_link in search(
        #         selection_text, num=1, stop=1, pause=5.0):
        #     print(final_google_link)
        google_search = GoogleSearch(selection_text)
        google_search.start_search(max_page=1)
        final_google_link = google_search.search_result[0]
        markdown_google_link = '[' + selection_text + \
            ']' + '(' + final_google_link + ')'

        # Replace selected text to Markdown link
        self.replace_selection(
            edit, selection_region, markdown_google_link)
