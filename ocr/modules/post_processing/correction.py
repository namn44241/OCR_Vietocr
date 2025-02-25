from ...helpers.timer import timer
MAX_LENGTH = 512

@timer
def correct(text: str, corrector) -> str:
    corrected_text = corrector(text.lower(), max_length = MAX_LENGTH)[0]['generated_text']
    return corrected_text