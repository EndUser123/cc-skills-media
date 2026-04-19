"""
Test corpus for nlm-to-wiki skill.

These fixtures cover:
- slug generation and collision detection
- query response parsing (good, malformed, empty)
- YAML frontmatter serialization round-trips
"""

# === SLUG COLLISION TEST CASES ===
# These pairs of concept names should produce colliding slugs
SLUG_COLLISION_PAIRS = [
    # Same lowercase after slugification
    ("Machine Learning", "machine-learning"),
    ("Machine-learning", "machine-learning"),
    ("MACHINE LEARNING", "machine-learning"),
    # Different hyphens
    ("DevOps Pipeline", "devops-pipeline"),
    ("Devops-Pipeline", "devops-pipeline"),
    ("DevOps-Pipeline", "devops-pipeline"),
]

# Valid slugs that should NOT collide
VALID_SLUGS = [
    "machine-learning",
    "deep-learning",
    "neural-networks",
    "transformer-models",
    "rag-systems",
]


# === QUERY RESPONSE TEST CASES ===

# Well-formed response with 3 concepts
WELL_FORMED_RESPONSE = """## Machine Learning
A technique that enables computers to learn from data without being explicitly programmed.

## Deep Learning
A subset of machine learning using neural networks with multiple layers.

## Transformer Models
Architecture that uses self-attention mechanisms for processing sequential data.
"""

# Single monolithic concept (no sub-headings)
MONOLITHIC_RESPONSE = """Machine learning is a technique that enables computers to learn from data without being explicitly programmed. It encompasses various approaches including supervised learning, unsupervised learning, and reinforcement learning."""

# Empty response (no content)
EMPTY_RESPONSE = ""

# Response with only one heading
SINGLE_CONCEPT_RESPONSE = """## Machine Learning
A technique that enables computers to learn from data without being explicitly programmed."""

# Malformed response (no ## prefix, but has content)
MALFORMED_NO_HEADING = """Machine Learning
A technique that enables computers to learn from data.

Deep Learning
A subset of machine learning using neural networks.
"""

# Response with extra whitespace
WHITESPACE_RESPONSE = """##   Machine Learning

A technique that enables computers to learn.

## Deep Learning

A subset of ML.
"""


# === FRONTMATTER YAML TEST CASES ===

VALID_FRONTMATTER = {
    "nlm_sync": {
        "version": "1.0",
        "notebook_id": "abc12345-def6-7890",
        "notebook_title": "AI Research Notes",
        "synced_at": "2026-04-09",
        "source_ids": [],
        "query_prompt": "For each major concept...",
    },
    "provenance": [
        {
            "claim": "Machine learning enables computers to learn from data",
            "source_id": "src-001",
            "cited_text": "Machine learning is a technique...",
        }
    ],
    "sources": [{"id": "abc12345", "title": "AI Research Notes"}],
    "tags": ["nlm-synced"],
    "created": "2026-04-09",
}


# Minimal frontmatter (all required fields)
MINIMAL_FRONTMATTER = {
    "nlm_sync": {
        "version": "1.0",
        "notebook_id": "abc12345",
        "notebook_title": "Test",
        "synced_at": "2026-04-09",
        "source_ids": [],
        "query_prompt": "",
    },
    "provenance": [],
    "sources": [],
    "tags": ["nlm-synced"],
    "created": "2026-04-09",
}


def slug_from_concept_name(name: str) -> str:
    """Slug generation matching SKILL.md specification."""
    slug = name.lower().replace(" ", "-")
    if len(slug) > 50:
        slug = slug[:50]
    return slug


def test_slug_collision():
    """Verify slug collision pairs produce identical slugs."""
    for concept_name, expected_slug in SLUG_COLLISION_PAIRS:
        assert slug_from_concept_name(concept_name) == expected_slug


def test_valid_slugs_unique():
    """Verify valid slugs are all unique."""
    slugs = [slug_from_concept_name(name) for name in VALID_SLUGS]
    assert len(slugs) == len(set(slugs)), "Valid slugs should be unique"


def test_parse_well_formed():
    """Well-formed response should produce 3 concepts."""
    concepts = [c.strip() for c in WELL_FORMED_RESPONSE.split("##") if c.strip()]
    assert len(concepts) == 3


def test_parse_monolithic():
    """Monolithic response produces 1 blob (whole text as single chunk).

    The parse validation should detect this: a single chunk without
    a heading-formatted title should be flagged as invalid, not
    treated as a valid concept.
    """
    concepts = [c.strip() for c in MONOLITHIC_RESPONSE.split("##") if c.strip()]
    assert len(concepts) == 1
    # The single chunk has no "## " heading — validation must catch this
    assert not concepts[0].startswith("## ")


def test_parse_empty():
    """Empty response should produce 0 concepts."""
    concepts = [c.strip() for c in EMPTY_RESPONSE.split("##") if c.strip()]
    assert len(concepts) == 0


def test_parse_single():
    """Single-heading response should produce 1 concept."""
    concepts = [c.strip() for c in SINGLE_CONCEPT_RESPONSE.split("##") if c.strip()]
    assert len(concepts) == 1


# === SYNC MANIFEST TEST CASES ===

MANIFEST_SCHEMA = {
    "notebook_id": str,
    "notebook_title": str,
    "last_synced_at": str,
    "source_ids": list,
    "concept_slugs": list,
}

def test_manifest_schema_valid():
    """Manifest JSON must have required fields."""
    manifest = {
        "notebook_id": "abc12345-def6-7890",
        "notebook_title": "AI Research Notes",
        "last_synced_at": "2026-04-09",
        "source_ids": ["src-001", "src-002"],
        "concept_slugs": ["machine-learning", "deep-learning"],
    }
    for field, field_type in MANIFEST_SCHEMA.items():
        assert field in manifest, f"Missing field: {field}"
        assert isinstance(manifest[field], field_type), f"Wrong type for {field}"


def test_manifest_source_comparison():
    """When source_ids match manifest, skip query."""
    prior = {
        "notebook_id": "abc12345",
        "source_ids": ["src-001", "src-002"],
    }
    current = ["src-001", "src-002"]
    # Set comparison: identical sets means no new sources
    assert set(prior["source_ids"]) == set(current), "Sources should match"


def test_manifest_new_source_detected():
    """When source_ids differ, new sources exist."""
    prior = {
        "notebook_id": "abc12345",
        "source_ids": ["src-001", "src-002"],
    }
    current = ["src-001", "src-002", "src-003"]
    assert len(set(current) - set(prior["source_ids"])) > 0, "New source should be detected"


def test_manifest_source_removed():
    """When prior has source not in current, source was removed."""
    prior = ["src-001", "src-002"]
    current = ["src-001"]
    assert len(set(prior) - set(current)) > 0, "Removed source should be detected"
