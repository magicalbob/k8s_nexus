k8s_nexus
=========

nexus3 in kubernetes.

`install-nexus.sh` sets it up. It you supply `kind` as the first argument to it, it will `kind` as the k8s cluster.

The `./bin` directory contains some python3 scripts for deleting and creating repos, content selectors, privileges, roles and users. These python scripts use several environment variables to specify varied inputs. The create_repos.py relies on individual json files in a directory to define each repo. The `prepare_json.py` makes these json files from output from:
```
	curl -vo ~/Downloads/nexus.dev.repos.json \
		'https://admin:????@{nexus_url}/service/rest/beta/repositories'
```
