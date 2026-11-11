#!/usr/bin/env python3
"""Tarkov Map companion server.

Watches the Escape from Tarkov screenshot folder. When you take a screenshot
in raid, the game writes your position into the file name. This server reads
it and pushes it to the phone app (open http://<PC-IP>:8080 on the phone).

Only the Python standard library is used.
"""
import argparse
import glob
import json
import os
import re
import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

# 2024-06-20[15-44]_-113.6, 2.5, 84.1_0.0, -0.9, 0.0, 0.4_15.53 (0).png
NUM = r"(-?\d+(?:\.\d+)?)"
SHOT_RE = re.compile(
    r"_" + NUM + r", " + NUM + r", " + NUM +
    r"_" + NUM + r", " + NUM + r", " + NUM + r", " + NUM + r"_"
)

# Location ids from the game logs -> map ids used by the app.
LOCATIONS = {
    "bigmap": "customs",
    "factory4_day": "factory",
    "factory4_night": "factory",
    "interchange": "interchange",
    "laboratory": "the-lab",
    "lighthouse": "lighthouse",
    "rezervbase": "reserve",
    "shoreline": "shoreline",
    "tarkovstreets": "streets-of-tarkov",
    "woods": "woods",
    "sandbox": "ground-zero",
    "sandbox_high": "ground-zero",
    "labyrinth": "the-labyrinth",
    "terminal": "terminal",
}
LOC_RE = re.compile(r"Location:\s*([A-Za-z0-9_]+)")


class State:
    def __init__(self):
        self.cond = threading.Condition()
        self.version = 0
        self.position = None
        self.map = None
        self.item = None

    def publish(self, **kw):
        with self.cond:
            for k, v in kw.items():
                setattr(self, k, v)
            self.version += 1
            self.cond.notify_all()

    def snapshot(self):
        return {"version": self.version, "position": self.position, "map": self.map, "item": self.item}


STATE = State()
SCANNER = None
items_mod = None
SCAN_POOL = ThreadPoolExecutor(1)


def scan_item(path, cursor, delete):
    try:
        for _ in range(20):  # wait until the game has finished writing the file
            size = os.path.getsize(path)
            time.sleep(0.15)
            if size and size == os.path.getsize(path):
                break
        t0 = time.time()
        item = SCANNER.identify(path, cursor)
        if item:
            print(f"[items] {item['name']}  flea={item['flea']}  ({item['score']}, {time.time() - t0:.1f}s)")
            STATE.publish(item=item)
    except Exception as e:
        print(f"[items] scan failed: {e}")
    finally:
        if delete:
            try:
                os.remove(path)
            except OSError:
                pass


def parse_screenshot(name):
    m = SHOT_RE.search(name)
    if not m:
        return None
    x, y, z, qx, qy, qz, qw = (float(v) for v in m.groups())
    return {"x": x, "y": y, "z": z, "q": [qx, qy, qz, qw], "file": name, "time": time.time()}


def default_screens_dir():
    home = os.environ.get("USERPROFILE") or os.path.expanduser("~")
    return os.path.join(home, "Documents", "Escape from Tarkov", "Screenshots")


def default_logs_dir():
    for p in (r"C:\Battlestate Games\EFT\Logs", r"C:\Battlestate Games\Escape from Tarkov\Logs"):
        if os.path.isdir(p):
            return p
    return None


def watch_screenshots(folder, delete, interval):
    seen = set(os.listdir(folder)) if os.path.isdir(folder) else set()
    print(f"[screens] watching {folder}")
    while True:
        time.sleep(interval)
        if not os.path.isdir(folder):
            continue
        current = set(os.listdir(folder))
        for name in sorted(current - seen):
            path = os.path.join(folder, name)
            cursor = SCANNER and items_mod.grab_cursor()  # read the mouse right away
            pos = parse_screenshot(name)
            if pos:
                print(f"[screens] x={pos['x']:.1f} y={pos['y']:.1f} z={pos['z']:.1f}")
                STATE.publish(position=pos)
            if cursor:
                SCAN_POOL.submit(scan_item, path, cursor, delete)
            elif delete and pos:
                try:
                    os.remove(path)
                except OSError:
                    pass
        seen = current


def watch_logs(folder, interval):
    """Best effort: detect the current map from the newest application log."""
    print(f"[logs] watching {folder}")
    path, offset = None, 0
    while True:
        time.sleep(interval)
        files = glob.glob(os.path.join(folder, "**", "*application*.log"), recursive=True)
        if not files:
            continue
        newest = max(files, key=os.path.getmtime)
        if newest != path:
            path, offset = newest, 0
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(offset)
                chunk = f.read()
                offset = f.tell()
        except OSError:
            continue
        found = LOC_RE.findall(chunk)
        if found:
            map_id = LOCATIONS.get(found[-1].lower())
            if map_id and map_id != STATE.map:
                print(f"[logs] map: {map_id}")
                STATE.publish(map=map_id)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=WEB_DIR, **kw)

    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path == "/api/state":
            body = json.dumps(STATE.snapshot()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            last = -1
            try:
                while True:
                    with STATE.cond:
                        if STATE.version == last:
                            STATE.cond.wait(timeout=15)
                        snap = STATE.snapshot()
                    if snap["version"] != last:
                        last = snap["version"]
                        self.wfile.write(f"data: {json.dumps(snap)}\n\n".encode())
                    else:
                        self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, OSError):
                return
        return super().do_GET()


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def main():
    ap = argparse.ArgumentParser(description="Tarkov Map companion server")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--screens", default=default_screens_dir(), help="EFT screenshot folder")
    ap.add_argument("--logs", default=default_logs_dir(), help="EFT Logs folder (map auto-detect)")
    ap.add_argument("--delete", action="store_true", help="delete screenshots after reading")
    ap.add_argument("--no-items", action="store_true", help="disable the item price scanner")
    ap.add_argument("--cell", type=float, default=63, help="inventory cell size in px at 1080p")
    args = ap.parse_args()

    global SCANNER, items_mod
    if not args.no_items:
        try:
            import items as items_mod
            items_mod.make_dpi_aware()
            SCANNER = items_mod.Scanner(args.cell)
            SCANNER.start()
            if sys.platform != "win32":
                print("[items] cursor reading works only on Windows")
        except ImportError:
            print("[items] disabled: run  pip install numpy opencv-python")

    threading.Thread(target=watch_screenshots, args=(args.screens, args.delete, 0.3), daemon=True).start()
    if args.logs and os.path.isdir(args.logs):
        threading.Thread(target=watch_logs, args=(args.logs, 2.0), daemon=True).start()
    else:
        print("[logs] not found - pick the map on the phone manually")

    srv = ThreadingHTTPServer(("0.0.0.0", args.port), Handler)
    print(f"\n  Open on your phone:  http://{lan_ip()}:{args.port}\n")
    srv.serve_forever()


if __name__ == "__main__":
    main()
