## yms-appt-service (FastAPI)

### Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open:
- `http://localhost:8000/health`
- `http://localhost:8000/docs`

### MongoDB config

Set environment variables (example in `.env.example`):
- `MONGODB_URI` (default: `mongodb://localhost:27017`)
- `MONGODB_DB` (default: `yms_appt_service`)

### Run tests

```bash
pip install -r requirements-dev.txt
pytest
```

### Build & run with Docker

```bash
docker build -t yms-appt-service:latest .
docker run --rm -p 8000:8000 yms-appt-service:latest
```

### Helm (Kubernetes) deployments

Chart: `helm/yms-appt-service`

Environment values:
- `helm/environments/qa-int.values.yaml`
- `helm/environments/qa-stage.values.yaml`
- `helm/environments/sandbox.values.yaml`
- `helm/environments/production.values.yaml`

Example install/upgrade:

```bash
helm upgrade --install yms-appt-service helm/yms-appt-service \
  -f helm/environments/qa-int.values.yaml \
  --namespace yms --create-namespace
```

Note: the `mongodbUri` values in the environment files are placeholders; replace with real credentials
or inject via your secret manager (recommended).

