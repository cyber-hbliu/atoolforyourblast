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
# name: (city, cc, groups, genres) — hand metadata, snob-reviewed; blanks honest
META = {
"Byron Yeates": ("Berlin", "DE", "T", ["trance", "progressive"]),
"S-candalo": U,
"Yushh": ("Bristol", "GB", "J", ["bass", "breaks"]),
"D. Tiffany": ("Vancouver", "CA", "H", ["trance-house", "breaks"]),
"Roza Terenzi": ("Berlin", "AU", "TJ", ["breaks", "tech-trance"]),
"Denzel": U,
"Joni DJ": U,
"DJ Deadname": U,
"DJPT": U,
"DJ G": U,
"DJ'J": U,
"DJ Healthy": ("New York", "US", "H", ["club", "house"]),
"JP": U,
"DJ Maria.": ("Tokyo", "JP", "T", ["techno", "bass"]),
"DJ Nobu": ("Chiba", "JP", "T", ["hypnotic techno", "psychedelic techno"]),
"Garçon": ("Rotterdam", "NL", "T", ["percussive techno"]),
"Konduku": ("Amsterdam", "NL", "T", ["percussive techno", "hypnotic"]),
"LYDO": ("New York", "US", "T", ["fast techno", "trance"]),
"Mama Snake": ("Copenhagen", "DK", "T", ["techno", "trance"]),
"Myles Mac": ("Melbourne", "AU", "H", ["chug", "house"]),
"DJ Possum": ("Melbourne", "AU", "H", ["chug", "downtempo house"]),
"Amelia Holt": ("New York", "US", "TE", ["electro", "techno"]),
"Andy Martin": ("", None, "T", ["techno"]),
"Aurora Halal": ("New York", "US", "T", ["techno", "trance"]),
"BASHKKA": ("Munich", "DE", "T", ["club", "techno"]),
"Byrell The Great": ("New York", "US", "J", ["ballroom", "vogue beats"]),
"CCL": ("Berlin / Seattle", "DE", "T", ["bass", "leftfield club"]),
"Como Se DJ": U,
"Cosmo": ("New York", "US", "H", ["house"]),
"Deep Creep": ("New York", "US", "T", ["club"]),
"Denzel & Joni DJ": U,
"DJ Deadname b2b DJPT": U,
"DJ G b2b DJ'J": U,
"DJ Miss Parker": ("New York", "US", "J", ["breaks", "club"]),
"DJ Temporary": U,
"Downloadable Content": U,
"Eden Aurelius": ("", "CA", "H", ["house", "trance"]),
"Ekkel": ("Amsterdam", "NL", "J", ["bubbling", "club"]),
"Escaflowne": U,
"James K": ("New York", "US", "M", ["ambient", "downtempo", "ethereal"]),
"Joy Guidry": ("New York", "US", "A", ["bassoon", "free jazz", "ambient", "experimental"]),
"Kangding Ray presents Sirāt": ("Berlin", "DE", "T", ["techno", "industrial"]),
"livwutang": ("New York", "US", "H", ["dub", "house"]),
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
"Rhadoo": ("Bucharest", "RO", "T", ["rominimal", "minimal"]),
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
"D. Tiffany": "Planet Euphorique", "Roza Terenzi": "Step Ball Chain",
"Yushh": "Pressure Dome", "DJ Nobu": "Future Terror", "Konduku": "Nous'klaer Audio",
"Kangding Ray presents Sirāt": "raster",
}

LIVE = {"Malibu", "Kangding Ray presents Sirāt", "James K", "SPF 50",
        "Trickpony", "OK EG", "Aurora Halal", "Joy Guidry"}

# billed set -> (day, stage, start, end-or-None, [member artists])
SETS = {
"D. Tiffany b2b Roza Terenzi": ("Thu", "The Gym", "9PM", "3AM", ["D. Tiffany", "Roza Terenzi"]),
"Escaflowne": ("Thu", "The Grove", "7PM", None, ["Escaflowne"]),
"Malibu": ("Thu", "The Grove", "10PM", None, ["Malibu"]),
"Kangding Ray presents Sirāt": ("Thu", "The Grove", "11PM", None, ["Kangding Ray presents Sirāt"]),
"mad miran": ("Thu", "The Grove", "12:30AM", "3AM", ["mad miran"]),

"Cosmo": ("Fri", "Lakeside", "1PM", "3:30PM", ["Cosmo"]),
"Myles Mac & DJ Possum": ("Fri", "Lakeside", "3:30PM", "6:30PM", ["Myles Mac", "DJ Possum"]),
"DJ Deadname b2b DJPT": ("Fri", "The Gym", "7:30PM", None, ["DJ Deadname", "DJPT"]),
"Byrell The Great": ("Fri", "The Gym", "10PM", None, ["Byrell The Great"]),
"CCL b2b Yushh": ("Fri", "The Gym", "12AM", None, ["CCL", "Yushh"]),
"Mala": ("Fri", "The Gym", "3AM", "6AM", ["Mala"]),
"James K": ("Fri", "The Grove", "6:30PM", None, ["James K"]),
"Deep Creep": ("Fri", "The Grove", "7:30PM", None, ["Deep Creep"]),
"Ekkel": ("Fri", "The Grove", "9:30PM", None, ["Ekkel"]),
"Naone": ("Fri", "The Grove", "11:30PM", None, ["Naone"]),
"SPF 50": ("Fri", "The Grove", "1:30AM", None, ["SPF 50"]),
"Andy Martin": ("Fri", "The Grove", "2:30AM", None, ["Andy Martin"]),
"Sandwell District": ("Fri", "The Grove", "4:30AM", "7AM", ["Sandwell District"]),
"Como Se DJ": ("Fri", "Bossa Lounge", "9PM", None, ["Como Se DJ"]),
"Trickpony": ("Fri", "Bossa Lounge", "12AM", None, ["Trickpony"]),
"Amelia Holt": ("Fri", "Bossa Lounge", "1AM", None, ["Amelia Holt"]),
"Eden Aurelius": ("Fri", "Bossa Lounge", "3AM", None, ["Eden Aurelius"]),
"DJ G b2b DJ'J": ("Fri", "Bossa Lounge", "5AM", "8AM", ["DJ G", "DJ'J"]),

"Saia": ("Sat", "La Noche Pool Party", "1PM", None, ["Saia"]),
"PAURRO": ("Sat", "La Noche Pool Party", "3PM", None, ["PAURRO"]),
"Byron Yeates b2b S-candalo": ("Sat", "La Noche Pool Party", "5PM", "8PM", ["Byron Yeates", "S-candalo"]),
"Downloadable Content": ("Sat", "Lakeside (Cul de Sac x Pando)", "1PM", None, ["Downloadable Content"]),
"Denzel & Joni DJ": ("Sat", "Lakeside (Cul de Sac x Pando)", "4PM", None, ["Denzel", "Joni DJ"]),
"DJ Temporary": ("Sat", "Lakeside (Cul de Sac x Pando)", "6:30PM", "9PM", ["DJ Temporary"]),
"DJ Miss Parker": ("Sat", "The Gym", "8PM", None, ["DJ Miss Parker"]),
"Shaun J. Wright": ("Sat", "The Gym", "10PM", None, ["Shaun J. Wright"]),
"BASHKKA": ("Sat", "The Gym", "12AM", None, ["BASHKKA"]),
"Verraco": ("Sat", "The Gym", "2AM", None, ["Verraco"]),
"LYDO b2b Mama Snake": ("Sat", "The Gym", "4AM", None, ["LYDO", "Mama Snake"]),
"DJ Maria. b2b DJ Nobu": ("Sat", "The Gym", "6AM", "9AM", ["DJ Maria.", "DJ Nobu"]),
"OK EG": ("Sat", "The Grove", "8PM", None, ["OK EG"]),
"Matas": ("Sat", "The Grove", "9:30PM", None, ["Matas"]),
"Aurora Halal": ("Sat", "The Grove", "11:30PM", None, ["Aurora Halal"]),
"Konduku & Garçon": ("Sat", "The Grove", "12:30AM", None, ["Konduku", "Garçon"]),
"Rhadoo": ("Sat", "The Grove", "3:15AM", None, ["Rhadoo"]),
"Ogazón": ("Sat", "The Grove", "6:15AM", None, ["Ogazón"]),
"Powder": ("Sat", "The Grove", "9AM", "1PM", ["Powder"]),
"Mike Midnight": ("Sat", "Bossa Lounge", "8PM", None, ["Mike Midnight"]),
"Joy Guidry": ("Sat", "Bossa Lounge", "10:45PM", None, ["Joy Guidry"]),
"livwutang": ("Sat", "Bossa Lounge", "12AM", None, ["livwutang"]),
"DJ Healthy b2b JP": ("Sat", "Bossa Lounge", "3AM", None, ["DJ Healthy", "JP"]),
"CCL": ("Sat", "Bossa Lounge", "6AM", "10AM", ["CCL"]),
}

URLS = {
"Joy Guidry": "https://guidrybassoon.bandcamp.com/",
"Trickpony": "https://stepballchain.bandcamp.com/album/pillow-talk",
"Mike Midnight": "https://fr33atlast.bandcamp.com/",
}

COUNTRY = {"US":"United States","DE":"Germany","GB":"United Kingdom","CA":"Canada",
"NL":"Netherlands","JP":"Japan","FR":"France","AU":"Australia","MX":"Mexico",
"RO":"Romania","DK":"Denmark","ES":"Spain","CO":"Colombia"}
REGION = {"US":"North America","CA":"North America","MX":"North America",
"CO":"South America","JP":"Asia","AU":"Oceania",
"DE":"Europe","GB":"Europe","NL":"Europe","FR":"Europe","RO":"Europe","ES":"Europe","DK":"Europe"}


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

by_stage = {}
for bill, (day, stage, start, end, members) in SETS.items():
    by_stage.setdefault((day, stage), []).append((to_min(start), bill))
for k in by_stage:
    by_stage[k].sort()

sets_out = []
people_set = {}
for bill, (day, stage, start, end, members) in SETS.items():
    smin = to_min(start)
    if end:
        emin = to_min(end)
        if emin <= smin: emin += 1440
    else:
        seq = by_stage[(day, stage)]
        nxt = [m for m, n in seq if m > smin]
        emin = nxt[0] if nxt else None
    sets_out.append({"bill": bill, "day": day, "stage": stage,
                     "start": start, "end": end, "s": smin, "e": emin,
                     "members": members, "live": bill in LIVE})
    for p in members:
        people_set[p] = {"day": day, "stage": stage, "start": start,
                         "end": end, "s": smin, "e": emin, "bill": bill}
sets_out.sort(key=lambda x: ({"Thu":0,"Fri":1,"Sat":2}[x["day"]], x["s"]))

names = sorted(people_set, key=str.lower)
missing = [n for n in names if n not in META]
assert not missing, missing

artists = []
for name in names:
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
        "url": url, "live": name in LIVE or people_set[name]["bill"] in LIVE,
        "set": people_set[name],
    })

data = {"meta": {"title": "Sustain-Release year twelve", "generated": "2026-09-04",
                 "settimes": True},
        "artists": artists, "sets": sets_out}
with open("data.js", "w", encoding="utf-8") as f:
    f.write("// Sustain-Release year twelve — see build_data.py for sources\n")
    f.write("const MT_DATA = ")
    json.dump(data, f, ensure_ascii=False, indent=1)
    f.write(";\n")

known = sum(1 for a in artists if a["groups"])
print(f"{len(artists)} people · {len(sets_out)} billed sets · {known} grouped · "
      f"{len(set(x['stage'] for x in sets_out))} stages")
