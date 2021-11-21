"""Test of the image_classification module"""
from panel_ai.image.base.pillow import IMAGE_EXAMPLES
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


def test_can_load_from_url():
    """Can load and image from a url"""
    classifier = ImageClassifier()
    assert not classifier.image
    classifier.load_image(IMAGE_EXAMPLES[0].url)
    assert classifier.image


def test_can_instantiate_with_image_argument():
    """We can provide an image as argument"""
    # Given
    tmp = ImageClassifier()
    tmp.load_image(IMAGE_EXAMPLES[0].url)
    image = tmp.image
    # When
    classifier = ImageClassifier(image=image)
    # Then
    assert classifier.image == image
