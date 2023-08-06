def colorWave(text: str, *, textColor: str = "#000", waveColor: str = "#fff"):
    """Automatize the process of making waving color text in CSS.

    Attributes
    -----------
    text: :class:`str`
        The text you want to wave.

    textColor: :class:`str`
        The color of the text. Supports all color syntaxes that CSS supports.\n
        If nothing is provided, it will be ``black``.

    waveColor: :class:`str`
        The color of the text. Supports all color syntaxes that CSS supports.\n
        If nothing is provided, it will be ``white``.
    """
    i = 1
    print("HTML:\n")

    for c in text:
        print(f"<span class=\"char-{i}\">{c}</span>", end="")
        i += 1

    print("\n\n\nCSS:\n")

    i = 1
    percentage = 100 / (len(text) * 2)

    for i in range(1, len(text) + 1):
        print(
            f"""
.char-{i}{{
    animation: char-{i} 4s infinite linear;
}}

@keyframes char-{i}{{
    {percentage * i}%{{
        color: {waveColor};
    }}
    {50 + (percentage * i)}%{{
        color: {textColor};
    }}
}}
            """
        )