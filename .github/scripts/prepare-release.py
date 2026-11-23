"""Prepares the release of the newest version in "CHANGELOG.md": checks that it is ready, and writes its tag message and its release notes.

The "Release" workflow runs this script once the release pull request has been merged, and creates the annotated tag and the GitHub Release from what
it writes (see docs/conventions/versioning.md). The "Linters" workflow runs it as a dry run on every pull request, so that a changelog the script
cannot read, or a bullet it cannot wrap, shows up long before the release rather than during it.

The release is the first "## Release vX.Y.Z" section of the changelog. Before anything is written, the script checks that:

  * the section has a date paragraph that reads "*Released on Month D, YYYY.*", rather than the one of an unreleased version,
  * the section is a flat list of bullets, with no opening paragraph, and
  * the version is the same in "package.json" and in "package-lock.json" (see docs/conventions/versioning.md).

A dry run reports a release that is not ready yet, which is what the changelog looks like between two releases, without failing, and uses the
current date in place of the missing release date; a changelog the script cannot read fails a dry run too. Whether the tag already exists is checked
by the workflow, since it needs the remote.

The script writes two files into the output directory:

  * "tag-message.txt", the message of the annotated tag, which follows the tag message rules (see docs/conventions/commit-messages.md): the subject
    "Release vX.Y.Z (Month D, YYYY)", a blank line, and the release's bullets, wrapped at 72 characters without ever breaking a code span.
  * "release-notes.md", the notes of the GitHub Release, which are the same bullets exactly as the changelog has them, unwrapped.

When it runs in GitHub Actions, it also sets the step outputs "version" and "tag". Run it from the root of the repository with:

    python3 .github/scripts/prepare-release.py --output-directory <directory>
    python3 .github/scripts/prepare-release.py --dry-run
"""

import argparse
import datetime
import json
import os
import pathlib
import re
import sys

# The width a line of the tag message's body is wrapped at, the 72 of the 50/72 rule (see docs/conventions/commit-messages.md)
WRAP_WIDTH = 72

# What a bullet's first line, and every line it continues on, start with in the tag message, so that a wrapped bullet stays aligned with its text
BULLET_PREFIX = '- '
CONTINUATION_PREFIX = '  '

# The date paragraph of an unreleased version, which the release branch replaces with the release date (see docs/conventions/changelog-entries.md)
UNRELEASED_DATE_PARAGRAPH = '*Release date to be determined.*'

release_heading_pattern = re.compile(r'^## Release v(\d+\.\d+\.\d+)$')
release_date_pattern = re.compile(r'^\*Released on (.+)\.\*$')

repository_root = pathlib.Path(__file__).resolve().parent.parent.parent


class ChangelogError(Exception):
    """The changelog cannot be read, so no tag message can be written from it, which fails even a dry run."""


def read_release(changelog: str) -> tuple[str, str, list[str]]:
    """Reads the newest release from the changelog.

    Args:
        changelog: The contents of "CHANGELOG.md".

    Returns:
        The release's version without the "v" prefix, its date paragraph, and its bullets, each without the "- " it starts with and with the lines
        it continues on joined into one.

    Raises:
        ChangelogError: The changelog has no release, the release has no date paragraph or no bullets, or it has text that is not part of a bullet.
    """

    lines = changelog.splitlines()
    start = next((index for index, line in enumerate(lines) if line.startswith('## Release ')), None)
    if start is None:
        raise ChangelogError('The changelog has no "## Release vX.Y.Z" heading')
    heading_match = release_heading_pattern.match(lines[start])
    if not heading_match:
        raise ChangelogError(f'The heading "{lines[start]}" does not read "## Release vX.Y.Z"')
    version = heading_match.group(1)

    end = next((index for index in range(start + 1, len(lines)) if lines[index].startswith('#')), len(lines))
    paragraphs = lines[start + 1:end]
    while paragraphs and not paragraphs[0].strip():
        paragraphs.pop(0)
    if not paragraphs or not paragraphs[0].startswith('*'):
        raise ChangelogError(f'Release v{version} has no date paragraph below its heading')
    date_paragraph = paragraphs.pop(0)

    bullets: list[str] = []
    for line in paragraphs:
        if line.startswith(BULLET_PREFIX):
            bullets.append(line[len(BULLET_PREFIX):].strip())
        elif line.startswith(' ') and line.strip() and bullets:
            bullets[-1] = f'{bullets[-1]} {line.strip()}'
        elif line.strip():
            raise ChangelogError(f'Release v{version} has a line that is not part of a bullet, but the release is a flat list: "{line}"')
    if not bullets:
        raise ChangelogError(f'Release v{version} has no bullets')

    return version, date_paragraph, bullets


def read_release_date(version: str, date_paragraph: str) -> datetime.date:
    """Reads the release date from the release's date paragraph.

    Args:
        version: The release's version, used for the error message.
        date_paragraph: The paragraph below the release's heading.

    Returns:
        The release date.

    Raises:
        ValueError: The paragraph is the one of an unreleased version, or it does not read "*Released on Month D, YYYY.*".
    """

    if date_paragraph == UNRELEASED_DATE_PARAGRAPH:
        raise ValueError(f'Release v{version} is not released yet: its date paragraph still reads "{UNRELEASED_DATE_PARAGRAPH}"')
    date_match = release_date_pattern.match(date_paragraph)
    if not date_match:
        raise ValueError(f'The date paragraph of release v{version} does not read "*Released on Month D, YYYY.*": "{date_paragraph}"')
    try:
        return datetime.datetime.strptime(date_match.group(1), '%B %d, %Y').date()
    except ValueError:
        raise ValueError(f'The release date of v{version} is not a date written as "Month D, YYYY": "{date_match.group(1)}"') from None


def find_version_mismatches(version: str) -> list[str]:
    """Compares the release's version with the version of every manifest that has to carry the same one.

    Args:
        version: The release's version, from the changelog.

    Returns:
        A description of every manifest whose version differs, or an empty list if all of them match.
    """

    mismatches: list[str] = []
    package = json.loads((repository_root / 'package.json').read_text(encoding='utf-8'))
    if package.get('version') != version:
        mismatches.append(f'"package.json" has version {package.get("version")}, but the changelog\'s newest release is v{version}')

    lock_file_path = repository_root / 'package-lock.json'
    if lock_file_path.exists():
        lock_file = json.loads(lock_file_path.read_text(encoding='utf-8'))
        lock_file_versions = {lock_file.get('version'), lock_file.get('packages', {}).get('', {}).get('version')}
        if lock_file_versions != {version}:
            mismatches.append(f'"package-lock.json" does not have version {version} throughout; run "npm install" to bring it up to date')

    return mismatches


def split_into_words(text: str) -> list[str]:
    """Splits a bullet into the words it is wrapped by, keeping every code span whole.

    A word ends at a space, unless the space is inside a code span, so that a code span with spaces in it, together with any punctuation attached to
    it, stays one word. A code span is opened by a run of backticks and closed by the next run of the same length, as in Markdown, so that a
    code span delimited by two backticks may contain a single one. A run of backticks that is never closed is taken literally.

    Args:
        text: The bullet's text, on one line.

    Returns:
        The bullet's words, in order.
    """

    words: list[str] = []
    current = ''
    index = 0
    while index < len(text):
        character = text[index]
        if character == '`':
            run_length = len(text) - index - len(text[index:].lstrip('`'))
            delimiter = '`' * run_length
            closing = re.compile(rf'(?<!`){delimiter}(?!`)').search(text, index + run_length)
            if closing:
                current += text[index:closing.end()]
                index = closing.end()
            else:
                current += delimiter
                index += run_length
        elif character == ' ':
            if current:
                words.append(current)
            current = ''
            index += 1
        else:
            current += character
            index += 1
    if current:
        words.append(current)
    return words


def wrap_bullet(text: str) -> list[str]:
    """Wraps a bullet at "WRAP_WIDTH" characters, with its continuation lines indented to its text, without ever breaking a code span.

    Args:
        text: The bullet's text, on one line and without the "- " it starts with.

    Returns:
        The bullet's lines, the first starting with "- ".

    Raises:
        ChangelogError: A word is too long for a line of its own, which only happens with a long code span; the tag message rules ask to reword the
            bullet then, rather than to break the code span.
    """

    lines: list[str] = []
    current = BULLET_PREFIX
    for word in split_into_words(text):
        if len(CONTINUATION_PREFIX) + len(word) > WRAP_WIDTH:
            raise ChangelogError(f'"{word}" is too long for a line of {WRAP_WIDTH} characters; reword the bullet, since a code span is never broken')
        separator = '' if current in (BULLET_PREFIX, CONTINUATION_PREFIX) else ' '
        if len(current) + len(separator) + len(word) > WRAP_WIDTH:
            lines.append(current)
            current = CONTINUATION_PREFIX + word
        else:
            current += separator + word
    lines.append(current)
    return lines


def report(message: str, level: str) -> None:
    """Prints a message, as an annotation of the given level when the script runs in GitHub Actions.

    Args:
        message: The message to print.
        level: The annotation level, "error", "warning", or "notice".
    """

    if os.environ.get('GITHUB_ACTIONS') == 'true':
        print(f'::{level}::{message}', file=sys.stderr)
    else:
        print(f'{level.capitalize()}: {message}', file=sys.stderr)


def main() -> int:
    """Checks the newest release of the changelog, and writes its tag message and its release notes.

    Returns:
        The exit code: 0 if the release is ready, or if a dry run could read the changelog, and 1 otherwise.
    """

    parser = argparse.ArgumentParser(description='Checks the newest release of "CHANGELOG.md", and writes its tag message and its release notes.')
    parser.add_argument('--output-directory', type=pathlib.Path, help='the directory the tag message and the release notes are written into')
    parser.add_argument('--dry-run', action='store_true', help='reports a release that is not ready without failing, and writes nothing')
    arguments = parser.parse_args()
    if not arguments.dry_run and arguments.output_directory is None:
        parser.error('--output-directory is required unless --dry-run is given')

    try:
        version, date_paragraph, bullets = read_release((repository_root / 'CHANGELOG.md').read_text(encoding='utf-8'))
        body = [line for bullet in bullets for line in wrap_bullet(bullet)]
    except ChangelogError as error:
        report(str(error), 'error')
        return 1

    problems = find_version_mismatches(version)
    try:
        release_date = read_release_date(version, date_paragraph)
    except ValueError as error:
        problems.insert(0, str(error))
        release_date = datetime.date.today()
    if problems:
        for problem in problems:
            report(problem, 'notice' if arguments.dry_run else 'error')
        if not arguments.dry_run:
            return 1

    subject = f'Release v{version} ({release_date.strftime("%B")} {release_date.day}, {release_date.year})'
    tag_message = '\n'.join([subject, '', *body]) + '\n'
    release_notes = '\n'.join(f'{BULLET_PREFIX}{bullet}' for bullet in bullets) + '\n'

    if arguments.dry_run:
        print(tag_message, end='')
        if problems:
            print(f'\nRelease v{version} is not ready yet, so the release date above is the current date.')
        return 0

    arguments.output_directory.mkdir(parents=True, exist_ok=True)
    (arguments.output_directory / 'tag-message.txt').write_text(tag_message, encoding='utf-8')
    (arguments.output_directory / 'release-notes.md').write_text(release_notes, encoding='utf-8')
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as output:
            output.write(f'version={version}\ntag=v{version}\n')
    print(tag_message, end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
