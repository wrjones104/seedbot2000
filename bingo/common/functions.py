from .constants import CHAR_TO_CODE, CODE_TO_CHAR


def text_to_DTE_Bytes(text: str) -> bytes:
    """Converts ``text`` to FF6 DTE text bytes
    Parameters
    ----------
    text : str
        The text to be converted

    Returns
    -------
    bytes
        An FF6 DTE bytes representation of ``text``
    """
    error = ""
    invalid_chars = set()
    if not isinstance(text, str):
        error += "Input text must be type str. Found type %s\n" % (type(text))
        raise Exception(error)

    # There are di- and trigraphs in here, so we need to be careful to be efficient
    btext = text.encode()
    ## TODO


def text_to_bytes(text: str, length=0) -> bytes:
    """Converts ``text`` to FF6 text bytes, right-padding with 0xFF up until a length of ``length``. If ``length`` is
       is 0, it is set to the length of ``text``

    Parameters
    ----------
    text : str
        The text to be converted
    length : int : optional
        The length to pad the bytes string to. Right pads with 0xFF until ``length`` is reached.
        If ``length`` is 0, it is set to the length of ``text``

    Returns
    -------
    bytes
        An FF6 bytes representation of ``text``
    """

    error = ""
    invalid_chars = set()
    if not isinstance(text, str):
        error += "Input text must be type str. Found type %s\n" % (type(text))
    else:
        for character in text:
            if not character in CHAR_TO_CODE.keys():
                invalid_chars.add(character)
        if len(invalid_chars) != 0:
            error += "Found the following invalid characters in input text\n\t%s\n" % (('').join(invalid_chars))
    if not isinstance(length, int):
        error += "Input length must be type int. Found type %s\n" % (type(length))
    if length < 0:
        error += "Input length must be 0 (for no padding) or a positive integer. Found %s\n" % (length)
    if error != "":
        raise Exception(error)

    if length == 0:
        length = len(text)
    text_chars = [CHAR_TO_CODE[c] for c in text]

    while len(text_chars) < length:
        text_chars.append(0xFF)
    return bytes(text_chars)


def bytes_to_text(btext: bytes) -> str:
    """Converts ``btext``, containing FF6 byte text to regular text

    Parameters
    ----------
    btext : bytes
        The FF6 byte text to be converted

    Returns
    -------
    str
        A textual representation of the FF6 bytes in ``btext``
    """
    error = ""
    invalid_bytes = set()
    if not isinstance(btext, bytes):
        error += "Input btext must be type bytes. Found type %s\n" % (type(btext))
    else:
        for b in btext:
            if not b in CODE_TO_CHAR.keys():
                invalid_bytes.add(b)
            if len(invalid_bytes) != 0:
                error += "Found the following invalid bytes in input btext\n\t%s\n" % (('').join(invalid_bytes))
    if error != "":
        raise Exception(error)

    output = [CODE_TO_CHAR[b] for b in btext]
    return ('').join(output)


def format_hex(bstring: bytes, line_length: int) -> str:
    """Converts a byte string to space-delimted two-character hex values with line breaks at an interval
       of ``line_length``. As an example \x80\x81\x82\x83 with ``line_length`` of 2 would yield:

       80 81
       82 83

    Parameters
    ----------
    bstring : bytes
        The byte string to be formatted. Can be int if it is only one character.
    line_length : int
        The number 2-digit hex values per line in the output

    Returns
    -------
    str
        A formatted string representation of the input bytes
    """
    error = ""
    if not isinstance(bstring, (bytes, int)):
        error += "Input bstring must be bytes or int. Found type %s\n" % (type(bstring))
    elif isinstance(bstring, int) and not 0 <= bstring <= 255:
        error += "If input bstring is int, it must be between 0 and 255 inclusive. Found value %s\n" % (bstring)

    if error != "":
        raise Exception(error)

    output = ['']
    counter = 0
    if isinstance(bstring, int):
        bstring = bstring.to_bytes(1, 'little')
    for b in bstring:
        h = str(hex(b))[2:]
        if len(h) < 2:
            h = "0" + h
        output.append(h)
        counter += 1
        if counter % line_length == 0:
            output.append("\n")
            counter = 0

    return (' ').join(output).strip().replace(' \n ', '\n')
