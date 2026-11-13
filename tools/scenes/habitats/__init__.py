"""Habitat registry. To add `grass`: create habitats/<name>.py exposing
NAME, PLATFORM (dict), build(variant) -> common.Variant, then list it here."""
from habitats import fire, water

REGISTRY = {m.NAME: m for m in (water, fire)}
