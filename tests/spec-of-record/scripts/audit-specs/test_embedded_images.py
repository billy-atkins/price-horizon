"""The audit's check that no spec embeds an image: an image by a link, by a reference label or by an HTML tag in a
file under the specs is reported, while image syntax in a code span or a fenced block, and an image in a file outside
the specs, pass."""
import pytest

from audit_set import spec_checks

pytestmark = [pytest.mark.reads("audit-embedded-images.md", "image-syntax-in-code", "image-inline", "image-by-reference",
                                "image-tag")]


# @canon-spec specs/methodology/modeling-constructs.md § Diagrams
@pytest.mark.action("--check-scope")
@pytest.mark.passes
@pytest.mark.parametrize("key, path", [
    ("image-syntax-in-code", "specs/harbor.md"),
    ("image-inline", "docs/harbor.md"),
])
def test_no_image_embedded_in_a_spec_passes(fixtures, key, path):
    assert spec_checks.image_findings(path, fixtures[key]) == []


# @canon-spec specs/methodology/modeling-constructs.md § Diagrams
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key", ["image-inline", "image-by-reference", "image-tag"])
def test_an_image_embedded_in_a_spec_is_reported(fixtures, key):
    assert [(line, message) for _, line, message in spec_checks.image_findings("specs/harbor.md", fixtures[key])] == [
        (5, "embeds an image rather than a diagram's source")]
