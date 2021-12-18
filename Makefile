#!/usr/bin/make

.PHONY: help migrate

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[32m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

migrate: ## Авто-миграция
	alembic revision --autogenerate
	alembic upgrade head
