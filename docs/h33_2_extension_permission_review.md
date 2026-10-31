# H33.2 Extension Permission Review

`extension/manifest.json` no longer requests `<all_urls>`. Content-script and web-accessible-resource matches are limited to HTTPS YouTube/YouTube short-link pages and the project's HTTP loopback viewer origins. Host permissions are limited to those YouTube hosts and `localhost` / `127.0.0.1`; existing `storage` and `activeTab` permissions remain.

The local API accepts only the extension ID configured when starting the viewer, e.g. `tools\\run_avatar_viewer.py --port 8000 --extension-id <ID>`. The README explains how to retrieve the ID for a locally unpacked extension. If no ID is configured, the viewer remains usable directly but extension API calls fail closed.

Manifest JSON and code-level checks pass. No installed-browser YouTube overlay test was run; injection, iframe behavior, and extension-origin API calls still require manual Chrome acceptance.
