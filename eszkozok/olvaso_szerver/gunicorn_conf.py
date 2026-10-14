"""gunicorn-beállítás az olvasói szerverhez (#76 M2, M0 3.8): 1 worker, 4 szál (gthread) — a VPS-t utánzó 1 vCPU / 2 GB-hoz.

Indítás (az `olvaso_szerver` könyvtárból):
    PARDES_DB=/út/a/pardes.db gunicorn -c gunicorn_conf.py "alkalmazas:letrehoz()"
A hozzáférési napló az útvonalat írja, a lekérdezés-szöveget (a `?szo=…` stb.) nem (`%(U)s` = út query nélkül; M0 3.7).
"""
import os

chdir = os.path.dirname(os.path.abspath(__file__))
bind = os.environ.get('PARDES_BIND', '127.0.0.1:8000')
worker_class = 'gthread'
workers = 1
threads = 4
timeout = 60
keepalive = 5
accesslog = '-'
access_log_format = '%(h)s %(m)s %(U)s %(s)s %(L)s'
errorlog = '-'
