ALBUM_RELEASE_ALIASES = {
    "rls",
    "psc",
    "dsc",
}


def detect_intent(text: str) -> str | None:
    if not text:
        return None

    text = text.strip().lower()

    if text in ALBUM_RELEASE_ALIASES:
        return "album_release"

    if text in ["tocando", "vh", "pifm", "cyo", "py", "lcs", "ag", "rosan", "roro", "ro", "rafarl", "pipi", "bressing", "kur", "xxt", "ts", "cebrutius", "tigraofm", "djpi", "royalfm", "geeksfm", "radinho", "qap"]:
        return "play"

    return None
