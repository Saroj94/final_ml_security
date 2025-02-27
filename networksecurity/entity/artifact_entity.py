from dataclasses import dataclass

"""Dataclass is basically used to create only variables inside the class. It is actually acts 
like a decorator which will creates the variable for empty class. Let's say in my class 
i don't have functions, i just need to have variables define inside the class or class variable.
"""

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str


@dataclass
class DataValidationArtifact:
    validation_Status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str