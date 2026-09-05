"""Configuration management."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")
DEFAULT_GEMINI_MODEL = "gemini-3.6-flash"


@dataclass
class Config:
    """Application configuration from environment variables."""

    # Google Cloud / Gemini
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip() or DEFAULT_GEMINI_MODEL

    # Google Cloud Project (for future Firestore, Pub/Sub, etc.)
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        return cls(
            GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY", ""),
            GEMINI_MODEL=os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip() or DEFAULT_GEMINI_MODEL,
            GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", ""),
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
        )

    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if not self.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")

        placeholder_values = {
            "your_google_api_key_here",
            "your_api_key_here",
            "replace_me",
            "changeme",
            "example",
            "test",
        }
        if self.GOOGLE_API_KEY.strip().lower() in placeholder_values:
            raise ValueError("GOOGLE_API_KEY still contains a placeholder value. Replace it with a real Gemini API key.")

        return True
