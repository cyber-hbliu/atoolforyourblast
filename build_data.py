# -*- coding: utf-8 -*-
"""Build data.js for the Sustain-Release year twelve tool (Sep 10-13, 2026).

Same method as the Making Time tool, adapted for a festival that publishes
set times: entries are BILLED SETS (b2bs stay one unit — that's what you
schedule), and SETTIMES is fully populated from the official daily timetable.

Groups: T techno - E electro - J dnb/jungle/breaks/bass - H house -
        A ambient/experimental (DJs) - M downtempo/new age/ethereal -
        B bands. Blanks mean unknown, not none.

Times: festival days run past midnight ("12AM", "3-6AM" belong to the billed
day). Minutes are counted from noon of the billed day; any clock time before
noon rolls +24h. Missing end times are derived from the next set on the same
stage; closers keep their published ranges.
"""
import json

GROUPMAP = {'T': 'techno', 'E': 'electro', 'J': 'jungle', 'H': 'house',
            'A': 'ambient', 'M': 'folk', 'B': 'bands'}

U = ("", None, "", [])
# name: (city, cc, groups, genres) — hand metadata, conservative
META = {
"Amelia Holt": ("New York", "US", "TE", ["electro", "techno"]),
"Andy Martin": ("", None, "T", ["techno"]),
"Aurora Halal": ("New York", "US", "T", ["techno", "trance"]),
"BASHKKA": ("Munich", "DE", "T", ["club", "techno"]),
"Byrell The Great": ("New York", "US", "J", ["ballroom", "vogue beats"]),
"Byron Yeates b2b S-candalo": ("Berlin", "DE", "T", ["trance", "progressive"]),
"CCL": ("Berlin / Seattle", "DE", "T", ["bass", "leftfield club"]),
"CCL b2b Yushh": ("Berlin / Bristol", "DE", "TJ", ["bass", "breaks"]),
"Como Se DJ": U,
"Cosmo": ("New York", "US", "H", ["house"]),
"D. Tiffany b2b Roza Terenzi": ("Vancouver / Berlin", "CA", "H", ["trance-house", "breaks"]),
"Deep Creep": ("New York", "US", "T", ["club"]),
"Denzel & Joni DJ": U,
"DJ Deadname b2b DJPT": U,
"DJ G b2b DJ'J": U,
"DJ Healthy b2b JP": ("New York", "US", "H", ["club", "house"]),
"DJ Maria. b2b DJ Nobu": ("Tokyo / Chiba", "JP", "T", ["techno"]),
"DJ Miss Parker": ("New York", "US", "J", ["breaks", "club"]),
"DJ Temporary": U,
"Downloadable Content": U,
"Eden Aurelius": ("", "CA", "H", ["house", "trance"]),
"Ekkel": U,
"Escaflowne": U,
"James K": ("New York", "US", "M", ["ambient", "downtempo", "ethereal"]),
"Joy Guidry": ("New York", "US", "A", ["bassoon", "free jazz", "ambient", "experimental"]),
"Kangding Ray presents Sirāt": ("Berlin", "DE", "T", ["techno", "industrial"]),
"Konduku & Garçon": ("Amsterdam / Rotterdam", "NL", "T", ["percussive techno"]),
"livwutang": ("New York", "US", "H", ["dub", "house"]),
"LYDO b2b Mama Snake": ("New York / Copenhagen", "US", "T", ["techno", "trance"]),
"mad miran": ("Amsterdam", "NL", "J", ["jungle", "eclectic"]),
"Mala": ("London", "GB", "J", ["dubstep", "dub"]),
"Malibu": ("Paris", "FR", "M", ["ambient", "new age", "ethereal"]),
"Matas": ("New York", "US", "T", ["techno"]),
"Mike Midnight": ("Philadelphia", "US", "A", ["ambient", "downtempo"]),
"Myles Mac & DJ Possum": U,
"Naone": ("Melbourne", "AU", "T", ["techno"]),
"Ogazón": ("", "ES", "T", ["minimal"]),
"OK EG": ("Melbourne", "AU", "TA", ["hypnotic techno"]),
"PAURRO": ("Mexico City", "MX", "H", ["house", "latin club"]),
"Powder": ("Tokyo", "JP", "H", ["house", "leftfield"]),
"Rhadoo": ("Bucharest", "RO", "T", ["minimal"]),
"Saia": U,
"Sandwell District": ("Berlin / UK", "DE", "T", ["techno", "industrial"]),
"Shaun J. Wright": ("Chicago", "US", "H", ["house", "vocal"]),
"SPF 50": U,
"Trickpony": ("Montréal", "CA", "M", ["trip hop", "downtempo"]),
"Verraco": ("Medellín", "CO", "T", ["techno", "bass"]),
}

LABELS = {
"Aurora Halal": "Mutual Dreaming", "Mala": "Deep Medi Musik",
"Rhadoo": "[a:rpia:r]", "Sandwell District": "Sandwell District",
"Trickpony": "Step Ball Chain", "Verraco": "TraTraTrax",
"D. Tiffany b2b Roza Terenzi": "Planet Euphorique",
"Kangding Ray presents Sirāt": "raster",
}

LIVE = {"Malibu", "Kangding Ray presents Sirāt", "James K", "SPF 50",
        "Trickpony", "OK EG", "Aurora Halal", "Joy Guidry"}

# (day, stage, start, end-or-None) — end None = derived from next set on stage
SETTIMES = {
"D. Tiffany b2b Roza Terenzi": ("Thu", "The Gym", "9PM", "3AM"),
"Escaflowne":            ("Thu", "The Grove", "7PM", None),
"Malibu":                ("Thu", "The Grove", "10PM", None),
"Kangding Ray presents Sirāt": ("Thu", "The Grove", "11PM", None),
"mad miran":             ("Thu", "The Grove", "12:30AM", "3AM"),

"Cosmo":                 ("Fri", "Lakeside", "1PM", "3:30PM"),
"Myles Mac & DJ Possum": ("Fri", "Lakeside", "3:30PM", "6:30PM"),
"DJ Deadname b2b DJPT":  ("Fri", "The Gym", "7:30PM", None),
"Byrell The Great":      ("Fri", "The Gym", "10PM", None),
"CCL b2b Yushh":         ("Fri", "The Gym", "12AM", None),
"Mala":                  ("Fri", "The Gym", "3AM", "6AM"),
"James K":               ("Fri", "The Grove", "6:30PM", None),
"Deep Creep":            ("Fri", "The Grove", "7:30PM", None),
"Ekkel":                 ("Fri", "The Grove", "9:30PM", None),
"Naone":                 ("Fri", "The Grove", "11:30PM", None),
"SPF 50":                ("Fri", "The Grove", "1:30AM", None),
"Andy Martin":           ("Fri", "The Grove", "2:30AM", None),
"Sandwell District":     ("Fri", "The Grove", "4:30AM", "7AM"),
"Como Se DJ":            ("Fri", "Bossa Lounge", "9PM", None),
"Trickpony":             ("Fri", "Bossa Lounge", "12AM", None),
"Amelia Holt":           ("Fri", "Bossa Lounge", "1AM", None),
"Eden Aurelius":         ("Fri", "Bossa Lounge", "3AM", None),
"DJ G b2b DJ'J":         ("Fri", "Bossa Lounge", "5AM", "8AM"),

"Saia":                  ("Sat", "La Noche Pool Party", "1PM", None),
"PAURRO":                ("Sat", "La Noche Pool Party", "3PM", None),
"Byron Yeates b2b S-candalo": ("Sat", "La Noche Pool Party", "5PM", "8PM"),
"Downloadable Content":  ("Sat", "Lakeside (Cul de Sac x Pando)", "1PM", None),
"Denzel & Joni DJ":      ("Sat", "Lakeside (Cul de Sac x Pando)", "4PM", None),
"DJ Temporary":          ("Sat", "Lakeside (Cul de Sac x Pando)", "6:30PM", "9PM"),
"DJ Miss Parker":        ("Sat", "The Gym", "8PM", None),
"Shaun J. Wright":       ("Sat", "The Gym", "10PM", None),
"BASHKKA":               ("Sat", "The Gym", "12AM", None),
"Verraco":               ("Sat", "The Gym", "2AM", None),
"LYDO b2b Mama Snake":   ("Sat", "The Gym", "4AM", None),
"DJ Maria. b2b DJ Nobu": ("Sat", "The Gym", "6AM", "9AM"),
"OK EG":                 ("Sat", "The Grove", "8PM", None),
"Matas":                 ("Sat", "The Grove", "9:30PM", None),
"Aurora Halal":          ("Sat", "The Grove", "11:30PM", None),
"Konduku & Garçon":      ("Sat", "The Grove", "12:30AM", None),
"Rhadoo":                ("Sat", "The Grove", "3:15AM", None),
"Ogazón":                ("Sat", "The Grove", "6:15AM", None),
"Powder":                ("Sat", "The Grove", "9AM", "1PM"),
"Mike Midnight":         ("Sat", "Bossa Lounge", "8PM", None),
"Joy Guidry":            ("Sat", "Bossa Lounge", "10:45PM", None),
"livwutang":             ("Sat", "Bossa Lounge", "12AM", None),
"DJ Healthy b2b JP":     ("Sat", "Bossa Lounge", "3AM", None),
"CCL":                   ("Sat", "Bossa Lounge", "6AM", "10AM"),
}

URLS = {
"Joy Guidry": "https://guidrybassoon.bandcamp.com/",
"Trickpony": "https://stepballchain.bandcamp.com/album/pillow-talk",
"Mike Midnight": "https://fr33atlast.bandcamp.com/",
}

COUNTRY = {"US":"United States","DE":"Germany","GB":"United Kingdom","CA":"Canada",
"NL":"Netherlands","JP":"Japan","FR":"France","AU":"Australia","MX":"Mexico",
"RO":"Romania","ES":"Spain","CO":"Colombia"}
REGION = {"US":"North America","CA":"North America","MX":"North America",
"CO":"South America","JP":"Asia","AU":"Oceania",
"DE":"Europe","GB":"Europe","NL":"Europe","FR":"Europe","RO":"Europe","ES":"Europe"}


def to_min(t):
    """Clock string -> minutes from noon of the billed day (pre-noon rolls +24h)."""
    t = t.strip().upper()
    ap = "PM" if t.endswith("PM") else "AM"
    hm = t[:-2].strip()
    h, m = (hm.split(":") + ["0"])[:2]
    h, m = int(h), int(m)
    if ap == "PM" and h != 12: h += 12
    if ap == "AM" and h == 12: h = 0
    mins = h * 60 + m
    return mins + 1440 if mins < 720 else mins


def load_optional(p):
    import os
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {}


USER = load_optional("overrides.json")

# derive missing ends from the next set on the same day+stage
by_stage = {}
for name, (day, stage, start, end) in SETTIMES.items():
    by_stage.setdefault((day, stage), []).append((to_min(start), name))
for k in by_stage:
    by_stage[k].sort()

sets = {}
for name, (day, stage, start, end) in SETTIMES.items():
    s = to_min(start)
    if end:
        e = to_min(end)
        if e <= s: e += 1440          # end rolls past the start (e.g. 9AM-1PM)
    else:
        seq = by_stage[(day, stage)]
        nxt = [m for m, n in seq if m > s]
        e = nxt[0] if nxt else None
    sets[name] = {"day": day, "stage": stage, "start": start, "end": end, "s": s, "e": e}

artists = []
for name in sorted(SETTIMES, key=str.lower):
    city, cc, grp, genres = META[name]
    label = LABELS.get(name, "")
    url = URLS.get(name)
    if name in USER:
        u = USER[name]
        grp = u.get("groups", grp); city = u.get("city", city)
        cc = u.get("cc", cc); genres = u.get("genres", genres)
        label = u.get("label", label); url = u.get("url", url)
    artists.append({
        "name": name, "city": city,
        "country": COUNTRY.get(cc, "Unknown"), "region": REGION.get(cc, "Unknown"),
        "groups": [GROUPMAP[g] for g in grp], "genres": genres, "label": label,
        "url": url, "live": name in LIVE, "set": sets[name],
    })

data = {"meta": {"title": "Sustain-Release year twelve", "generated": "2026-08-18",
                 "settimes": True},
        "artists": artists}
with open("data.js", "w", encoding="utf-8") as f:
    f.write("// Sustain-Release year twelve — see build_data.py for sources\n")
    f.write("const MT_DATA = ")
    json.dump(data, f, ensure_ascii=False, indent=1)
    f.write(";\n")

known = sum(1 for a in artists if a["groups"])
print(f"{len(artists)} billed sets · {known} grouped · "
      f"{sum(1 for a in artists if a['live'])} live · 3 days, "
      f"{len(set(v['stage'] for v in sets.values()))} stages")
