"""
Machine Learning Training Pipeline for AzureCloudHub.
Trains a dual-head text classification model for sentiment and category routing,
simulating an AI/ML microservice workload deployed on Azure App Service / ACI.
"""

import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# Synthetic dataset representing cloud telemetry tickets, user feedback, and queries
DATA = [
    # Positive Feedback
    ("Azure Kubernetes Service auto-scaling worked flawlessly during our product launch", "Positive", "Performance"),
    ("The migration from on-prem to Azure Blob storage was smooth and cut costs significantly", "Positive", "Cost"),
    ("Application Insights detected the memory leak in minutes. Amazing observability tool!", "Positive", "Monitoring"),
    ("Great customer support and very reliable 99.99% uptime across availability zones", "Positive", "Reliability"),
    ("Bicep templates make infrastructure as code deployment effortless and repeatable", "Positive", "DevOps"),
    ("Cost management budget alerts saved us from an accidental overspend last week", "Positive", "Cost"),
    ("FastAPI model serving on Azure App Service responds in under 20ms. Very satisfied!", "Positive", "Performance"),
    ("The Azure portal interface is clean and intuitive for managing resource groups", "Positive", "Usability"),
    
    # Neutral Queries & Requests
    ("How do I configure zone-redundant storage for our secondary disaster recovery region?", "Neutral", "Storage"),
    ("What is the pricing difference between Azure SQL General Purpose and Business Critical?", "Neutral", "Billing"),
    ("Can we assign Reader role to developers while keeping Contributor restricted to DevOps?", "Neutral", "Security"),
    ("Please provide documentation on connecting on-premises VNet to Azure via ExpressRoute", "Neutral", "Networking"),
    ("We need to set up a budget alert at 80% threshold for our development subscription", "Neutral", "Cost"),
    ("How do we rehydrate archived blobs from cold storage back to hot tier?", "Neutral", "Storage"),
    ("Looking for guidance on Azure Policy enforcement for tagging resource groups", "Neutral", "Governance"),
    ("What is the composite SLA for App Service with an Azure SQL backend database?", "Neutral", "Reliability"),

    # Negative Issues & Incidents
    ("Virtual machine instance terminated unexpectedly in East US with error code 500", "Negative", "Reliability"),
    ("Network latency between West Europe and Southeast Asia is spiking severely", "Negative", "Networking"),
    ("Unexpected billing spike this month due to unattached managed disks running continuously", "Negative", "Cost"),
    ("Failed to deploy ARM template due to quota limitation on vCPU cores in Central India", "Negative", "Deployment"),
    ("Blob storage access denied error 403 despite having Storage Blob Data Contributor role", "Negative", "Security"),
    ("Microservice container crashed with out of memory error during peak traffic load", "Negative", "Performance"),
    ("Our VPN Gateway disconnected during database replication causing data inconsistency", "Negative", "Networking"),
    ("The portal is failing to load resource locks for our production subscription", "Negative", "Governance")
]

def train_and_save_model(output_dir: str = "ml/model_artifacts"):
    os.makedirs(output_dir, exist_ok=True)
    
    texts = [item[0] for item in DATA]
    sentiments = [item[1] for item in DATA]
    categories = [item[2] for item in DATA]
    
    # Text vectorizer
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000, lowercase=True)
    X = vectorizer.fit_transform(texts)
    
    # Train Sentiment Classifier
    sentiment_clf = LogisticRegression(C=1.0, max_iter=200, random_state=42)
    sentiment_clf.fit(X, sentiments)
    
    # Train Category Classifier
    category_clf = LogisticRegression(C=1.0, max_iter=200, random_state=42)
    category_clf.fit(X, categories)
    
    # Save artifacts
    vectorizer_path = os.path.join(output_dir, "vectorizer.joblib")
    sentiment_path = os.path.join(output_dir, "sentiment_clf.joblib")
    category_path = os.path.join(output_dir, "category_clf.joblib")
    
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(sentiment_clf, sentiment_path)
    joblib.dump(category_clf, category_path)
    
    print(f"[OK] Model artifacts saved to: {output_dir}")
    print(f"  - Vectorizer: {vectorizer_path}")
    print(f"  - Sentiment Model: {sentiment_path}")
    print(f"  - Category Model: {category_path}")

if __name__ == "__main__":
    train_and_save_model()
