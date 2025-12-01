import os

bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"
workers = 1
worker_class = "sync"
timeout = 240
loglevel = "info"
