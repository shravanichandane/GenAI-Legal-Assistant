import pytest
from app.models.legal_bert_classifier import LegalBertClassifier

def test_legal_bert_classifier_initialization():
    classifier = LegalBertClassifier()
    assert classifier.classifier is not None
    assert "LIABILITY" in classifier.labels
    assert "GENERAL" in classifier.labels

def test_legal_bert_classifier_predict():
    classifier = LegalBertClassifier()
    
    # Test a clear indemnification clause
    text = "The Company shall indemnify and hold harmless the Client against any and all claims, damages, and losses arising from the breach of this Agreement."
    label, confidence = classifier.predict(text)
    
    assert label in ["INDEMNITY", "LIABILITY"]
    assert confidence > 0.0
    
    # Test an empty text
    label, confidence = classifier.predict("")
    assert label == "GENERAL"
    assert confidence == 0.0
