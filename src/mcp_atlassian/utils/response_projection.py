"""Small, explicit projections for agent-facing Atlassian results."""

from __future__ import annotations

from typing import Any

JIRA_BRIEF_FIELDS = "summary,status,assignee,priority,updated,issuetype,labels"
_JIRA_BRIEF_KEYS = frozenset(
    {
        "id",
        "key",
        "summary",
        "status",
        "assignee",
        "priority",
        "updated",
        "issue_type",
        "labels",
        "browse_url",
    }
)


def jira_browse_url(base_url: str, issue_key: str) -> str:
    """Build the human-facing issue URL from the configured Jira site."""
    return f"{base_url.rstrip('/')}/browse/{issue_key}"


def brief_jira_search(result: dict[str, Any], base_url: str) -> dict[str, Any]:
    """Keep navigation and triage fields while excluding full issue bodies."""
    issues = result.get("issues", [])
    return {
        **{key: value for key, value in result.items() if key != "issues"},
        "issues": [
            {
                **{
                    key: value
                    for key, value in issue.items()
                    if key in _JIRA_BRIEF_KEYS
                },
                "browse_url": jira_browse_url(base_url, issue["key"]),
            }
            for issue in issues
        ],
    }


def confluence_page_metadata(page: dict[str, Any]) -> dict[str, Any]:
    """Keep page identity, version and attachment manifest, omit body text."""
    content = page.get("content") or {}
    value = content.get("value", "") if isinstance(content, dict) else ""
    return {
        **{key: value for key, value in page.items() if key != "content"},
        "has_content": bool(value),
        "content_characters": len(value),
    }
