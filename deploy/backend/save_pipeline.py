from joblib import dump
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from preprocessing import preprocess_data  # Import from the new file

# Preprocessing Pipeline
preprocessing_pipeline = Pipeline([
    ("preprocessing", FunctionTransformer(preprocess_data))
])

# Save the pipeline
dump(preprocessing_pipeline, "preprocessing_pipeline.joblib")