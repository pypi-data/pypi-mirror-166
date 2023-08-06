"""Configuration utilities."""
from dataclasses import dataclass, fields
from pathlib import Path
from urllib.parse import urlparse

from .error import ProviderConfigError

# FIXME: type-check when we drop support for Python 3.10
try:
    import tomllib  # type: ignore
except ImportError:
    import toml as tomllib  # type: ignore

DEFAULT_CONFIG_FILE = "pyproject.toml"

DEFAULT_OIDC_SCOPE = "openid profile email"
DEFAULT_REDIRECT_URI = "http://127.0.0.1:39303/oauth2/callback"


@dataclass(frozen=True)
class ProviderConfig:
    """OIDC provider configuration."""

    issuer: str
    authorization_endpoint: str
    token_endpoint: str


def validate_redirect_uri(uri: str) -> None:
    """Validate redirection URI."""
    redirect_uri = urlparse(uri)

    if redirect_uri.scheme not in ("http", "https"):
        raise ProviderConfigError("redirect scheme must be 'http' or 'https'.")

    if not redirect_uri.hostname or not redirect_uri.port:
        raise ProviderConfigError("redirection URI must include hostname and port.")

    if redirect_uri.params or redirect_uri.query:
        raise ProviderConfigError("redirection URI must not include query params.")

    if redirect_uri.hostname != "127.0.0.1" and redirect_uri.scheme == "http":
        raise ProviderConfigError("TLS must be enabled for non-loopback interfaces.")


@dataclass(frozen=True)
class ClientProfile:
    """OIDC client profile."""

    issuer: str
    client_id: str
    client_secret: str | None = None
    redirect_uri: str = DEFAULT_REDIRECT_URI
    scope: str = DEFAULT_OIDC_SCOPE

    def __post_init__(self) -> None:
        if not self.issuer.startswith("https://"):
            raise ProviderConfigError("OIDC issuer must be HTTPS.")

        validate_redirect_uri(self.redirect_uri)


def read_profile(path: Path, profile_name: str | None = None) -> ClientProfile:
    """Read an (optionally named) OIDC client profile from a config file."""
    with open(path) as config_file:
        data = tomllib.load(config_file)["tool"]["oidc"]
        if profile_name:
            data = data[profile_name]

    return ClientProfile(
        **{
            key: value
            for key, value in data.items()
            # Ignore extra keys that are not profile fields
            if key in (field.name for field in fields(ClientProfile))
        }
    )
