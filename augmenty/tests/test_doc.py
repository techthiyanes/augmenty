import pytest

import augmenty

from spacy.lang.en import English
from spacy.tokens import Span


@pytest.fixture()
def nlp():
    nlp = English()
    return nlp


def test_create_spongebob_augmenter(nlp):
    spongebob_augmenter = augmenty.load("spongebob.v1", level=1)
    texts = ["A sample text"]
    aug_text = "A SaMpLe tExT"

    aug_texts = list(augmenty.texts(texts, spongebob_augmenter, nlp))
    assert aug_texts[0] == aug_text


def test_create_upper_case_augmenter(nlp):
    spongebob_augmenter = augmenty.load("upper_case.v1", level=1)
    texts = ["A sample text"]
    aug_text = "A SAMPLE TEXT"

    aug_texts = list(augmenty.texts(texts, spongebob_augmenter, nlp))
    assert aug_texts[0] == aug_text


def test_paragraph_subset_augmenter(nlp):
    text = (
        "My name is Kenneth Enevoldsen. "
        + "Augmenty is a wonderful tool for augmentation. "
        + "It have tons of different augmenters. Augmenty is developed using spaCy."
    )
    doc = nlp(text)
    doc.set_ents(
        [
            Span(doc, 3, 5, label="person"),
            Span(doc, 6, 7, label="ORG"),
            Span(doc, 21, 22, label="ORG"),
        ]
    )

    def __assign(t):
        t.is_sent_start = True if t.text == "." else False

    [__assign(t) for t in doc]

    p_subset_aug = augmenty.load(
        "paragraph_subset_augmenter.v1", min_paragraph=1, max_paragraph=1.00
    )
    aug_docs = list(augmenty.docs([doc], p_subset_aug, nlp))
    assert aug_docs[0].text

    # with sentencizer
    nlp.add_pipe("sentencizer")
    aug_texts = list(augmenty.texts([text], p_subset_aug, nlp))
    assert aug_texts[0]

    # full length
    p_subset_aug = augmenty.load(
        "paragraph_subset_augmenter.v1", min_paragraph=1.0, max_paragraph=1.0
    )
    aug_docs = list(augmenty.docs([doc], p_subset_aug, nlp))
    assert aug_docs[0].text == text

    # zero length
    p_subset_aug = augmenty.load(
        "paragraph_subset_augmenter.v1", min_paragraph=0.0, max_paragraph=0.0
    )
    aug_docs = list(augmenty.docs([doc], p_subset_aug, nlp))
    assert aug_docs[0].text == ""
