def detect_intent(text: str) -> str | None:
    if not text:
        return None

    text = text.strip().lower()

    if text in ["tocando", "pifm", "kmed", "ky", "cyo", "py", "braya", "dead", "ag", "rosan", "roro", "ro", "rafarl", "pipi", "bressing", "kur", "xxt", "ts", "cebrutius", "tigraofm", "djpi", "royalfm", "geeksfm", "radinho", "qap"]:
        return "play"

    return None
