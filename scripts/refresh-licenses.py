"""Re-vendors the license texts in "licenses/" from their upstream sources.

This is a template-authoring script. It is never run while generating a project. A generated project gets its license text from the vendored copy
through a Jinja include, with no network access involved (see docs/project-template/licensing.md).

Two upstream sources are used, because they serve different purposes:

  * choosealicense.com carries the licenses whose copyright line is operative text that the licensee is expected to fill in. Its texts mark those
    spots with "[year]" and "[fullname]" tokens, which this script rewrites into the template's own placeholders.
  * The SPDX license list carries the licenses that are meant to be shipped verbatim. Nothing in those texts is substituted, because altering them is
    either wrong (Apache-2.0, MPL-2.0) or expressly prohibited by the license document itself (the GNU licenses).

Both sources are pinned, so that running the script twice produces the same files. Every text is downloaded and checked before the first file is
written, so a failure part of the way through leaves "licenses/" exactly as it was.

Run it with:

    python3 scripts/refresh-licenses.py
"""

import pathlib
import re
import sys
import urllib.request

# The tag of the SPDX license list release the verbatim texts are pinned to; bump it deliberately, and re-run this script, rather than tracking the
# moving "main" branch
SPDX_LICENSE_LIST_VERSION = 'v3.29.0'

# The commit of choosealicense.com's "gh-pages" branch the substituting texts are pinned to; the repository publishes no releases, so a commit is the
# only fixed point there is; bump it deliberately to the branch's current head (for example with "git ls-remote
# https://github.com/github/choosealicense.com refs/heads/gh-pages"), and re-run this script
CHOOSE_A_LICENSE_COMMIT = 'f66c5dd01866041688edd87f658b6d5ac3304f1b'

SPDX_TEXT_URL = 'https://raw.githubusercontent.com/spdx/license-list-data/{version}/text/{identifier}.txt'
CHOOSE_A_LICENSE_URL = 'https://raw.githubusercontent.com/github/choosealicense.com/{commit}/_licenses/{key}.txt'

# How long a single download may take, in seconds, before the script gives up instead of hanging indefinitely
DOWNLOAD_TIMEOUT = 30

# The licenses whose copyright line the licensee fills in; the value is the file name choosealicense.com uses, which is neither the SPDX identifier
# nor its lower-cased form in every case, so the mapping is spelled out rather than derived
SUBSTITUTING_LICENSES: dict[str, str] = {
    'MIT': 'mit',
    'BSD-2-Clause': 'bsd-2-clause',
    'BSD-3-Clause': 'bsd-3-clause',
}

# The fill-in tokens of the substituting licenses, and the template placeholders they are rewritten into
SUBSTITUTIONS: dict[str, str] = {
    '[year]': '[[ copyright_year ]]',
    '[fullname]': '[[ copyright_holder ]]',
}

# The licenses that are shipped exactly as published; see docs/project-template/licensing.md for why each one is in this list rather than the one
# above
VERBATIM_LICENSES: tuple[str, ...] = (
    'Apache-2.0',
    'MPL-2.0',
    'GPL-3.0-only',
    'GPL-3.0-or-later',
    'LGPL-3.0-only',
    'LGPL-3.0-or-later',
)

# The Jinja delimiters this template uses (see copier.yml); an opening delimiter in a license text would be interpreted as template syntax when the
# text is included, and the closing delimiters are checked as well, as a precaution, because a stray one is a sign of a text that was mangled on its
# way here; the texts are checked before the fill-in tokens are rewritten, since the rewriting introduces delimiters on purpose
FORBIDDEN_DELIMITERS: tuple[str, ...] = ('[[', ']]', '[%', '%]', '[#', '#]')

licenses_directory = pathlib.Path(__file__).resolve().parent.parent / 'licenses'


def fetch(url: str) -> str:
    """Downloads a text file.

    Args:
        url: The URL to download.

    Returns:
        The downloaded file's contents, decoded as UTF-8.

    Raises:
        urllib.error.HTTPError: The server answered with an error status, for example because the file does not exist at the pinned version.
        urllib.error.URLError: The server could not be reached.
        TimeoutError: The download took longer than "DOWNLOAD_TIMEOUT" seconds.
    """

    with urllib.request.urlopen(url, timeout=DOWNLOAD_TIMEOUT) as response:
        return response.read().decode('utf-8')


def strip_front_matter(text: str) -> str:
    """Removes the Jekyll YAML front matter that choosealicense.com puts at the top of each of its license files.

    Args:
        text: The raw file contents, which start with a "---" delimited front matter block.

    Returns:
        The license text alone, with the front matter and the blank line after it removed.
    """

    match = re.match(r'^---\n.*?\n---\n+', text, re.DOTALL)
    return text[match.end():] if match else text


def assert_no_delimiters(identifier: str, text: str) -> None:
    """Fails if a license text contains one of this template's Jinja delimiters.

    Args:
        identifier: The SPDX identifier, used for the error message.
        text: The license text to check.

    Raises:
        SystemExit: The text contains a delimiter, which would break the Jinja include that renders it.
    """

    found = [delimiter for delimiter in FORBIDDEN_DELIMITERS if delimiter in text]
    if found:
        sys.exit(f'"{identifier}" contains the Jinja delimiter(s) {found}, which would break the include in "template/LICENSE"')


def substitute_tokens(identifier: str, text: str) -> str:
    """Rewrites the fill-in tokens of a substituting license into this template's placeholders.

    The tokens are rewritten here, at vendoring time, rather than being substituted at render time by a script, so that rendering a project needs
    nothing but Jinja.

    Args:
        identifier: The SPDX identifier, used for the error message.
        text: The license text, as published by choosealicense.com.

    Returns:
        The license text with every fill-in token replaced by its placeholder.

    Raises:
        SystemExit: A token is missing from the text, which means that choosealicense.com renamed it, and the vendored text would otherwise keep a
            literal token where the copyright line should be.
    """

    missing = [token for token in SUBSTITUTIONS if token not in text]
    if missing:
        sys.exit(f'"{identifier}" does not contain the fill-in token(s) {missing}; check whether choosealicense.com renamed them')

    for token, placeholder in SUBSTITUTIONS.items():
        text = text.replace(token, placeholder)
    return text


def main() -> None:
    """Downloads and checks every license text, and then writes them all into the "licenses" directory."""

    # Every text is downloaded and checked first, and nothing is written until all of them have passed, so that a failure never leaves the
    # directory with a mix of old and new texts
    texts: dict[str, str] = {}
    for identifier, key in SUBSTITUTING_LICENSES.items():
        text = strip_front_matter(fetch(CHOOSE_A_LICENSE_URL.format(commit=CHOOSE_A_LICENSE_COMMIT, key=key)))
        assert_no_delimiters(identifier, text)
        texts[identifier] = substitute_tokens(identifier, text)

    for identifier in VERBATIM_LICENSES:
        text = fetch(SPDX_TEXT_URL.format(version=SPDX_LICENSE_LIST_VERSION, identifier=identifier))
        assert_no_delimiters(identifier, text)
        texts[identifier] = text

    licenses_directory.mkdir(exist_ok=True)
    for identifier, text in texts.items():
        (licenses_directory / f'{identifier}.txt').write_text(text, encoding='utf-8')
        if identifier in SUBSTITUTING_LICENSES:
            print(f'Vendored {identifier} from choosealicense.com at {CHOOSE_A_LICENSE_COMMIT[:12]}, with the copyright line templated')
        else:
            print(f'Vendored {identifier} from the SPDX license list {SPDX_LICENSE_LIST_VERSION}, verbatim')

    print('\n"UNLICENSED.txt" is hand-written and is not touched by this script.')


if __name__ == '__main__':
    main()
