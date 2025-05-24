This preps a prometheus agent to export stats on a user

You'll need to connect the container to the nearby prometheus/grafana containers with

docker network connect monitor-net duolingo-exporter

Also may need to change the prometheus.yml

