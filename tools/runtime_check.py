#!/usr/bin/env python3
"""Runtime check for LoyaltyPointsInquiryAPI: python3 tools/runtime_check.py <project folder> [--change]

The Toolkit check proves the project builds. This check proves it works: it deploys the REST API to a
local, throw-away ACE integration server and calls it with the cases of the mock SRS, against a mock LMS
that this script runs itself. Nothing is installed and nothing outside a scratch folder is changed.

Steps:
  1. Build a BAR from a copy of the project (mqsicreatebar -cleanBuild).
  2. Point the service at the mock LMS with BAR overrides of the user-defined property LMS_URL, and
     shorten the HTTP Request timeout with an override of timeoutForServer. If LMS_URL is not a
     deploy-time property, that is reported as a failure (IBM-14): no deploy could set the real URL.
  3. Deploy the BAR to a new work directory and start an integration server on a free port.
  4. Send each case and compare the reply and what LMS received with what the SRS says.
  5. Stop the server and delete the scratch folder.

Exit 0 = every case passed, 1 = a case failed or the service did not start, 2 = ACE not found.
--change adds the URF-90001 cases (partnerCode, includeExpiring, pointsExpiringNext30Days).
--force-url  (diagnosis only) when LMS_URL is not a deploy-time property, rewrite the default URL in the
             copied ESQL so the remaining cases can still run. The IBM-14 failure is still reported.

Needs ACE 12 or 13 with its integration server (the Toolkit install includes it). Tested on macOS with
ACE 13.0.9; the Linux and Windows paths follow the same commands but have not been run.
"""
import glob
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

URL_PROPERTY = "LMS_URL"
SERVICE_PATH = "/loyalty/v1/loyalty-points-inquiry"
TIMEOUT_SECONDS = 3          # HTTP Request node timeout set by override
SLOW_SECONDS = 6             # how long the mock LMS sleeps for the timeout case
WINDOWS = platform.system() == "Windows"

# ---------------------------------------------------------------- mock LMS

LMS_LOG = []
SUCCESS = ("<PointsInquiryRes><CIF_Number>{cif}</CIF_Number><Member_Id>M-778</Member_Id>"
           "<Tier_Code>GOLD</Tier_Code><Points_Balance>12500</Points_Balance><Points_Pending>300</Points_Pending>"
           "<Points_Expiry_Date>2027-03-31</Points_Expiry_Date><Status>ACTIVE</Status>{extra}</PointsInquiryRes>")


class MockLMS(BaseHTTPRequestHandler):
    """Answers by CIF_Number: OK1 success, OK2 success with Points_Expiring_30D, LMSERR an LMS error,
    HTTP500 an HTTP 500, SLOW sleeps past the node timeout."""

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0)).decode("utf-8", "replace")
        LMS_LOG.append({"path": self.path, "body": body})
        m = re.search(r"<CIF_Number>([^<]*)</CIF_Number>", body)
        cif = m.group(1) if m else ""
        status, xml = 200, SUCCESS.format(cif=cif, extra="")
        if cif == "OK2":
            xml = SUCCESS.format(cif=cif, extra="<Points_Expiring_30D>450</Points_Expiring_30D>")
        elif cif == "LMSERR":
            xml = "<PointsInquiryRes><Error_Code>LMS-404</Error_Code><Error_Desc>Member not found</Error_Desc></PointsInquiryRes>"
        elif cif == "HTTP500":
            status, xml = 500, "<Fault><Code>LMS-500</Code><Reason>Internal error</Reason></Fault>"
        elif cif == "SLOW":
            time.sleep(SLOW_SECONDS)
        data = xml.encode()
        try:
            self.send_response(status)
            self.send_header("Content-Type", "text/xml; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except OSError:
            pass  # the caller timed out and closed the socket

    def log_message(self, *a):
        pass


# ---------------------------------------------------------------- cases
# expect: status, json (fields that must equal), absent (fields that must not be in the reply),
#         lms (XML elements LMS must receive, value or None for "must not be sent"), lms_called (bool)

OK_FIELDS = {"cifNumber": "OK1", "memberId": "M-778", "tierCode": "GOLD", "pointsBalance": "12500",
             "pointsPending": "300", "pointsExpiryDate": "2027-03-31", "status": "ACTIVE"}

CASES = [
    ("missing mandatory field -> 400 EAI-LMS-BRK-001 (SRS 2.2), LMS not called",
     {"programCode": "RETAIL"},
     {"status": 400, "json": {"errorCode": "EAI-LMS-BRK-001"}, "lms_called": False}),
    ("invalid programCode -> 400 EAI-LMS-BRK-002 (SRS 2.1.1, 2.2), LMS not called",
     {"cifNumber": "OK1", "programCode": "GOLD"},
     {"status": 400, "json": {"errorCode": "EAI-LMS-BRK-002"}, "lms_called": False}),
    ("payload wrapped in {\"Data\": ...} is not the API shape -> 400 EAI-LMS-BRK-001 (IBM-16)",
     {"Data": {"cifNumber": "OK1", "programCode": "RETAIL"}},
     {"status": 400, "json": {"errorCode": "EAI-LMS-BRK-001"}, "lms_called": False}),
    ("success -> 200 with every output field mapped (SRS 2.1.1 OUTPUT)",
     {"cifNumber": "OK1", "programCode": "RETAIL", "cardNumber": "4000111122223333"},
     {"status": 200, "json": OK_FIELDS,
      "lms": {"CIF_Number": "OK1", "Program_Code": "RETAIL", "Card_Number": "4000111122223333"}}),
    ("LMS returns Error_Code -> 400 EAI-LMS-BRK-004 with the LMS code in errorDesc (SRS 2.2)",
     {"cifNumber": "LMSERR", "programCode": "RETAIL"},
     {"status": 400, "json": {"errorCode": "EAI-LMS-BRK-004"}, "desc_contains": "LMS-404"}),
    ("LMS times out -> 500 EAI-LMS-BRK-003 (SRS 2.2)",
     {"cifNumber": "SLOW", "programCode": "RETAIL"},
     {"status": 500, "json": {"errorCode": "EAI-LMS-BRK-003"}}),
    ("LMS answers HTTP 500 -> an error reply within the timeout, not a hang",
     {"cifNumber": "HTTP500", "programCode": "RETAIL"},
     {"status_in": [400, 500, 502], "json_has": ["errorCode"]}),
]

CHANGE_CASES = [
    ("URF-90001: partnerCode sent to LMS for COBRAND",
     {"cifNumber": "OK1", "programCode": "COBRAND", "partnerCode": "P77", "includeExpiring": "Y"},
     {"status": 200, "lms": {"Partner_Code": "P77", "Include_Expiring": "Y"}}),
    ("URF-90001: partnerCode not sent to LMS for RETAIL",
     {"cifNumber": "OK1", "programCode": "RETAIL", "partnerCode": "P77"},
     {"status": 200, "lms": {"Partner_Code": None}}),
    ("URF-90001: includeExpiring absent -> N",
     {"cifNumber": "OK1", "programCode": "RETAIL"},
     {"status": 200, "lms": {"Include_Expiring": "N"}}),
    ("URF-90001: includeExpiring empty -> N (decision: empty counts as not present)",
     {"cifNumber": "OK1", "programCode": "RETAIL", "includeExpiring": ""},
     {"status": 200, "lms": {"Include_Expiring": "N"}}),
    ("URF-90001: pointsExpiringNext30Days returned when LMS sends it",
     {"cifNumber": "OK2", "programCode": "RETAIL"},
     {"status": 200, "json": {"pointsExpiringNext30Days": "450"}}),
    ("URF-90001: pointsExpiringNext30Days absent when LMS does not send it",
     {"cifNumber": "OK1", "programCode": "RETAIL"},
     {"status": 200, "absent": ["pointsExpiringNext30Days"]}),
]

# Checked on every reply, reported once: (case, Content-Type, has X-TRACKING-ID)
REPLIES = []


# ---------------------------------------------------------------- ACE helpers

def ace_home():
    homes = [os.environ["ACE_HOME"]] if os.environ.get("ACE_HOME") else []
    if WINDOWS:
        for root in (os.environ.get("ProgramFiles", r"C:\Program Files"), r"C:\IBM"):
            homes += sorted(glob.glob(os.path.join(root, "IBM", "ACE", "*")), reverse=True)
            homes += sorted(glob.glob(os.path.join(root, "ACE", "*")), reverse=True)
    elif platform.system() == "Darwin":
        homes += [os.path.expanduser("~/Applications/IBM App Connect Enterprise"),
                  "/Applications/IBM App Connect Enterprise"]
    else:
        homes += sorted(glob.glob("/opt/IBM/ace-*"), reverse=True) + sorted(glob.glob("/opt/ibm/ace-*"), reverse=True)
    for home in homes:
        if os.path.isdir(os.path.join(home, "server", "bin")):
            return home
    return None


def ace(home, command, log, background=False):
    """Run an ACE command with the mqsiprofile environment."""
    if WINDOWS:
        line = f'"{os.path.join(home, "server", "bin", "mqsiprofile.cmd")}" >NUL && {command}'
        args = ["cmd", "/c", line]
    else:
        line = f'. "{os.path.join(home, "server", "bin", "mqsiprofile")}" >/dev/null 2>&1; {command}'
        args = ["bash", "-c", line]
    out = open(log, "a")
    if background:
        return subprocess.Popen(args, stdout=out, stderr=subprocess.STDOUT)
    return subprocess.run(args, stdout=out, stderr=subprocess.STDOUT).returncode


def q(path):
    return f'"{path}"'


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def configurable(bar):
    """Configurable property names in the BAR (from META-INF/broker.xml of the nested application)."""
    props = []
    with zipfile.ZipFile(bar) as z:
        for name in z.namelist():
            if name.endswith(".appzip"):
                with zipfile.ZipFile(z.open(name)) as app:
                    xml = app.read("META-INF/broker.xml").decode("utf-8", "replace")
                    props += re.findall(r'<ConfigurableProperty[^>]*uri="([^"]+)"', xml)
    return props


# ---------------------------------------------------------------- one case

def service_path(project):
    """Base path + operation path from the project's openapi.json; the SRS path if it cannot be read."""
    try:
        api = json.load(open(os.path.join(project, "openapi.json"), encoding="utf-8"))
        base = api.get("basePath") or (api.get("servers") or [{}])[0].get("url", "")
        base = re.sub(r"^[a-z]+://[^/]+", "", base).rstrip("/")
        path = next(p for p in api["paths"] if "loyalty-points-inquiry" in p)
        return base + path
    except Exception:
        return SERVICE_PATH


def call(port, body):
    req = urllib.request.Request(f"http://127.0.0.1:{port}{SERVICE_PATH}", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "ClientId": "c1",
                                          "Authorization": "Bearer t", "X-USER-ID": "u1", "X-MSG-ID": "m1",
                                          "X-ORG-ID": "AE"}, method="POST")
    try:
        r = urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS + 30)
        return r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode("utf-8", "replace")
    except Exception as e:
        return None, {}, repr(e)


def check(port, name, body, exp):
    before = len(LMS_LOG)
    t = time.time()
    status, headers, text = call(port, body)
    took = time.time() - t
    sent = LMS_LOG[before:]
    problems = []
    try:
        reply = json.loads(text)
    except ValueError:
        reply = None
    if "status" in exp and status != exp["status"]:
        problems.append(f"HTTP {status}, expected {exp['status']}")
    if "status_in" in exp and status not in exp["status_in"]:
        problems.append(f"HTTP {status}, expected one of {exp['status_in']}")
    if not isinstance(reply, dict):
        problems.append("reply is not a JSON object")
        reply = {}
    for k, v in exp.get("json", {}).items():
        if reply.get(k) != v:
            problems.append(f"{k} = {reply.get(k)!r}, expected {v!r}")
    for k in exp.get("json_has", []):
        if k not in reply:
            problems.append(f"{k} missing")
    for k in exp.get("absent", []):
        if k in reply:
            problems.append(f"{k} present ({reply[k]!r}), expected absent")
    if "desc_contains" in exp and exp["desc_contains"] not in str(reply.get("errorDesc")):
        problems.append(f"errorDesc {reply.get('errorDesc')!r} lacks {exp['desc_contains']!r}")
    if exp.get("lms_called") is False and sent:
        problems.append("LMS was called")
    if "lms" in exp:
        if not sent:
            problems.append("LMS was not called")
        else:
            xml = sent[-1]["body"]
            for el, v in exp["lms"].items():
                m = re.search(rf"<{el}>([^<]*)</{el}>|<{el}/>", xml)
                got = None if not m else (m.group(1) or "")
                if v is None and m:
                    problems.append(f"LMS got {el}={got!r}, expected not sent")
                elif v is not None and got != v:
                    problems.append(f"LMS got {el}={got!r}, expected {v!r}")
    if status is not None:
        ctype = next((v for k, v in headers.items() if k.lower() == "content-type"), "")
        REPLIES.append((name, ctype, any(k.lower() == "x-tracking-id" for k in headers)))
    mark = "PASS" if not problems else "FAIL"
    print(f"  {mark}  {name}  [{took:.1f}s]")
    for p in problems:
        print(f"        - {p}")
    if problems:
        print(f"        reply: HTTP {status} {text[:200]}")
    return not problems


# ---------------------------------------------------------------- main

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    project = os.path.abspath(args[0])
    name = os.path.basename(project.rstrip("/\\"))
    home = ace_home()
    if not home:
        print("RUNTIME CHECK: NOT RUN - ACE not found. Set ACE_HOME to the ACE installation folder.")
        return 2
    # The integration server's admin socket path must stay under 104 characters on macOS.
    base = os.environ.get("RUNTIME_CHECK_DIR") or ("/tmp" if not WINDOWS and os.path.isdir("/tmp") else None)
    scratch = tempfile.mkdtemp(prefix="rtc-", dir=base)
    log = os.path.join(scratch, "ace.log")
    server = None
    lms = ThreadingHTTPServer(("127.0.0.1", 0), MockLMS)
    threading.Thread(target=lms.serve_forever, daemon=True).start()
    lms_url = f"http://127.0.0.1:{lms.server_address[1]}/PointsInquiry"
    failures = []
    try:
        ws = os.path.join(scratch, "ws")
        os.makedirs(ws)
        shutil.copytree(project, os.path.join(ws, name))
        bar, bar2 = os.path.join(scratch, "a.bar"), os.path.join(scratch, "b.bar")

        def build():
            exe = os.path.join(home, "tools", "mqsicreatebar.exe" if WINDOWS else "mqsicreatebar")
            subprocess.run([exe, "-data", ws, "-b", bar, "-a", name, "-cleanBuild"],
                           stdout=open(log, "a"), stderr=subprocess.STDOUT)
            return os.path.isfile(bar)

        if not build():
            print(f"RUNTIME CHECK: FAIL - the BAR did not build; run toolkit_check.py first. Log: {log}")
            return 1
        props = configurable(bar)
        # In a REST API the value used at run time is the one on the operation's subflow node in the main
        # flow ("gen.<API>#<operation> (Implementation).LMS_URL"); set every LMS_URL entry the BAR has.
        url_props = [p for p in props if p.endswith(("#" + URL_PROPERTY, "." + URL_PROPERTY))]
        if not url_props:
            failures.append(f"IBM-14: {URL_PROPERTY} is not a deploy-time property of the BAR, so no deploy can "
                            f"set the real LMS URL. Define it as a user-defined property on the flow or subflow "
                            f"that holds the Compute node.")
            print("  FAIL  " + failures[-1])
            if "--force-url" not in sys.argv:
                print("RUNTIME CHECK: FAIL (stopped; --force-url runs the other cases for diagnosis)")
                return 1
            for esql in glob.glob(os.path.join(ws, name, "**", "*.esql"), recursive=True):
                text = open(esql, encoding="utf-8").read()
                new = re.sub(rf"(DECLARE\s+{URL_PROPERTY}\s+EXTERNAL\s+CHARACTER\s+)'[^']*'", rf"\1'{lms_url}'", text)
                if new != text:
                    open(esql, "w", encoding="utf-8").write(new)
            os.remove(bar)
            build()
            print("  NOTE  --force-url: default LMS URL rewritten in the copied ESQL for the remaining cases")
        overrides = [f"{p}={TIMEOUT_SECONDS}" for p in props if p.endswith(".timeoutForServer")]
        overrides += [f"{p}={lms_url}" for p in url_props]
        if overrides:
            ace(home, f"mqsiapplybaroverride -b {q(bar)} -o {q(bar2)} -k {name} -m {q(','.join(overrides))}", log)
            if os.path.isfile(bar2):
                bar = bar2
        work = os.path.join(scratch, "w")
        ace(home, f"mqsicreateworkdir {q(work)}", log)
        ace(home, f"ibmint deploy --input-bar-file {q(bar)} --output-work-directory {q(work)}", log)
        port = free_port()
        server_log = os.path.join(scratch, "server.log")
        server = ace(home, f"IntegrationServer --work-dir {q(work)} --http-port-number {port} --admin-rest-api -1",
                     server_log, background=True)
        started = False
        for _ in range(120):
            time.sleep(1)
            text = open(server_log, encoding="utf-8", errors="replace").read()
            if "BIP1991I" in text:
                started = True
                break
            if server.poll() is not None:
                break
        text = open(server_log, encoding="utf-8", errors="replace").read()
        errors = [l.strip() for l in text.splitlines() if re.search(r"BIP\d+[ES]:", l)]
        if not started or errors:
            print(f"RUNTIME CHECK: FAIL - {name} did not start on the integration server")
            for e in errors[:10]:
                print("  " + e[:300])
            return 1
        global SERVICE_PATH
        SERVICE_PATH = service_path(os.path.join(ws, name))
        print(f"Deployed {name} on a local integration server at {SERVICE_PATH}; mock LMS at {lms_url}")
        cases = CASES + (CHANGE_CASES if "--change" in sys.argv else [])
        results = [check(port, n, b, e) for n, b, e in cases]
        passed = sum(results)
        bad_type = [(n, t) for n, t, _ in REPLIES if "application/json" not in t]
        no_track = [n for n, _, h in REPLIES if not h]
        for label, bad in (("every reply has Content-Type application/json", bad_type),
                           ("every reply has an X-TRACKING-ID header (SRS header 6)", no_track)):
            print(f"  {'PASS' if not bad else 'FAIL'}  {label}")
            if bad:
                failures.append(label)
                print(f"        - {len(bad)} of {len(REPLIES)} replies do not, e.g. "
                      + "; ".join(f"{b[0]} -> {b[1]!r}" if isinstance(b, tuple) else b for b in bad[:2]))
        verdict = "PASS" if passed == len(results) and not failures else "FAIL"
        print(f"RUNTIME CHECK: {verdict} - {passed}/{len(results)} cases passed"
              + (f", {len(failures)} other failure(s)" if failures else "") + f" - project: {name}")
        return 0 if verdict == "PASS" else 1
    finally:
        if server and server.poll() is None:
            server.terminate()
            try:
                server.wait(10)
            except subprocess.TimeoutExpired:
                server.kill()
        # IntegrationServer runs under bash; make sure the server process itself is gone
        if not WINDOWS:
            pattern = f"IntegrationServer --work-dir {os.path.join(scratch, 'w')}"
            subprocess.run(["pkill", "-f", pattern], capture_output=True)
            for _ in range(30):  # the server shuts down gracefully; wait before deleting its work directory
                if subprocess.run(["pgrep", "-f", pattern], capture_output=True).returncode != 0:
                    break
                time.sleep(1)
        lms.shutdown()
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
