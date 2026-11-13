"""Habitat registry. To add one: create habitats/<name>.py exposing
NAME, PLATFORM (dict), build(variant) -> common.Variant, then list it here."""
from habitats import fire, grass, water

REGISTRY = {m.NAME: m for m in (water, fire, grass)}
