"""Check staged assets under the actual repository path without a browser.

This is a local HTTP check, not desktop/mobile rendering or deployment evidence.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from urllib.request import urlopen
import functools,json,shutil,tempfile

ROOT=Path(__file__).resolve().parents[1]
TEMP_PARENT=ROOT/'.qa-tmp'
TEMP_PARENT.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='feoc-http-',dir=TEMP_PARENT) as tmp:
    temp_root=Path(tmp).resolve()
    assert temp_root.is_relative_to(TEMP_PARENT.resolve())
    target=temp_root/'FE-OC-website'
    shutil.copytree(ROOT/'_site',target)
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self,*args): pass
    server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(temp_root)))
    thread=Thread(target=server.serve_forever,daemon=True); thread.start()
    results=[]
    try:
        base=f'http://127.0.0.1:{server.server_port}/FE-OC-website/'
        for file in sorted(target.rglob('*')):
            if not file.is_file(): continue
            name=file.relative_to(target).as_posix()
            with urlopen(base+name) as response:
                payload=response.read()
                assert response.status==200 and payload==file.read_bytes(),name
                results.append({'path':name,'status':response.status,'bytes_identical':True})
        with urlopen(base) as response: assert response.status==200
    finally:
        server.shutdown();server.server_close();thread.join()
(ROOT/'docs/local-http-checks.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
print(f'PASS: {len(results)} staged files served byte-for-byte under /FE-OC-website/.')
