"""Template discovery helpers for github.sh."""

ISSUE_TEMPLATE_DIR = ".github/ISSUE_TEMPLATE/"
ISSUE_TEMPLATE_LEGACY_PATHS = (".github/ISSUE_TEMPLATE.md", "ISSUE_TEMPLATE.md")

ISSUE_TEMPLATE_CONFIG_PATHS = frozenset({
    f"{ISSUE_TEMPLATE_DIR.lower()}config.yml",
    f"{ISSUE_TEMPLATE_DIR.lower()}config.yaml",
})


def is_issue_template_config_path(path):
    """Return True for GitHub issue-template chooser config files."""
    return path.lower() in ISSUE_TEMPLATE_CONFIG_PATHS


def issue_template_dir_paths(paths, *, extensions=None):
    """Return issue-template directory files, excluding chooser config files."""
    return sorted(
        p for p in paths
        if p.startswith(ISSUE_TEMPLATE_DIR)
        and not is_issue_template_config_path(p)
        and (extensions is None or p.endswith(extensions))
    )
