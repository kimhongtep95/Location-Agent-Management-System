# SearchBugs Platform

Infrastructure and delivery assets for the SearchBugs system.

## Included

- Local development stack with API, web, PostgreSQL, and Redis
- Health checks and volume wiring
- GitHub Actions workflow to validate the compose stack definition
- Environment template for local and deployment configuration

## Usage

```bash
cp .env.example .env
docker compose up --build
```

The compose file expects the sibling repositories to exist in the same parent folder:

- `../searchbugs-bug-tracking-project-management`
- `../e-commerce-inventory-platform`
