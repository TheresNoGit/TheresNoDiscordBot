"""Parses wikilinks."""
import re
import urllib.parse

from discord.ext.commands import UserInputError

from utils import AliasDict


_VALID_LINK = re.compile(
    r"""
        \[\[
        (?!
            (
                [^]|]*
                (
                    ~{3,} .*?  # 3+ tildes is illegal.
                    # So are certain combinations of .s and /s.
                    | /\.\.?(/ .*?)?
                )
                | \.\.? .*?
            )
            (\||\]\])
        )
        (?P<wikilink> [^][<>{}#|]+ )
        ( \|.*? )?
        \]\]
    """,
    re.VERBOSE
)
_WIKI_FAMILIES = AliasDict(
    {('w', 'testwiki', 'test2wiki', 'nost', 'nostalgia'): 'wikipedia',
     'wikt': 'wiktionary',
     'b': 'wikibooks',
     ('d', 'testwikidata'): 'wikidata',
     'n': 'wikinews',
     'q': 'wikiquote',
     's': 'wikisource',
     'species': 'wikispecies',
     'v': 'wikiversity',
     'voy': 'wikivoyage'},
    value_isnt_alias={
        ('c', 'commons', 'm', 'meta', 'metawiki',
         'incubator'): 'wikimedia',
        'mw': 'mediawiki'
    }
)
_WIKI_LANGS = {
    'aa', 'ab', 'ace', 'ady', 'af', 'ak', 'als', 'alt', 'am', 'an', 'ang',
    'ar', 'arc', 'ary', 'arz', 'as', 'ast', 'atj', 'av', 'avk', 'awa', 'ay',
    'az', 'azb', 'ba', 'ban', 'bar', 'bat-smg', 'bcl', 'be', 'be-tarask',
    'be-x-old', 'bg', 'bh', 'bi', 'bjn', 'bm', 'bn', 'bo', 'bpy', 'br', 'bs',
    'bug', 'bxr', 'ca', 'cbk-zam', 'cdo', 'ce', 'ceb', 'ch', 'cho', 'chr',
    'chy', 'ckb', 'co', 'cr', 'crh', 'cs', 'csb', 'cu', 'cv', 'cy', 'da',
    'dag', 'de', 'din', 'diq', 'dsb', 'dty', 'dv', 'dz', 'ee', 'el', 'eml',
    'en', 'eo', 'es', 'et', 'eu', 'ext', 'fa', 'ff', 'fi', 'fiu-vro', 'fj',
    'fo', 'fr', 'frp', 'frr', 'fur', 'fy', 'ga', 'gag', 'gan', 'gcr', 'gd',
    'gl', 'glk', 'gn', 'gom', 'gor', 'got', 'gu', 'gv', 'ha', 'hak', 'haw',
    'he', 'hi', 'hif', 'ho', 'hr', 'hsb', 'ht', 'hu', 'hy', 'hyw', 'hz', 'ia',
    'id', 'ie', 'ig', 'ii', 'ik', 'ilo', 'inh', 'io', 'is', 'it', 'iu', 'ja',
    'jam', 'jbo', 'jv', 'ka', 'kaa', 'kab', 'kbd', 'kbp', 'kg', 'ki', 'kj',
    'kk', 'kl', 'km', 'kn', 'ko', 'koi', 'kr', 'krc', 'ks', 'ksh', 'ku', 'kv',
    'kw', 'ky', 'la', 'lad', 'lb', 'lbe', 'lez', 'lfn', 'lg', 'li', 'lij',
    'lld', 'lmo', 'ln', 'lo', 'lrc', 'lt', 'ltg', 'lv', 'mad', 'mai',
    'map-bms', 'mdf', 'mg', 'mh', 'mhr', 'mi', 'min', 'mk', 'ml', 'mn', 'mni',
    'mnw', 'mo', 'mr', 'mrj', 'ms', 'mt', 'mus', 'mwl', 'my', 'myv', 'mzn',
    'na', 'nah', 'nap', 'nds', 'nds-nl', 'ne', 'new', 'ng', 'nia', 'nl', 'nn',
    'no', 'nov', 'nqo', 'nrm', 'nso', 'nv', 'ny', 'oc', 'olo', 'om', 'or',
    'os', 'pa', 'pag', 'pam', 'pap', 'pcd', 'pdc', 'pfl', 'pi', 'pih', 'pl',
    'pms', 'pnb', 'pnt', 'ps', 'pt', 'qu', 'rm', 'rmy', 'rn', 'ro', 'roa-rup',
    'roa-tara', 'ru', 'rue', 'rw', 'sa', 'sah', 'sat', 'sc', 'scn', 'sco',
    'sd', 'se', 'sg', 'sh', 'shi', 'shn', 'shy', 'si', 'simple', 'sk', 'skr',
    'sl', 'sm', 'smn', 'sn', 'so', 'sq', 'sr', 'srn', 'ss', 'st', 'stq', 'su',
    'sv', 'sw', 'szl', 'szy', 'ta', 'tay', 'tcy', 'te', 'tet', 'tg', 'th',
    'ti', 'tk', 'tl', 'tn', 'to', 'tpi', 'tr', 'trv', 'ts', 'tt', 'tum', 'tw',
    'ty', 'tyv', 'udm', 'ug', 'uk', 'ur', 'uz', 've', 'vec', 'vep', 'vi',
    'vls', 'vo', 'wa', 'war', 'wo', 'wuu', 'xal', 'xh', 'xmf', 'yi', 'yo',
    'yue', 'za', 'zea', 'zh', 'zh-classical', 'zh-min-nan', 'zh-yue', 'zu'
}
_WIKI_PSEUDOLANGS = AliasDict(
    {'c': 'commons',
     ('m', 'metawiki'): 'meta',
     'nost': 'nostalgia'},
    value_isnt_alias={('d', 'wikidata', 'mediawiki', 'species',
                       'wikispecies'): 'www',
                      ('testwiki', 'testwikidata'): 'test',
                      'test2wiki': 'test2'},
    unaliased={'incubator'}
)
_VALID_PREFIXES = (_WIKI_FAMILIES.keys()
                   | _WIKI_LANGS
                   | _WIKI_PSEUDOLANGS.keys())


def extract(text: str) -> list[str]:
    """Get a wikilink."""
    return [i.group('wikilink') for i in _VALID_LINK.finditer(text)]


def parse(link: str) -> str:
    """Parse a wikilink."""
    parts = link.lstrip(':').split(':')
    # Check for text that isn't actually a lang/family code.
    for idx, part in enumerate(parts):
        if part.lower() not in _VALID_PREFIXES:
            page = ':'.join(parts[idx:])
            prefixes = [i.lower() for i in parts[:idx]]
            break
    else:
        page = parts[-1]
        prefixes = []
    family, lang = 'wikipedia', 'en'

    if len(prefixes) > 2:
        raise UserInputError
    if len(prefixes) == 2:
        # Exactly 1 family code and exactly 1 language code.
        if not all(len(set(prefixes) & s) == 1
                   for s in (_WIKI_FAMILIES.keys(), _WIKI_LANGS)):
            raise UserInputError
        prefixes.sort(key=lambda x: x in _WIKI_FAMILIES)
        # Cases like `[[d:fr:Foo]]`.
        if prefixes[1] in _WIKI_PSEUDOLANGS:
            raise UserInputError
        family = _WIKI_FAMILIES[prefixes[1]]
        lang = prefixes[0]
    elif prefixes:
        family = _WIKI_FAMILIES.get(prefixes[0], family)
        lang = _WIKI_PSEUDOLANGS.get(
            prefixes[0],
            prefixes[0] if prefixes[0] in _WIKI_LANGS else lang
        )

    return (f"<https://{lang}.{family}.org/wiki/{urllib.parse.quote(page)}>")
