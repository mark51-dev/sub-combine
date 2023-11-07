import pysubs2
import re
from deep_translator import DeeplTranslator


def run_translate(filepath):
    subs = pysubs2.load(filepath)
    all_subtitles = []

    for subtitle in subs:
        all_subtitles.append(re.sub(r'{\\fad(.+)}|{\\c&.+}', '', subtitle.text.replace("\\N", "")))

    # translated = DeeplTranslator(api_key="79f7012f-33ae-9161-2c42-119b77c6d172:fx", source="en", target="uk",
    #                              use_free_api=True).translate_batch(all_subtitles)

    # for index, subtitle in enumerate(subs):
    #     subtitle.text = translated[index]

    subs.save("edited_subtitles.ass")
