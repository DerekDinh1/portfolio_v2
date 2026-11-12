"""Habitat registry. To add `fire` or `grass`: create habitats/<name>.py exposing
NAME, PLATFORM (dict), build(variant) -> common.Variant, then list it here."""
from habitats import water

REGISTRY = {m.NAME: m for m in (water,)}
