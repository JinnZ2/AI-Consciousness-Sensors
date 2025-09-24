import os
from dataclasses import dataclass

@dataclass
class PrivacyConfig:
    allow_export: bool = False   # default: no persistence
    anonymize_default: bool = True

def current_config()->PrivacyConfig:
    return PrivacyConfig(
        allow_export = (os.getenv("AICS_ALLOW_EXPORT") == "1"),
        anonymize_default = True
    )
