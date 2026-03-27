# Vidsrc.cc Decryptor

Simple FastAPI backend for extracting final stream data from `vidsrc.cc`.

This project resolves the full chain and returns the final JSON with:

- `sources`
- `tracks`
- `encrypted`
- provider response details

It supports:

- Movies
- TV series
- Anime

## What This Project Does

You send one request to the API.

The backend then:

1. Opens the Vidsrc embed page
2. Extracts the page variables needed for the request
3. Generates the correct `vrf`
4. Resolves the server list
5. Resolves the final provider page
6. Extracts the final stream payload

The response usually includes direct HLS links in `sources`.

## Features

- Movie support
- TV support
- Anime support
- Working `vrf` generation
- Stream source extraction
- Subtitle track extraction
- Clean docs page at `/`
- Backend-only flow

## Project Files

- `api.py` - FastAPI app and docs page
- `extractor.py` - main extraction logic
- `vrf_generator.py` - standalone VRF generator
- `streameee_embed1.min.js` - local reference file used during reversing

## Requirements

- Python 3.11+ recommended

Python packages:

- `fastapi`
- `uvicorn`
- `httpx`
- `beautifulsoup4`
- `cryptography`

## Install

```bash
pip install fastapi uvicorn httpx beautifulsoup4 cryptography
```

## Run

```bash
python api.py
```

Default server:

```text
http://127.0.0.1:5050
```

## API Endpoint

### `GET /extract`

Query params:

- `id` - title ID
- `type` - `movie`, `tv`, or `anime`
- `season` - required for TV
- `episode` - required for TV and anime
- `lang` - anime language, usually `sub` or `dub`

## ID Rules

### Movies

Movies can use:

- TMDb ID
- IMDb ID

Examples:

- `385687`
- `559969`
- `tt9243946`

### TV Series

TV can use:

- TMDb ID
- IMDb ID

Examples:

- `60735`
- `1399`
- `tt0944947`

### Anime

Anime has two common ID styles here:

- AniList anime ID: use `ani` before the AniList number
- MAL ID: use the plain MAL number only

Examples:

- AniList: `ani178005`
- MAL: `52991`

Simple rule:

- AniList -> `ani<anilist_id>`
- MAL -> `<mal_id>`

## Example Requests

### Movie with TMDb ID

```text
/extract?id=385687&type=movie
```

### Movie with IMDb ID

```text
/extract?id=tt9243946&type=movie
```

### TV with TMDb ID

```text
/extract?id=60735&type=tv&season=1&episode=1
```

### TV with IMDb ID

```text
/extract?id=tt0944947&type=tv&season=1&episode=1
```

### Anime with AniList ID

```text
/extract?id=ani178005&type=anime&episode=1&lang=sub
```

### Anime with MAL ID

```text
/extract?id=52991&type=anime&episode=1&lang=sub
```

### Anime dub example

```text
/extract?id=21&type=anime&episode=1&lang=dub
```

## Example Response Shape

```json
{
  "sources": [
    {
      "file": "https://...m3u8",
      "type": "hls"
    }
  ],
  "tracks": [
    {
      "file": "https://...vtt",
      "label": "English",
      "kind": "captions",
      "default": true
    }
  ],
  "encrypted": false
}
```

## Response Fields

- `sources` - playable stream URLs
- `tracks` - subtitle files
- `type` - stream type, usually `hls`
- `encrypted` - whether the final payload is still encrypted

## Notes

- Anime may return different paths depending on `lang=sub` or `lang=dub`
- TV requires both `season` and `episode`
- Movies only need `id` and `type=movie`
- Some providers change behavior over time, so extraction logic may need updates later

## VRF

This repo includes a working VRF generator in:

- `vrf_generator.py`

That script is useful if you want to test the Vidsrc request flow separately from the API.

## Local Docs UI

After starting the server, open:

```text
http://127.0.0.1:5050/
```

The homepage includes:

- quick test buttons
- movie examples
- TV examples
- anime examples
- ID rules

## GitHub

Repository:

```text
https://github.com/walterwhite-69/Vidsrc.cc-Decryptor
```

## Developer

Walter
