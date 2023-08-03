## Plex Sync

Syncs Plex watchlist with Radarr/Sonarr 

## Environment Variables

| Variable      | Default        | Required |
|---------------|----------------|----------|
| PLEX_TOKEN    | -              | *        |
| RADARR_TOKEN  | -              | *        |
| RADARR_URL    | localhost:7878 |          |
| SONARR_TOKEN  | -              | *        |
| SONARR_URL    | localhost:8989 |          |
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
          RADARR_URL: http://radarr:7878
          SONARR_TOKEN: xxxxxxxxx
          SONARR_URL: http://sonarr:8989
      restart: unless-stopped

```