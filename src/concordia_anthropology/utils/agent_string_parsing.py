import re
from typing import Sequence, Tuple, Optional
from concordia.components.game_master.event_resolution import PUTATIVE_EVENT_TAG, EVENT_TAG

TAG_RE = re.compile(r'^\s*(\[[^\]]+\])\s*(.*)$')
QUOTED_RE = re.compile(r'"([^"]+)"')

def split_tags_and_payload(observation: str, known_tags: Sequence[str] = (PUTATIVE_EVENT_TAG, EVENT_TAG)) -> Tuple[list[str], str]:
    s = observation.strip()
    tags: list[str] = []
    if observation == "":
      return (tags, "")

    for tag in known_tags:
        if s.startswith(tag + " "):
            tags.append(tag)
            s = s[len(tag):].lstrip()
            break
        if s == tag:
            tags.append(tag)
            return tags, ""
    return tags, s


def parse_actor_and_content(payload: str, candidates: list[str]) -> Tuple[Optional[str], str]:
    s = payload.strip()
    # Longest-first to avoid prefix shadowing
    for name in sorted(candidates, key=len, reverse=True):

        m = re.match(rf'^{re.escape(name)}(\b|[:\s—–-])?(.*)$', s)
        if m:
            rest = m.group(2).lstrip()
            # Clean common “separator noise” once
            rest = rest.lstrip(':—–-').lstrip()
            return name, rest

    # Fallback: "Name: rest"
    if ':' in s:
        actor, rest = s.split(':', 1)
        actor = actor.strip()
        if actor in candidates:
            return actor, rest.lstrip()
    return None, s


# TODO: I might not need this...
def extract_text(content: str) -> str:
    """
    Prefer a quoted segment if present; otherwise return the remaining content.
    """
    m = QUOTED_RE.search(content)
    if m:
        return m.group(1).strip()
    return content.strip()