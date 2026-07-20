"""
═══════════════════════════════════════════════════════════════════════
 NOVA-X DAEMON PACKAGE
 Persistent Background Runtime for NOVA-X

 This package provides:

 • Daemon lifecycle management
 • Event scheduling
 • Service supervision
 • Heartbeat monitoring
 • Mission management
 • Plugin loading

 Author: Douglas Davis & OpenAI
 Version: 1.0.0
═══════════════════════════════════════════════════════════════════════
"""

__version__ = "1.0.0"
__author__ = "Douglas Davis"

DAEMON_NAME = "NOVA-X Daemon"

RUNNING = "running"
STOPPED = "stopped"
STARTING = "starting"
STOPPING = "stopping"

DEFAULT_SLEEP = 5
DEFAULT_HEARTBEAT = 30
