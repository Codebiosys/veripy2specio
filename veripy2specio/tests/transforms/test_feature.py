import pytest
from veripy2specio.tests.fixtures import veripy_feature
from veripy2specio import constants


def test_feature_properties():
    from veripy2specio.transforms.feature import Feature

    valid_feature = Feature(veripy_feature.feature_no_scenarios)
    serialized_feature = valid_feature.serialize()
    # Base Props
    assert valid_feature.source == veripy_feature.feature_no_scenarios
    assert valid_feature.keyword == constants.Keyword.FEATURE
    assert serialized_feature['keyword'] == "Feature"
    assert valid_feature.name == "veripy outputs a result"
    assert serialized_feature['name'] == "veripy outputs a result"
    assert not valid_feature.passed
    assert not serialized_feature['passed']
    assert valid_feature.feature_number == 1
    assert serialized_feature['feature_number'] == 1
    assert valid_feature.id == 'id_123'
    assert serialized_feature['id'] == 'id_123'
    assert valid_feature.status == constants.Status.SKIPPED
    assert serialized_feature['status'] == 'Skipped'
    assert valid_feature.description == "<p>A description of the test</p>\n"
    assert serialized_feature['description'] == "<p>A description of the test</p>\n"
    assert next(valid_feature.tags)['last']
    assert serialized_feature['tags'][0]['last']
    assert next(valid_feature.tags)['name'] == 'Test1'
    assert serialized_feature['tags'][0]['name'] == 'Test1'
    assert not valid_feature.has_scenarios
    assert not serialized_feature['has_scenarios']
    assert not valid_feature.has_prerequisites
    assert not serialized_feature['has_prerequisites']


@pytest.mark.parametrize("no_doc_feature", [
    veripy_feature.feature_no_doc,
    veripy_feature.feature_empty_doc,
    veripy_feature.feature_pre_only_doc,
])
def test_no_description(no_doc_feature):
    from veripy2specio.transforms.feature import Feature

    valid_feature = Feature(no_doc_feature)
    serialized_feature = valid_feature.serialize()
    # Base Props

    assert not valid_feature.description
    assert 'description' not in serialized_feature
