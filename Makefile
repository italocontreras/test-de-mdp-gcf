SHELL=/bin/sh

export COMPOSE_DOCKER_CLI_BUILD=1
export BUILDKIT_PROGRESS=tty
export DOCKER_BUILDKIT=1

.PHONY: gcf local


gcf:
	gcloud functions deploy test-de-mdp-gcf \
		--project test-mdp-de \
		--region us-east1 \
		--ingress-settings internal-only \
		--egress-settings private-ranges-only \
		--source . \
		--env-vars-file gcf/.env.yml \
		--ignore-file gcf/.gcloudignore \
		--runtime python39 \
		--trigger-resource input \
		--trigger-event google.storage.object.finalize \
		--entry-point main \
		--max-instances 1 \
		--memory 4g \
		--timeout 540s \
		--no-retry \
		--service-account test-de-mdp-gsa@test-mdp-de.iam.gserviceaccount.com


local:
	docker build \
		-f local/Dockerfile \
		-t test-de-mdp-gsa/local \
		--no-cache=false \
		.
	docker run \
		-it --rm \
		-v "$(PWD)":/app:rw \
		test-de-mdp-gsa/local

