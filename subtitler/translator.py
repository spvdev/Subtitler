"""Offline subtitle translation using Argos Translate."""

import argostranslate.package
import argostranslate.translate


def get_installed_languages():
    """Return a dict mapping language codes to language objects."""
    return {lang.code: lang for lang in argostranslate.translate.get_installed_languages()}


def ensure_language_pair(source_code, target_code):
    """Download and install the translation package for a language pair if needed.

    Args:
        source_code: Source language code (e.g. 'en').
        target_code: Target language code (e.g. 'es').
    """
    installed = get_installed_languages()
    if source_code in installed and target_code in installed:
        source_lang = installed[source_code]
        translation = source_lang.get_translation(installed[target_code])
        if translation is not None:
            return

    print(f"Downloading translation package: {source_code} -> {target_code}...")
    argostranslate.package.update_package_index()
    available = argostranslate.package.get_available_packages()

    pkg = next(
        (p for p in available
         if p.from_code == source_code and p.to_code == target_code),
        None,
    )
    if pkg is None:
        raise ValueError(
            f"No translation package available for {source_code} -> {target_code}. "
            f"Run 'subtitler languages' to see available pairs."
        )

    pkg.install()
    print("Translation package installed.")


def translate_text(text, source_code, target_code):
    """Translate a single string."""
    return argostranslate.translate.translate(text, source_code, target_code)


def translate_srt(subs, source_code, target_code):
    """Translate all subtitle entries in a pysrt SubRipFile in-place.

    Args:
        subs: A pysrt.SubRipFile object.
        source_code: Source language code.
        target_code: Target language code.

    Returns:
        The modified SubRipFile.
    """
    ensure_language_pair(source_code, target_code)

    total = len(subs)
    for i, item in enumerate(subs, start=1):
        translated = translate_text(item.text, source_code, target_code)
        item.text = translated
        if i % 20 == 0 or i == total:
            print(f"  Translated {i}/{total} subtitles...")

    return subs


def list_available_packages():
    """Print all available translation language pairs."""
    argostranslate.package.update_package_index()
    available = argostranslate.package.get_available_packages()
    return [(p.from_name, p.from_code, p.to_name, p.to_code) for p in available]
