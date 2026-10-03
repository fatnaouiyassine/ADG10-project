"""Journal local des actions externes pour eviter les doubles envois."""

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from config import settings


class DispatchLedger:
    def __init__(self, path: Path | None = None):
        self.path = path or settings.state_dir / "dispatch_log.json"

    def _read(self) -> dict[str, dict[str, Any]]:
        if not self.path.exists():
            return {}
        try:
            content = json.loads(self.path.read_text(encoding="utf-8"))
            return content if isinstance(content, dict) else {}
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                f"Le journal d'envoi est illisible : {self.path}"
            ) from exc

    def has(self, event_key: str) -> bool:
        return event_key in self._read()

    def get(self, event_key: str) -> dict[str, Any] | None:
        return self._read().get(event_key)

    def find(self, **criteria: Any) -> dict[str, Any] | None:
        for event_key, metadata in self._read().items():
            candidate = {"event_key": event_key, **metadata}
            if all(candidate.get(key) == value for key, value in criteria.items()):
                return candidate
        return None

    def mark(self, event_key: str, metadata: dict[str, Any] | None = None) -> None:
        entries = self._read()
        entries[event_key] = {
            "sent_at": datetime.now(timezone.utc).isoformat(),
            **(metadata or {}),
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(".tmp")
        temporary_path.write_text(
            json.dumps(entries, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary_path.replace(self.path)

    def recent(self, limit: int = 20) -> list[dict[str, Any]]:
        entries = [dict(event_key=key, **value) for key, value in self._read().items()]
        return sorted(entries, key=lambda item: item.get("sent_at", ""), reverse=True)[:limit]


def dispatch_key(
    record_id: str,
    sequence: str,
    day: int,
    anchor_date: str,
    channel: str,
) -> str:
    return ":".join(
        [record_id, sequence.lower(), f"j{day}", anchor_date or "sans-date", channel.lower()]
    )
