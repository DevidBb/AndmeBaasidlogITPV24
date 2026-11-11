"""Item price scanner.

When a screenshot is taken while the mouse is over an item in the inventory,
the area under the cursor is compared with every item icon from tarkov.dev
and the best match (with prices) is returned.

Needs: pip install numpy opencv-python
"""
import json
import os
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np

API = "https://api.tarkov.dev/graphql"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
ICONS = os.path.join(CACHE, "icons")
UA = {"User-Agent": "tarkov-map-companion", "Content-Type": "application/json"}

ITEMS_Q = "{ items { id name shortName normalizedName width height gridImageLink iconLink types } }"
PRICES_Q = ("{ items { id avg24hPrice lastLowPrice basePrice "
            "sellFor { priceRUB vendor { name normalizedName } } } }")

COARSE_CELL = 16      # cell size (px) used for the fast first pass
GRID_CELL_1080 = 63   # inventory cell size in px at 1080p
MIN_SCORE = 0.55      # below this the match is ignored


def gql(query):
    req = urllib.request.Request(API, json.dumps({"query": query}).encode(), UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["data"]["items"]


def imread(path):
    data = np.fromfile(path, dtype=np.uint8)  # works with any characters in the path
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


# ---------------------------------------------------------------- cursor ---

def grab_cursor():
    """Mouse position relative to the game window, as fractions 0..1 (Windows only)."""
    if sys.platform != "win32":
        return None
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32
    pt = wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    hwnd = user32.FindWindowW(None, "EscapeFromTarkov")
    if hwnd:
        rect = wintypes.RECT()
        user32.GetClientRect(hwnd, ctypes.byref(rect))
        user32.ScreenToClient(hwnd, ctypes.byref(pt))
        cw, ch = rect.right, rect.bottom
    else:
        cw, ch = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if cw <= 0 or ch <= 0:
        return None
    fx, fy = pt.x / cw, pt.y / ch
    return (fx, fy) if 0 <= fx < 1 and 0 <= fy < 1 else None


def make_dpi_aware():
    if sys.platform == "win32":
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass


# --------------------------------------------------------------- scanner ---

class Scanner:
    def __init__(self, cell_1080=GRID_CELL_1080):
        self.cell_1080 = cell_1080
        self.items = {}       # id -> metadata
        self.prices = {}      # id -> price info
        self.templates = []   # (id, w, h, coarse_img)
        self.ready = False
        self.lock = threading.Lock()

    # ---- data loading ----
    def start(self):
        threading.Thread(target=self._load, daemon=True).start()
        threading.Thread(target=self._price_loop, daemon=True).start()

    def _load(self):
        try:
            os.makedirs(ICONS, exist_ok=True)
            meta = os.path.join(CACHE, "items.json")
            if os.path.exists(meta) and time.time() - os.path.getmtime(meta) < 24 * 3600:
                items = json.load(open(meta, encoding="utf-8"))
            else:
                print("[items] downloading item list from tarkov.dev ...")
                items = gql(ITEMS_Q)
                json.dump(items, open(meta, "w", encoding="utf-8"))
            items = [i for i in items if i.get("gridImageLink") and "preset" not in (i.get("types") or [])]
            self.items = {i["id"]: i for i in items}
            todo = [i for i in items if not os.path.exists(self._icon_path(i))]
            if todo:
                print(f"[items] downloading {len(todo)} icons (first run only) ...")
                with ThreadPoolExecutor(16) as ex:
                    list(ex.map(self._download_icon, todo))
            templates = []
            for i in items:
                img = imread(self._icon_path(i)) if os.path.exists(self._icon_path(i)) else None
                if img is None:
                    continue
                w, h = i["width"], i["height"]
                small = cv2.resize(img, (w * COARSE_CELL, h * COARSE_CELL), interpolation=cv2.INTER_AREA)
                templates.append((i["id"], w, h, small, img))
            with self.lock:
                self.templates = templates
                self.ready = True
            print(f"[items] ready: {len(templates)} items")
        except Exception as e:
            print(f"[items] failed to load items: {e}")

    def _price_loop(self):
        while True:
            try:
                self.prices = {p["id"]: p for p in gql(PRICES_Q)}
                print(f"[items] prices updated ({len(self.prices)})")
            except Exception as e:
                print(f"[items] price update failed: {e}")
            time.sleep(15 * 60)

    @staticmethod
    def _icon_path(item):
        return os.path.join(ICONS, item["id"] + ".img")

    def _download_icon(self, item):
        try:
            req = urllib.request.Request(item["gridImageLink"], headers={"User-Agent": UA["User-Agent"]})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            with open(self._icon_path(item), "wb") as f:
                f.write(data)
        except Exception:
            pass

    # ---- matching ----
    def identify(self, shot_path, cursor):
        if not self.ready or cursor is None:
            return None
        shot = imread(shot_path)
        if shot is None:
            return None
        H, W = shot.shape[:2]
        cx, cy = int(cursor[0] * W), int(cursor[1] * H)
        cell = self.cell_1080 * H / 1080.0
        with self.lock:
            templates = self.templates

        # pass 1: everything at low resolution -> shortlist
        coarse = self._match(shot, cx, cy, cell, COARSE_CELL / cell,
                             [(t[0], t[1], t[2], t[3]) for t in templates])
        shortlist = {tid for _, tid in coarse[:40]}

        # pass 2: shortlist at full resolution, a few scales
        fine = []
        full = [(t[0], t[1], t[2], t[4]) for t in templates if t[0] in shortlist]
        for scale in (0.96, 1.0, 1.04):
            c = cell * scale
            sized = [(tid, w, h, cv2.resize(img, (round(w * c), round(h * c)), interpolation=cv2.INTER_AREA))
                     for tid, w, h, img in full]
            fine += self._match(shot, cx, cy, cell, 1.0, sized)
        ranked, seen = [], set()
        for score, tid in sorted(fine, reverse=True):
            if tid not in seen:
                seen.add(tid)
                ranked.append((score, tid))
            if len(ranked) == 4:
                break
        if not ranked:
            return None
        if ranked[0][0] < MIN_SCORE:
            print(f"[items] no confident match (best {ranked[0][0]:.2f})")
            return None
        score, tid = ranked[0]
        info = self.describe(tid)
        info["score"] = round(score, 3)
        info["alternatives"] = [{"name": self.items[t]["name"], "score": round(s, 3)}
                                for s, t in ranked[1:] if s > MIN_SCORE]
        return info

    @staticmethod
    def _match(shot, cx, cy, cell, k, templates):
        """Score templates that would cover the cursor. k = resize factor applied to the screenshot."""
        H, W = shot.shape[:2]
        reach = int(6.5 * cell) + 4                 # biggest item is ~6 cells
        x0, y0 = max(0, cx - reach), max(0, cy - reach)
        x1, y1 = min(W, cx + reach), min(H, cy + reach)
        crop = shot[y0:y1, x0:x1]
        if k != 1.0:
            crop = cv2.resize(crop, None, fx=k, fy=k, interpolation=cv2.INTER_AREA)
        ccx, ccy = (cx - x0) * k, (cy - y0) * k
        out = []
        for tid, w, h, tpl in templates:
            for t in ((tpl,) if w == h else (tpl, cv2.rotate(tpl, cv2.ROTATE_90_CLOCKWISE))):
                th, tw = t.shape[:2]
                ax0, ay0 = int(max(0, ccx - tw + 1)), int(max(0, ccy - th + 1))
                ax1, ay1 = int(min(crop.shape[1], ccx + tw)), int(min(crop.shape[0], ccy + th))
                if ax1 - ax0 < tw or ay1 - ay0 < th:
                    continue
                score = float(cv2.matchTemplate(crop[ay0:ay1, ax0:ax1], t, cv2.TM_CCOEFF_NORMED).max())
                if np.isfinite(score):
                    out.append((score, tid))
        out.sort(reverse=True)
        return out

    def describe(self, tid):
        it = self.items[tid]
        p = self.prices.get(tid, {})
        traders = [s for s in (p.get("sellFor") or []) if s["vendor"]["normalizedName"] != "flea-market"]
        flea = next((s["priceRUB"] for s in (p.get("sellFor") or [])
                     if s["vendor"]["normalizedName"] == "flea-market"), None)
        best_trader = max(traders, key=lambda s: s["priceRUB"], default=None)
        slots = max(1, it["width"] * it["height"])
        flea_price = p.get("avg24hPrice") or p.get("lastLowPrice") or flea
        return {
            "id": tid,
            "name": it["name"],
            "shortName": it["shortName"],
            "icon": it.get("iconLink") or it["gridImageLink"],
            "size": [it["width"], it["height"]],
            "flea": flea_price,
            "fleaPerSlot": round(flea_price / slots) if flea_price else None,
            "trader": {"name": best_trader["vendor"]["name"], "price": best_trader["priceRUB"]} if best_trader else None,
            "link": "https://tarkov.dev/item/" + (it.get("normalizedName") or tid),
            "time": time.time(),
        }
