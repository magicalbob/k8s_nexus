k8s_nexus
=========

nexus3 in kubernetes.

`install-nexus.sh` sets it up. It you supply `kind` as the first argument to it, it will `kind` as the k8s cluster.

The `./bin` directory contains some python3 scripts for deleting and creating repos. The creation relies on individual json files in the `./bin/repo_config` directory to define each repo. The `prepare_json.py` makes these json files from output from:
```
	curl -vo ~/Downloads/nexus.dev.repos.json \
		'https://admin:????@{nexus_url}/service/rest/beta/repositories'
```
`delete_repos.py` and `python_walk.py` rely on `NEXUS_USERNAME` and `NEXUS_PASSWORD` to provide authentication for the nexus at `NEXUS_HOST`.
