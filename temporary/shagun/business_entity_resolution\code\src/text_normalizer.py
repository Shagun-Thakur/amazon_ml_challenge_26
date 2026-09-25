import re
import unicodedata

# Order longer phrases before their abbreviations to avoid partial matches
LEGAL_SUFFIX_REGEX = re.compile(
    r"\b(incorporated|corporation|private|privee|prive|limited|company|"
    r"inc|llc|corp|ltd|co|pvt|sa|sarl|sas|sasu|eurl|gmbh|plc|pty)\b",
    flags=re.IGNORECASE,
)

ADDRESS_ABBREVIATIONS = {
    # Standard road types specified in brief
    "rd": "road",
    "st": "street",
    "ave": "avenue",
    "blvd": "boulevard",
    # Additional common street and building abbreviations
    "ln": "lane",
    "dr": "drive",
    "ct": "court",
    "pkg": "parking",
    "pkwy": "parkway",
    "hwy": "highway",
    "sq": "square",
    "cir": "circle",
    "apt": "apartment",
    "ste": "suite",
    "bldg": "building",
    "fl": "floor",
    # French road designations
    "bd": "boulevard",
    "bld": "boulevard",
    "av": "avenue",
    "rte": "route",
}


def normalize_unicode(text: str) -> str:
    """
    Unicode NFKD normalization to remove accents and transliterations without losing base characters.
    Handles French ligatures (œ, æ) and decomposes diacritics (é -> e, ç -> c).
    """
    if not text:
        return ""
    # Standardize ligatures
    s = (
        text.replace("œ", "oe")
        .replace("Œ", "Oe")
        .replace("æ", "ae")
        .replace("Æ", "Ae")
    )
    # Decompose unicode characters into base + diacritics, then discard diacritics
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")


def clean_base_text(text: str) -> str:
    """
    Standardizes text:
    - Unicode NFKD normalization
    - Lowercase
    - Replace '&' with ' and '
    - Strip all non-alphanumeric characters (keeping whitespace)
    - Collapse consecutive whitespace
    """
    if not text:
        return ""
    norm = normalize_unicode(text).lower()
    norm = norm.replace("&", " and ")
    norm = re.sub(r"[^a-z0-9\s]", " ", norm)
    return re.sub(r"\s+", " ", norm).strip()


def strip_legal_suffixes(business_name: str) -> str:
    """
    Removes corporate entity legal suffixes strictly from business names.
    If stripping empties the name completely, returns the original stripped name.
    """
    if not business_name:
        return ""
    cleaned = LEGAL_SUFFIX_REGEX.sub(" ", business_name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    # Clean trailing conjunctions left behind by patterns like "& co" or "& inc"
    cleaned = re.sub(r"\s+(and|&)$", "", cleaned).strip()
    return cleaned if cleaned else business_name.strip()


def expand_address_abbreviations(address: str) -> str:
    """
    Normalizes street, road, and unit abbreviations to canonical tokens.
    """
    if not address:
        return ""
    words = address.split()
    expanded = [ADDRESS_ABBREVIATIONS.get(w, w) for w in words]
    return " ".join(expanded)