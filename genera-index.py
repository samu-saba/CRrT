import os
from urllib.parse import quote

# ==========================================
# CONFIGURAZIONE COMUNE E DATI DEL REPO
# ==========================================
owner = "samu-saba"
repo = "CRrT"
branch = "main"

# Definizione delle tre sezioni da elaborare
sections = [
    {
        "title": "Sezione Soprani",
        "code": "Soprani",
        "storage_key": "rns_soprani_playlists_v1",
        "local_path": r"F:\Progetti Git\CRrT\Soprani",
        "output_file": r"F:\Progetti Git\CRrT\Soprani.index.html"
    },
    {
        "title": "Sezione Tenori",
        "code": "Tenori",
        "storage_key": "rns_tenori_playlists_v1",
        "local_path": r"F:\Progetti Git\CRrT\Tenori",
        "output_file": r"F:\Progetti Git\CRrT\Tenori.index.html"
    },
    {
        "title": "Sezione Contralti",
        "code": "contralti",
        "storage_key": "rns_contralti_playlists_v1",
        "local_path": r"F:\Progetti Git\CRrT\contralti",
        "output_file": r"F:\Progetti Git\CRrT\contralti.index.html"
    }
]

# ==========================================
# GENERAZIONE CICLICA DEGLI INDEX
# ==========================================
for sec in sections:
    section_title = sec["title"]
    section_code = sec["code"]
    storage_key = sec["storage_key"]
    local_base_path = sec["local_path"]
    output_path = sec["output_file"]

    print(f"Elaborazione in corso per: {section_title}...")

    # Costruzione dinamica dell'HTML di base
    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>Archivio Studio Permanente - {section_title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #ffffff; color: #222222; }}
        header {{ margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #1a365d; }}
        h1 {{ margin: 0 0 5px 0; color: #1a365d; font-size: 1.8rem; }}
        p.subtitle {{ margin: 0; color: #555555; font-size: 0.95rem; }}

        /* Navigazione a Schede */
        .tabs {{ display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
        .tab-btn {{
            padding: 10px 18px;
            font-size: 1rem;
            font-weight: bold;
            border: 2px solid #1a365d;
            border-radius: 6px;
            background-color: #ffffff;
            color: #1a365d;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .tab-btn.active {{ background-color: #1a365d; color: #ffffff; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        /* Barra di ricerca */
        .search-container {{ margin-bottom: 25px; }}
        #search-input {{ width: 100%; padding: 12px 15px; font-size: 1rem; border: 2px solid #cccccc; border-radius: 6px; outline: none; box-sizing: border-box; }}
        #search-input:focus {{ border-color: #1a365d; }}

        /* Sezioni e Tracce */
        .section {{ margin-bottom: 20px; border: 1px solid #cccccc; border-radius: 6px; overflow: hidden; background-color: #fafafa; }}
        details {{ width: 100%; }}
        summary {{ background-color: #1a365d; color: #ffffff; font-size: 1.2rem; font-weight: bold; padding: 15px 20px; cursor: pointer; user-select: none; list-style: none; }}
        summary::-webkit-details-marker {{ display: none; }}
        summary::after {{ content: ' ▼'; font-size: 0.9rem; float: right; transition: transform 0.2s; }}
        details[open] summary::after {{ transform: rotate(180deg); }}
        .section-content {{ padding: 20px; background-color: #ffffff; border-top: 1px solid #cccccc; }}
        
        .track {{ margin-bottom: 15px; display: flex; flex-direction: column; padding-bottom: 12px; border-bottom: 1px solid #eeeeee; }}
        .track:last-child {{ margin-bottom: 0; border-bottom: none; padding-bottom: 0; }}
        .track-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; gap: 10px; }}
        .track-title {{ font-weight: bold; color: #333333; font-size: 0.95rem; word-break: break-word; }}
        audio {{ width: 100%; height: 40px; }}

        /* Pulsanti Playlist */
        .add-btn {{
            background-color: #edf2f7;
            color: #1a365d;
            border: 1px solid #cbd5e0;
            border-radius: 4px;
            padding: 5px 10px;
            font-size: 0.85rem;
            font-weight: bold;
            cursor: pointer;
            white-space: nowrap;
            transition: background-color 0.2s;
        }}
        .add-btn:hover {{ background-color: #e2e8f0; }}
        .add-btn.added {{ background-color: #2f855a; color: #ffffff; border-color: #2f855a; }}

        /* Area Gestione Playlist */
        .playlist-controls {{
            background-color: #f7fafc;
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }}
        .playlist-controls select, .playlist-controls input {{
            padding: 8px 12px;
            font-size: 0.95rem;
            border: 1px solid #cbd5e0;
            border-radius: 4px;
        }}
        .playlist-controls select {{ flex: 1; min-width: 180px; font-weight: bold; color: #1a365d; }}
        .btn-action {{
            padding: 8px 14px;
            font-size: 0.9rem;
            font-weight: bold;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            background-color: #1a365d;
            color: #ffffff;
        }}
        .btn-action.danger {{ background-color: #c53030; }}
        .btn-action.secondary {{ background-color: #4a5568; }}
        
        .pl-item-actions {{ display: flex; gap: 5px; }}
        .pl-move-btn {{
            background: #edf2f7;
            border: 1px solid #cbd5e0;
            border-radius: 4px;
            padding: 4px 8px;
            cursor: pointer;
            font-weight: bold;
        }}
        .pl-remove-btn {{
            background: #fed7d7;
            color: #9b2c2c;
            border: 1px solid #feb2b2;
            border-radius: 4px;
            padding: 4px 8px;
            cursor: pointer;
            font-weight: bold;
        }}
        .empty-msg {{ text-align: center; color: #718096; padding: 30px 10px; font-style: italic; }}
        .folder-badge {{ font-size: 0.8rem; color: #718096; font-weight: normal; display: block; margin-bottom: 4px; }}
    </style>
</head>
<body>
    <header>
        <h1>Archivio Studio Permanente – {section_title}</h1>
        <p class="subtitle">Libreria completa e Playlist personalizzate – Riproduzione sequenziale continua</p>
    </header>

    <!-- SCHEDE DI NAVIGAZIONE -->
    <div class="tabs">
        <button class="tab-btn active" data-tab="library-tab">📚 Libreria Brani</button>
        <button class="tab-btn" data-tab="playlist-tab">🎵 Le Mie Playlist (<span id="pl-count">0</span>)</button>
    </div>

    <!-- SCHEDA 1: LIBRERIA -->
    <div id="library-tab" class="tab-content active">
        <div class="search-container">
            <input type="text" id="search-input" placeholder="🔍 Cerca un brano o una cartella...">
        </div>
        <div id="playlist-container">
"""

    if not os.path.exists(local_base_path):
        print(f"  [ATTENZIONE] Il percorso locale '{local_base_path}' non esiste. Verrà generato un index vuoto per questa sezione.")
    else:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        for root, dirs, files in os.walk(local_base_path):
            dirs.sort()
            files.sort()
            audio_files = [f for f in files if f.lower().endswith(('.mp3', '.m4a', '.wav'))]
            if audio_files:
                folder_name = os.path.basename(root)
                tracks_html = ""
                for file_name in audio_files:
                    rel_path = os.path.relpath(os.path.join(root, file_name), local_base_path).replace("\\", "/")
                    encoded_rel_path = "/".join([quote(p) for p in rel_path.split("/")])
                    file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{section_code}/{encoded_rel_path}"
                    
                    tracks_html += f"""
                    <div class="track" data-title="{file_name.lower()}" data-folder="{folder_name.lower()}">
                        <span class="track-title">{file_name}</span>
                        <audio controls controlsList="nodownload" class="global-audio" src="{file_url}"></audio>
                    </div>"""
                        
                html_content += f"""
        <div class="section" data-section-name="{folder_name.lower()}">
            <details>
                <summary>📁 {folder_name}</summary>
                <div class="section-content">{tracks_html}
                </div>
            </details>
        </div>"""

    html_content += f"""
        </div>
    </div>
        
    <!-- SCHEDA 2: LE MIE PLAYLIST -->
    <div id="playlist-tab" class="tab-content">
        <div class="playlist-controls">
            <select id="playlist-select" title="Seleziona playlist"></select>
            <button class="btn-action" id="new-playlist-btn">+ Nuova</button>
            <button class="btn-action secondary" id="rename-playlist-btn">Rinomina</button>
            <button class="btn-action danger" id="delete-playlist-btn">Elimina</button>
        </div>

        <div id="custom-playlist-tracks" class="section-content" style="border: 1px solid #cccccc; border-radius: 6px;">
            <!-- I brani della playlist selezionata appariranno qui -->
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const STORAGE_KEY = '{storage_key}';
            let state = JSON.parse(localStorage.getItem(STORAGE_KEY)) || {{
                activePlaylist: 'Scaletta Principale',
                playlists: {{ 'Scaletta Principale': [] }}
            }};

            const tabBtns = document.querySelectorAll('.tab-btn');
            const tabContents = document.querySelectorAll('.tab-content');
            const playlistSelect = document.getElementById('playlist-select');
            const customTracksContainer = document.getElementById('custom-playlist-tracks');
            const plCountSpan = document.getElementById('pl-count');

            function saveState() {{
                localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
                updateUI();
            }}

            tabBtns.forEach(btn => {{
                btn.addEventListener('click', () => {{
                    document.querySelectorAll('audio').forEach(a => a.pause());
                    tabBtns.forEach(b => b.classList.remove('active'));
                    tabContents.forEach(c => c.classList.remove('active'));
                    btn.classList.add('active');
                    document.getElementById(btn.getAttribute('data-tab')).classList.add('active');
                }});
            }});

            const libraryTracks = document.querySelectorAll('#playlist-container .track');
            libraryTracks.forEach(track => {{
                const titleEl = track.querySelector('.track-title');
                const audioEl = track.querySelector('audio');
                const sectionEl = track.closest('.section');
                const folderName = sectionEl ? sectionEl.getAttribute('data-section-name') : '';
                const titleText = titleEl.textContent.trim();
                const srcUrl = audioEl.getAttribute('src');

                const headerDiv = document.createElement('div');
                headerDiv.className = 'track-header';
                track.insertBefore(headerDiv, titleEl);
                headerDiv.appendChild(titleEl);

                const addBtn = document.createElement('button');
                addBtn.className = 'add-btn';
                addBtn.setAttribute('data-src', srcUrl);
                addBtn.textContent = '+ Playlist';

                addBtn.addEventListener('click', () => {{
                    const currentList = state.playlists[state.activePlaylist];
                    const existingIndex = currentList.findIndex(item => item.src === srcUrl);

                    if (existingIndex === -1) {{
                        currentList.push({{ title: titleText, src: srcUrl, folder: folderName }});
                    }} else {{
                        currentList.splice(existingIndex, 1);
                    }}
                    saveState();
                }});

                headerDiv.appendChild(addBtn);
            }});

            document.getElementById('new-playlist-btn').addEventListener('click', () => {{
                const name = prompt('Nome della nuova playlist:');
                if (name && name.trim()) {{
                    const cleanName = name.trim();
                    if (!state.playlists[cleanName]) {{
                        state.playlists[cleanName] = [];
                    }}
                    state.activePlaylist = cleanName;
                    saveState();
                }}
            }});

            document.getElementById('rename-playlist-btn').addEventListener('click', () => {{
                const oldName = state.activePlaylist;
                const newName = prompt('Nuovo nome per "' + oldName + '":', oldName);
                if (newName && newName.trim() && newName.trim() !== oldName) {{
                    const cleanName = newName.trim();
                    state.playlists[cleanName] = state.playlists[oldName];
                    delete state.playlists[oldName];
                    state.activePlaylist = cleanName;
                    saveState();
                }}
            }});

            document.getElementById('delete-playlist-btn').addEventListener('click', () => {{
                const keys = Object.keys(state.playlists);
                if (keys.length <= 1) {{
                    alert('Deve esserci almeno una playlist. Puoi svuotarla o rinominarla.');
                    return;
                }}
                if (confirm('Vuoi davvero eliminare la playlist "' + state.activePlaylist + '"?')) {{
                    delete state.playlists[state.activePlaylist];
                    state.activePlaylist = Object.keys(state.playlists)[0];
                    saveState();
                }}
            }});

            playlistSelect.addEventListener('change', (e) => {{
                state.activePlaylist = e.target.value;
                saveState();
            }});

            function attachGlobalAudioHandlers() {{
                const allAudios = document.querySelectorAll('audio');
                allAudios.forEach((audio) => {{
                    // Evita di duplicare i listener se già presenti
                    if (audio.dataset.handled === "true") return;
                    audio.dataset.handled = "true";

                    audio.addEventListener('contextmenu', e => e.preventDefault());
                    
                    audio.addEventListener('play', () => {{
                        document.querySelectorAll('audio').forEach(o => {{ 
                            if (o !== audio) o.pause(); 
                        }});
                    }});

                    audio.addEventListener('ended', () => {{
                        // Gestione riproduzione continua sequenziale
                        const currentTabContent = audio.closest('.tab-content');
                        if (!currentTabContent) return;
                        const audiosInTab = Array.from(currentTabContent.querySelectorAll('audio'));
                        const currentIdx = audiosInTab.indexOf(audio);
                        
                        if (currentIdx !== -1) {{
                            for (let i = currentIdx + 1; i < audiosInTab.length; i++) {{
                                const nextAudio = audiosInTab[i];
                                const parentTrack = nextAudio.closest('.track');
                                if (!parentTrack || parentTrack.style.display !== 'none') {{
                                    nextAudio.play();
                                    break;
                                }}
                            }}
                        }}
                    }});
                }});
            }}

            function updateUI() {{
                const currentList = state.playlists[state.activePlaylist] || [];
                plCountSpan.textContent = currentList.length;

                playlistSelect.innerHTML = '';
                Object.keys(state.playlists).forEach(plName => {{
                    const opt = document.createElement('option');
                    opt.value = plName;
                    opt.textContent = `${{plName}} (${{state.playlists[plName].length}} brani)`;
                    if (plName === state.activePlaylist) opt.selected = true;
                    playlistSelect.appendChild(opt);
                }});

                const activeSrcSet = new Set(currentList.map(i => i.src));
                document.querySelectorAll('.add-btn').forEach(btn => {{
                    if (activeSrcSet.has(btn.getAttribute('data-src'))) {{
                        btn.classList.add('added');
                        btn.textContent = '✓ In Playlist';
                    }} else {{
                        btn.classList.remove('added');
                        btn.textContent = '+ Playlist';
                    }}
                }});

                renderCustomPlaylist();
            }}

            function renderCustomPlaylist() {{
                const currentList = state.playlists[state.activePlaylist] || [];
                customTracksContainer.innerHTML = '';

                if (currentList.length === 0) {{
                    customTracksContainer.innerHTML = `<div class="empty-msg">La playlist <strong>"${{state.activePlaylist}}"</strong> è vuota.<br>Vai nella scheda "Libreria Brani" e clicca su <strong>+ Playlist</strong> accanto ai canti che vuoi aggiungere.</div>`;
                    return;
                }}

                currentList.forEach((item, index) => {{
                    const trackDiv = document.createElement('div');
                    trackDiv.className = 'track';

                    trackDiv.innerHTML = `
                        <span class="folder-badge">📁 ${{item.folder}}</span>
                        <div class="track-header">
                            <span class="track-title">${{index + 1}}. ${{item.title}}</span>
                            <div class="pl-item-actions">
                                <button class="pl-move-btn" title="Sposta su" ${{index === 0 ? 'disabled' : ''}}>▲</button>
                                <button class="pl-move-btn" title="Sposta giù" ${{index === currentList.length - 1 ? 'disabled' : ''}}>▼</button>
                                <button class="pl-remove-btn" title="Rimuovi dalla playlist">✕</button>
                            </div>
                        </div>
                        <audio controls controlsList="nodownload" class="playlist-audio" src="${{item.src}}"></audio>
                    `;

                    const [btnUp, btnDown, btnRemove] = trackDiv.querySelectorAll('button');
                    btnUp.addEventListener('click', () => {{
                        if (index > 0) {{
                            [currentList[index - 1], currentList[index]] = [currentList[index], currentList[index - 1]];
                            saveState();
                        }}
                    }});
                    btnDown.addEventListener('click', () => {{
                        if (index < currentList.length - 1) {{
                            [currentList[index + 1], currentList[index]] = [currentList[index], currentList[index + 1]];
                            saveState();
                        }}
                    }});
                    btnRemove.addEventListener('click', () => {{
                        currentList.splice(index, 1);
                        saveState();
                    }});

                    customTracksContainer.appendChild(trackDiv);
                }});

                attachGlobalAudioHandlers();
            }}

            const searchInput = document.getElementById('search-input');
            const sections = document.querySelectorAll('#playlist-container .section');

            searchInput.addEventListener('input', (e) => {{
                const term = e.target.value.toLowerCase().trim();
                sections.forEach(section => {{
                    const sectionName = section.getAttribute('data-section-name') || '';
                    const tracks = section.querySelectorAll('.track');
                    let visibleCount = 0;

                    tracks.forEach(track => {{
                        const title = track.getAttribute('data-title') || '';
                        // Corrispondenza se il termine è nel nome del brano O nel nome della cartella
                        if (title.includes(term) || sectionName.includes(term)) {{
                            track.style.display = 'flex';
                            visibleCount++;
                        }} else {{
                            track.style.display = 'none';
                        }}
                    }});

                    const details = section.querySelector('details');
                    if (visibleCount > 0) {{
                        section.style.display = 'block';
                        if (term !== '') {{
                            details.setAttribute('open', 'open');
                        }}
                    }} else {{
                        section.style.display = 'none';
                    }}
                }});
            }});

            attachGlobalAudioHandlers();
            updateUI();
        }});
    </script>
</body>
</html>
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"  [OK] Generato con successo: {output_path}")

print("\nTutti gli index sono stati generati correttamente!")