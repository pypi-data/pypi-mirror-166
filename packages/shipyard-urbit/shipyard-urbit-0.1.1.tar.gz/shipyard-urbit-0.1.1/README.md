# Shipyard

Urbit hosting and automation platform.

Note: this is a Pre-Release package.  All changes will be breaking.  Wait for release 1.0.0 or later.

## Install

```
pip install shipyard-urbit
```

## Usage

```
shipyard
```

## API Overview

Visit [redacted] for full API Documentation.

## Development

### Modules

#### shipyard

 * `models.py` - types used throughout the project
 * `multi.py` - process management utilities

#### shipyard.api

HTTP API built with FastAPI.

#### shipyard.cli

Command-line interface built with Typer.

#### shipyard.colony

Host setup and configuration using Ansible.

#### shipyard.deploy

Creating and migrating Urbit ships within our host infrastructure.

#### shipyard.envoy

Communication and direction of Urbit ships.

#### shipyard.vigil

Monitoring and alerting. WIP.

## License

This project is licensed under Apache-2.0.  Code licensed from other projects will be clearly marked with the appropriate notice.
