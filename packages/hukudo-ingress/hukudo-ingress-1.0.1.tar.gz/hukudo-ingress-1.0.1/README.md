# Ingress
Configure Caddy as an ingress for your Docker containers.

## Usage
```
pip install hukudo-ingress==1.0.1
ingress --help
```

## Development
Initial
```
make dev-setup
ingress --help
```

[Completion](https://click.palletsprojects.com/en/8.1.x/shell-completion/)
```
eval "$(_INGRESS_COMPLETE=bash_source ingress)"
```
