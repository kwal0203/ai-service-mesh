# Linkerd Viz Dashboard (Screenshot)

This chunk enables the Linkerd viz dashboard and captures a screenshot for the demo.

## Install Viz (If Needed)
```bash
linkerd viz install | kubectl apply -f -
linkerd viz check
```

## Launch the Dashboard
```bash
linkerd viz dashboard --address 127.0.0.1 --port 8084
```
Then open `http://127.0.0.1:8084` in your browser.

## Capture Screenshot
- Navigate to the `Namespace` or `Deployments` view for the `demo` namespace.
- Capture a screenshot showing the service stats/traffic split.
- Save it as `docs/screenshots/linkerd-viz-dashboard.png`.
