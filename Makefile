.SILENT:
.ONESHELL:
.PHONY: help setup_all setup_gh_auth generate_tasks start_workspace
.DEFAULT_GOAL := help


# MARK: SETUP


setup_all: generate_tasks start_workspace  ## Run full setup (generate tasks, open workspace)

setup_gh_auth:  ## Configure gh as git credential helper + durable GPG signing config
	if command -v gh > /dev/null 2>&1; then gh auth setup-git; \
	else echo "gh cli not installed. skipping auth."; fi
	git config --global commit.gpgsign true
	git config --global gpg.format openpgp


# MARK: WORKSPACE


generate_tasks:  ## Generate workspace.code-workspace from config/projects.conf
	echo "Generating workspace tasks..."
	bash scripts/generate-tasks.sh

start_workspace:  ## Open workspace in current VS Code window
	if command -v code > /dev/null 2>&1; then code -r workspace.code-workspace; fi


# MARK: HELP


help:  ## Show available recipes grouped by section
	echo "Usage: make [recipe]"
	echo ""
	awk '/^# MARK:/ { \
		section = substr($$0, index($$0, ":")+2); \
		printf "\n\033[1m%s\033[0m\n", section \
	} \
	/^[a-zA-Z0-9_-]+:.*?##/ { \
		helpMessage = match($$0, /## (.*)/); \
		if (helpMessage) { \
			recipe = $$1; \
			sub(/:/, "", recipe); \
			printf "  \033[36m%-22s\033[0m %s\n", recipe, substr($$0, RSTART + 3, RLENGTH) \
		} \
	}' $(MAKEFILE_LIST)
