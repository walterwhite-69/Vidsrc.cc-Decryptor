from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from extractor import VidsrcExtractor
import uvicorn
from fastapi.exceptions import HTTPException as FastAPIHTTPException

app = FastAPI(title="Vidsrc M3U8 API", description="Automated stream extraction for vidsrc.cc")
extractor = VidsrcExtractor()

HTML_DOCS = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vidsrc Extractor API | Documentation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #080608;
            --bg-2: #170c12;
            --card-bg: rgba(255, 255, 255, 0.045);
            --card-border: rgba(255, 255, 255, 0.1);
            --accent-aqua: #7ef7ef;
            --accent-red: #ff6b7a;
            --accent-gold: #ffd6a5;
            --glow-aqua: rgba(126, 247, 239, 0.25);
            --glow-red: rgba(255, 107, 122, 0.25);
            --text-main: #f6efef;
            --text-dim: #c7afb6;
            --font: 'Outfit', sans-serif;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; -webkit-font-smoothing: antialiased; }

        body {
            background-color: var(--bg);
            background-image: 
                radial-gradient(circle at 18% 18%, rgba(126, 247, 239, 0.12) 0%, transparent 36%),
                radial-gradient(circle at 82% 22%, rgba(255, 107, 122, 0.14) 0%, transparent 34%),
                radial-gradient(circle at 70% 78%, rgba(255, 214, 165, 0.08) 0%, transparent 38%),
                linear-gradient(180deg, var(--bg) 0%, var(--bg-2) 100%);
            color: var(--text-main);
            font-family: var(--font);
            line-height: 1.6;
            overflow-x: hidden;
            min-height: 100vh;
        }

        .container { max-width: 1000px; margin: 0 auto; padding: 80px 20px; }

        header { text-align: center; margin-bottom: 80px; perspective: 1000px; }

        h1 {
            font-size: 4rem;
            font-weight: 800;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--accent-aqua) 0%, #fff 40%, var(--accent-red) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5));
            transform: translateZ(50px);
        }

        .tagline { color: var(--accent-gold); font-size: 1rem; letter-spacing: 2px; text-transform: uppercase; }
        .lead { max-width: 760px; margin: 18px auto 0; color: var(--text-dim); }
        .lead strong { color: var(--accent-aqua); font-weight: 600; }

        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; perspective: 2000px; }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 40px;
            backdrop-filter: blur(15px);
            transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
            transform-style: preserve-3d;
            position: relative;
            cursor: default;
        }

        .card:hover {
            transform: translateY(-10px) rotateX(5deg) rotateY(5deg);
            border-color: var(--accent-red);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.35), 0 0 18px var(--glow-red);
        }

        .card h2 { font-size: 1.8rem; margin-bottom: 15px; color: var(--accent-aqua); transform: translateZ(30px); }
        .card p { color: var(--text-dim); margin-bottom: 25px; transform: translateZ(20px); }

        .endpoint-box {
            background: rgba(0, 0, 0, 0.28);
            border-radius: 12px;
            padding: 15px;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            margin-bottom: 14px;
            border-left: 3px solid var(--accent-aqua);
            transform: translateZ(10px);
            word-break: break-all;
        }

        .endpoint-note {
            color: var(--text-dim);
            font-size: 0.95rem;
            margin-bottom: 18px;
        }

        .btn {
            display: inline-block;
            padding: 12px 24px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent-aqua) 0%, var(--accent-red) 100%);
            color: #16080c;
            text-decoration: none;
            font-weight: 700;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            transform: translateZ(40px);
            box-shadow: 0 8px 24px rgba(255, 107, 122, 0.18);
        }

        .btn:hover { transform: translateZ(50px) scale(1.05); filter: brightness(1.2); }

        .section {
            margin-top: 72px;
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 34px;
            backdrop-filter: blur(12px);
        }

        .section h2 {
            color: var(--accent-gold);
            font-size: 1.5rem;
            margin-bottom: 16px;
        }

        .steps, .example-list {
            display: grid;
            gap: 14px;
        }

        .steps p, .example-list p {
            color: var(--text-dim);
        }

        .example-row {
            display: flex;
            gap: 12px;
            align-items: center;
        }

        .example-row .endpoint-box {
            flex: 1;
            margin-bottom: 0;
        }

        .mini-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 92px;
            padding: 11px 14px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: var(--text-main);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.25s ease;
        }

        .mini-btn:hover {
            border-color: var(--accent-aqua);
            color: var(--accent-aqua);
            transform: translateY(-1px);
            box-shadow: 0 8px 18px var(--glow-aqua);
        }

        .mini {
            color: var(--text-dim);
            font-size: 0.95rem;
            margin-top: 8px;
        }

        .footer-signoff {
            margin-top: 88px;
            text-align: center;
        }

        .developer-badge {
            display: inline-block;
            padding: 10px 18px;
            border-radius: 999px;
            background: linear-gradient(135deg, rgba(126, 247, 239, 0.12) 0%, rgba(255, 107, 122, 0.14) 100%);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: var(--text-main);
            font-size: 0.95rem;
            font-weight: 700;
            letter-spacing: 0.4px;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
        }

        .developer-badge span {
            color: var(--accent-gold);
        }

        .footer-copy {
            margin-top: 18px;
            color: var(--text-dim);
            font-size: 0.9rem;
        }

        .floating-bits { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
        .bit {
            position: absolute;
            background: var(--accent-aqua);
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.15;
            animation: float 20s infinite alternate;
        }

        @keyframes float { 0% { transform: translate(0, 0); } 100% { transform: translate(100px, 100px); } }
        @media (max-width: 768px) {
            h1 { font-size: 2.5rem; }
            .grid { grid-template-columns: 1fr; }
            .example-row { flex-direction: column; align-items: stretch; }
            .mini-btn { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="floating-bits">
        <div class="bit" style="width: 400px; height: 400px; top: -100px; left: -100px;"></div>
        <div class="bit" style="width: 300px; height: 300px; bottom: -50px; right: -50px; background: #ff6b7a;"></div>
    </div>

    <div class="container">
        <header>
            <div class="tagline">Fast Vidsrc Extractor</div>
            <h1>Vidsrc Pro</h1>
            <p class="lead">Simple backend-only extraction for <strong>movies</strong>, <strong>TV</strong>, and <strong>anime</strong>. Open one endpoint, and the API returns stream sources, subtitle tracks, and provider data.</p>
        </header>

        <div class="grid">
            <div class="card">
                <h2>🎬 Movies</h2>
                <p>Use a movie ID and get the final stream response. Good for quick testing and direct playback tools.</p>
                <div class="endpoint-box">GET /extract?id=385687&type=movie</div>
                <div class="endpoint-note">Example movie: Fast X. Returns `sources`, `tracks`, and stream info.</div>
                <a href="/extract?id=385687&type=movie" target="_blank" class="btn">Test Endpoint</a>
            </div>

            <div class="card">
                <h2>📺 TV Series</h2>
                <p>Pass the show ID, season, and episode. The backend handles the episode route and final source lookup.</p>
                <div class="endpoint-box">GET /extract?id=60735&type=tv&season=1&episode=1</div>
                <div class="endpoint-note">Example TV: The Flash S1E1.</div>
                <a href="/extract?id=60735&type=tv&season=1&episode=1" target="_blank" class="btn">Test Endpoint</a>
            </div>

            <div class="card">
                <h2>⛩️ Anime</h2>
                <p>Anime supports episode selection and language mode. Use `lang=sub` or `lang=dub` when available.</p>
                <div class="endpoint-box">GET /extract?id=ani178005&type=anime&episode=1</div>
                <div class="endpoint-note">Example anime: episode 1 with sub mode.</div>
                <a href="/extract?id=ani178005&type=anime&episode=1" target="_blank" class="btn">Test Endpoint</a>
            </div>
        </div>

        <section class="section">
            <h2>How It Works</h2>
            <div class="steps">
                <p><strong>1.</strong> Open `/extract` with the right query values.</p>
                <p><strong>2.</strong> The backend visits the provider pages, resolves the final source route, and returns JSON.</p>
                <p><strong>3.</strong> Use the `sources[0].file` URL as the main HLS stream. Subtitle files will be in `tracks`.</p>
            </div>
            <p class="mini">If a title has more than one language or source path, the backend still keeps the response shape simple.</p>
        </section>

        <section class="section">
            <h2>More Examples</h2>
            <div class="example-list">
                <div>
                    <div class="example-row">
                        <div class="endpoint-box">GET /extract?id=385687&type=movie</div>
                        <a href="/extract?id=385687&type=movie" target="_blank" class="mini-btn">Open</a>
                    </div>
                    <p>Movie using a TMDb ID. Example: Fast X.</p>
                </div>
                <div>
                    <div class="example-row">
                        <div class="endpoint-box">GET /extract?id=21&type=anime&episode=1&lang=sub</div>
                        <a href="/extract?id=21&type=anime&episode=1&lang=sub" target="_blank" class="mini-btn">Open</a>
                    </div>
                    <p>Anime example with a plain numeric ID and sub mode.</p>
                </div>
                <div>
                    <div class="example-row">
                        <div class="endpoint-box">GET /extract?id=21&type=anime&episode=1&lang=dub</div>
                        <a href="/extract?id=21&type=anime&episode=1&lang=dub" target="_blank" class="mini-btn">Open</a>
                    </div>
                    <p>Same anime endpoint, but asking for dub when that version exists.</p>
                </div>
                <div>
                    <div class="example-row">
                        <div class="endpoint-box">GET /extract?id=1399&type=tv&season=1&episode=1</div>
                        <a href="/extract?id=1399&type=tv&season=1&episode=1" target="_blank" class="mini-btn">Open</a>
                    </div>
                    <p>TV example with season and episode values.</p>
                </div>
                <div>
                    <div class="example-row">
                        <div class="endpoint-box">GET /extract?id=559969&type=movie</div>
                        <a href="/extract?id=559969&type=movie" target="_blank" class="mini-btn">Open</a>
                    </div>
                    <p>Movie example for a different title, useful when checking another live source path.</p>
                </div>
                <div>
                    <div class="example-row">
                        <div class="endpoint-box">GET /extract?id=tt9243946&type=movie</div>
                        <a href="/extract?id=tt9243946&type=movie" target="_blank" class="mini-btn">Open</a>
                    </div>
                    <p>Movie using an IMDb ID instead of a TMDb ID.</p>
                </div>
                <div>
                    <div class="example-row">
                        <div class="endpoint-box">GET /extract?id=tt0944947&type=tv&season=1&episode=1</div>
                        <a href="/extract?id=tt0944947&type=tv&season=1&episode=1" target="_blank" class="mini-btn">Open</a>
                    </div>
                    <p>TV example using an IMDb ID with season and episode.</p>
                </div>
            </div>
        </section>

        <section class="section">
            <h2>Anime ID Rules</h2>
            <div class="steps">
                <p><strong>AniList anime ID:</strong> add <code>ani</code> before the number. Example: <code>ani178005</code>.</p>
                <p><strong>MyAnimeList ID:</strong> use the plain MAL number only. Example: <code>52991</code>.</p>
                <p><strong>Anime type:</strong> always use <code>type=anime</code> and include <code>episode</code>.</p>
                <p><strong>Language:</strong> use <code>lang=sub</code> or <code>lang=dub</code>.</p>
            </div>
            <div class="example-list" style="margin-top:16px;">
                <div>
                    <div class="example-row">
                        <div class="endpoint-box">GET /extract?id=ani178005&type=anime&episode=1&lang=sub</div>
                        <a href="/extract?id=ani178005&type=anime&episode=1&lang=sub" target="_blank" class="mini-btn">Open</a>
                    </div>
                    <p>AniList anime ID example.</p>
                </div>
                <div>
                    <div class="example-row">
                        <div class="endpoint-box">GET /extract?id=52991&type=anime&episode=1&lang=sub</div>
                        <a href="/extract?id=52991&type=anime&episode=1&lang=sub" target="_blank" class="mini-btn">Open</a>
                    </div>
                    <p>MAL anime ID example with no <code>ani</code> prefix.</p>
                </div>
            </div>
        </section>

        <section class="section">
            <h2>Response Notes</h2>
            <div class="steps">
                <p><strong>`sources`</strong> contains the playable stream links.</p>
                <p><strong>`tracks`</strong> contains subtitle files and labels.</p>
                <p><strong>`type`</strong> inside a source usually tells you if it is `hls`.</p>
                <p><strong>`encrypted`</strong> shows whether the final source payload is already plain or still protected.</p>
            </div>
        </section>

        <section class="footer-signoff">
            <div class="developer-badge">Developer: <span>Walter</span></div>
            <p class="footer-copy">
                Backend-only stream extraction with simple endpoints.<br>
                &copy; 2026 Vidsrc Extractor Dashboard
            </p>
        </section>
    </div>

    <script>
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mousemove', e => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = `perspective(1000px) rotateX(0) rotateY(0) translateY(0)`;
            });
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def root():
    return HTML_DOCS

@app.get("/extract")
def extract(
    id: str,
    type: str = Query("movie", enum=["movie", "tv", "anime"]),
    season: str = None,
    episode: str = None,
    lang: str = "sub"
):
    try:
        is_tv = type == "tv"
        is_anime = type == "anime"
        
        result = extractor.get_stream(
            id=id,
            is_tv=is_tv,
            is_anime=is_anime,
            season=season,
            episode=episode,
            sub_or_dub=lang
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Could not extract sources")
            
        return result
    except FastAPIHTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5050)
