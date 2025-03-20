"""
Configuration settings for the BPMN Cloud Upload Tool.

This module contains default configuration values used throughout the application.
"""

# Default Celonis API URL
DEFAULT_CELONIS_BASE_URL = "https://bosch.eu-4.celonis.cloud/process-repository/api/v1"

# Default proxy settings
DEFAULT_PROXY_HOST = "rb-proxy-unix-de01.bosch.com"
DEFAULT_PROXY_PORT = "8080"

# Cache settings (in seconds)
API_CACHE_TTL = 300  # 5 minutes

# File upload settings
ALLOWED_BPMN_EXTENSIONS = ['bpmn', 'xml']
MAX_PREVIEW_CHARS = 2000  # Maximum characters to show in XML preview