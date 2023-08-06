# Linguarita

When gettext doesn't work and you are sick of writing your own language engine for every program, you came to the right place! Linguarita is a generic language engine retrieving translations from JSON files.

The changelog can be found at https://codeberg.org/lucien-rowan/linguarita/src/branch/main/CHANGELOG.md

## Installing the module

You can either copy the source code and directly include linguarita.py into your program but I find that difficult. Instead, you can just open your virtual environment and type `pip install linguarita-lucien-rowan` into the terminal.

## Using the module

Basically, your project needs the following files:
- main.py (can be another name as well, just for execution)
- translations/(lang).json (the translations are stored in JSON files, just replace (lang) with the actual language like en for English, de for German or ua for Ukrainian)

The translations occur with `linguarita.translateText(og_str, langcode)` with og_str being the string you want to translate (must be the same as in the JSON file) and the langcode being the filename of the JSON file before the dot.

## Contributing

Of course, this module also needs some attention.

### Which attention?

- Enhancing it with useful features
- Fixing the bugs that might occur
- Documenting its API
- Translating that documentation to other languages
- Implementing it into Python applications

While Linguarita is a simple module from its code, it might seem a bit hard to implement it in real life scenarios. Therefore, documentation and example applications will follow.