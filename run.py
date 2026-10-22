import sys
import os
import socket
import webbrowser
import threading
import time
import uvicorn

# Ensure the root venture-swarm directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def open_browser(port: int):
    time.sleep(1.5)
    url = f"http://localhost:{port}"
    print(f"\n[VentureSwarm] Opening web interface at {url} ...")
    try:
        webbrowser.open(url)
    except Exception:
        pass

if __name__ == "__main__":
    print("=" * 65)
    print("  VENTURESWARM — Multi-Agent Autonomous Launch Platform")
    print("  Architecture: LangGraph-style Agent Swarm with Debate Loop")
    print("  Live Tools: DuckDuckGo Search + Live Competitor Web Scraping")
    print("  Theme: GitHub Primer Dark Mode | Font: Fira Code & SF Mono")
    print("=" * 65)

    target_port = int(os.environ.get("PORT", 8000))
    if is_port_in_use(target_port):
        if target_port == 8000 and not is_port_in_use(8001):
            print(f"\n[Notice] Port {target_port} is already in use by another instance. Switching to port 8001...")
            target_port = 8001
        else:
            print(f"\n[Warning] Port {target_port} appears to be in use. Trying anyway...")

    print(f"\nStarting local server on http://localhost:{target_port} ...\n")

    # Start browser opener in background thread
    threading.Thread(target=open_browser, args=(target_port,), daemon=True).start()

    # Run FastAPI app with Uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=target_port, log_level="info")

