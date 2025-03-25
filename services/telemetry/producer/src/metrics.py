from prometheus_client import Counter

telemetry_counter = Counter("telemetry_events_total", "Total telemetry events received")