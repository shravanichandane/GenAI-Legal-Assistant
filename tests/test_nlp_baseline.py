"""
Tests for Module 0.4 — NLP Baseline Classifier
"""

import pytest
import os
from pathlib import Path
from app.models.baseline_classifier import BaselineClauseClassifier

# ---------------------------------------------------------------------------
# Dummy Training Data for Tests
# ---------------------------------------------------------------------------
# In a real project, this would be loaded from a CSV or database.

TRAIN_DATA = [
    # INDEMNITY clauses
    "The Contractor shall indemnify, defend, and hold harmless the Client from any claims.",
    "Party A agrees to indemnify Party B against all losses and damages.",
    "Vendor will indemnify and hold the Company harmless from third-party IP claims.",
    
    # LIABILITY clauses
    "In no event shall either party be liable for any indirect, incidental, or consequential damages.",
    "Total liability under this Agreement shall not exceed the total fees paid.",
    "Limitation of Liability: The provider's liability is strictly limited.",
    
    # PAYMENT clauses
    "Client shall pay the invoice within 30 days of receipt.",
    "Payment terms are Net 45. Late payments will incur a 1.5% monthly interest rate.",
    "The total compensation for the Services shall be $10,000.",
    
    # GENERAL clauses
    "This Agreement shall be governed by the laws of the State of California.",
    "This contract constitutes the entire agreement between the parties.",
    "Any notices required under this Agreement shall be in writing."
]

TRAIN_LABELS = [
    "INDEMNITY", "INDEMNITY", "INDEMNITY",
    "LIABILITY", "LIABILITY", "LIABILITY",
    "PAYMENT", "PAYMENT", "PAYMENT",
    "GENERAL", "GENERAL", "GENERAL"
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def classifier():
    """Returns a fresh, untrained classifier instance."""
    return BaselineClauseClassifier()

@pytest.fixture
def trained_classifier(classifier):
    """Returns a classifier trained on the dummy data."""
    classifier.train(TRAIN_DATA, TRAIN_LABELS)
    return classifier

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_initialization(classifier):
    """Test that the classifier initializes correctly."""
    assert classifier.is_trained is False
    assert classifier.classes_ == []

def test_training(classifier):
    """Test the training process."""
    classifier.train(TRAIN_DATA, TRAIN_LABELS)
    assert classifier.is_trained is True
    # Should find 4 distinct classes
    assert set(classifier.classes_) == {"INDEMNITY", "LIABILITY", "PAYMENT", "GENERAL"}

def test_predict_indemnity(trained_classifier):
    """Test that the model can predict an unseen INDEMNITY clause."""
    test_clause = "The supplier agrees to indemnify and defend us against lawsuits."
    
    pred_class, confidence = trained_classifier.predict(test_clause)
    
    assert pred_class == "INDEMNITY"
    assert 0.0 <= confidence <= 1.0

def test_predict_payment(trained_classifier):
    """Test that the model can predict an unseen PAYMENT clause."""
    test_clause = "All payment of fees must be completed within thirty days."
    
    pred_class, confidence = trained_classifier.predict(test_clause)
    
    assert pred_class == "PAYMENT"
    assert 0.0 <= confidence <= 1.0

def test_predict_untrained_raises_error(classifier):
    """Calling predict on an untrained model should raise an error."""
    with pytest.raises(RuntimeError, match="Model must be trained"):
        classifier.predict("Some text")

def test_evaluate(trained_classifier):
    """Test the evaluation function."""
    # We evaluate on the training set just to verify the function works
    results = trained_classifier.evaluate(TRAIN_DATA, TRAIN_LABELS)
    
    assert "accuracy" in results
    assert "f1_macro" in results
    assert "report" in results
    # Since it's evaluated on its own tiny training data, it should do very well
    assert results["accuracy"] > 0.8

def test_save_and_load_model(trained_classifier, tmp_path):
    """Test saving the model to disk and loading it back."""
    model_path = tmp_path / "test_model.pkl"
    
    # Save it
    trained_classifier.save_model(str(model_path))
    assert os.path.exists(model_path)
    
    # Load it into a new instance
    new_classifier = BaselineClauseClassifier()
    new_classifier.load_model(str(model_path))
    
    assert new_classifier.is_trained is True
    assert set(new_classifier.classes_) == {"INDEMNITY", "LIABILITY", "PAYMENT", "GENERAL"}
    
    # Predictions should match
    text = "Client shall pay the invoice."
    pred1, conf1 = trained_classifier.predict(text)
    pred2, conf2 = new_classifier.predict(text)
    
    assert pred1 == pred2
    assert conf1 == conf2
