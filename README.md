# Zenith image-build verification app

A throwaway self-hosted web notes app for testing Zenith developer onboarding. It uses Python 3.12 or newer and only standard-library modules. Each customer runs a separate process with a separate SQLite database. No container image exists for this app, and this repository deliberately starts with no Dockerfile or workflow.

Run `DATA_DIR=./data PORT=8080 python app.py`, then open http://localhost:8080. POSTing the HTML form stores a note in DATA_DIR/notes.sqlite3. GET /api/notes reads the stored notes, and GET /health reports readiness. Data must survive container replacement on a persistent volume. No external services or credentials are needed.

This is a verification fixture, not a product for publication. License MIT. Created solely for ZENITH-206 image build and registry proof.
