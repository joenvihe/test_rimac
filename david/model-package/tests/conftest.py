import pytest

from classifier_model.config.core import config
from classifier_model.processing.data_manager import load_dataset, load_from_s3


@pytest.fixture()
def sample_input_data():
    # return load_dataset(file_name=config.app_config.test_data_file)
    return load_from_s3(file_name=config.app_config.test_data_file)
