"""Test of the image_classification module"""
from panel_ai.image.image_classification import ImageClassifier, dummy_model


def test_image_classifier_constructor_no_args():
    """Can construct ImageClassifier without arguments"""
    ImageClassifier()


def test_can_change_example():
    """Can change the example image of the ImageClassifier"""
    # Given
    classifier = ImageClassifier(model=dummy_model)
    image = classifier.image
    # When
    classifier.example = classifier.param.example.objects[1]
    # Then
    assert classifier.image
    assert classifier.image != image
