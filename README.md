## Plex Sync

Syncs Plex watchlist with Radarr/Sonarr 

## Environment Variables

| Variable      | Default        | Required |
|---------------|----------------|----------|
| PLEX_TOKEN    | -              | *        |
| RADARR_TOKEN  | -              | *        |
| RADARR_HOST   | localhost:7878 |          |
| SONARR_TOKEN  | -              | *        |
| SONARR_HOST   | localhost:8989 |          |
| TIME_INTERVAL | 60             |          |

## Run
```bash
# export env vars and then run
python main.py
```


# Docker compose

```yaml
version: '3'

services:
    plexsync:
      image: eben0/plexsync:latest
      environment:
          PLEX_TOKEN: xxxxxxxxx
          RADARR_TOKEN: xxxxxxxxx
          RADARR_HOST: radarr:7878
          SONARR_TOKEN: xxxxxxxxx
          SONARR_HOST: sonarr:8989
      restart: unless-stopped

```