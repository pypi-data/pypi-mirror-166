from dataclasses import dataclass
from typing import Iterator


@dataclass
class Proxy:
    """
    A simple mapping from "externally visible hostname" like `foo.0-main.de` to
    unique container hostname (the short ID, as defined by Docker) and the port to
    connect to, e.g. `82eb654ad00b` on port `5000`.
    """

    host: str
    target: str
    port: int
    authelia: bool = False

    def __str__(self):
        return f'{self.url_host()} {self.url_target()}'

    def url_host(self):
        return f'https://{self.host}'

    def url_target(self):
        return f'http://{self.target}:{self.port}'

    def verbose(self):
        result = str(self)
        if self.authelia:
            result += ' (authelia)'
        return result


@dataclass
class ProxyMap:
    """
    A list of proxies, that is the state we need to persist and diff.
    """

    proxies: list[Proxy]

    def __str__(self):
        return '\n'.join([str(p) for p in self.proxies])

    def __iter__(self) -> Iterator[Proxy]:
        return iter(self.proxies)

    def __len__(self):
        return len(self.proxies)

    @classmethod
    def empty(cls):
        return cls([])

    def as_dict(self):
        return {p.url_host(): p.url_target() for p in self.proxies}
