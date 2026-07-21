# Monitoring stack (Prometheus + Grafana)

This folder is meant to live inside the `japanese-duolingo-tracker` repo, alongside
`dockerfile` / `adam.py` at the repo root. That's not cosmetic - the `duolingo-exporter`
service's build context is `..` (the repo root), so this only builds correctly when this
folder stays a subfolder of that repo.

```
japanese-duolingo-tracker/
├── adam.py
├── dockerfile
├── requirements.txt
└── monitoring/
    ├── docker-compose.yml
    ├── prometheus/
    │   ├── prometheus.yml
    │   └── targets/
    │       ├── duolingo.yml
    │       └── _template.yml.example
    └── grafana/
        └── provisioning/
            └── datasources/
                └── datasource.yml
```

## Deploying via Portainer (git repo stack)

1. In Portainer: **Stacks → Add stack → Repository**
2. Repository URL: `https://github.com/AdamBeedell/japanese-duolingo-tracker.git`
3. Reference: `refs/heads/main` (or whatever branch you push this to)
4. Compose path: `monitoring/docker-compose.yml`
5. Leave authentication blank (repo's public) unless you've made it private
6. Deploy the stack

Portainer clones the whole repo, so `dockerfile`/`adam.py` at the root are right there for
the build context, and the `prometheus/` and `grafana/` folders sit next to the compose file
as normal relative bind mounts - no manual file copying onto the ZimaOS box needed for this
stack anymore.

**To pick up changes later** (new target file, edited dashboard provisioning, a change to
`adam.py` itself): push to the repo, then in Portainer either hit **Pull and redeploy** on
the stack, or enable the GitOps auto-update polling/webhook option when you create it.

## Adding something new to monitor

Same as before - drop a file in `prometheus/targets/` (copy `_template.yml.example`),
commit, push, redeploy. Prometheus itself also re-polls that folder every 30s once the
container's running, so for target-only changes you don't even need to touch the stack -
just make sure the new target's container is on `monitor-net`.

## Notes

- `GF_SECURITY_ADMIN_PASSWORD` is `changeme` in the compose file - change it before pushing
  if this repo is or might become public, or better, move it to a Portainer stack
  environment variable instead of hardcoding it.
- If ZimaOS's `/root` is read-only (it was, last we checked), set `DOCKER_CONFIG` to a
  writable path before Portainer/Docker tries to build - Portainer itself usually isn't
  affected since it runs its own build process inside its container, but worth knowing if
  you still build from the ZimaOS CLI directly for anything.
