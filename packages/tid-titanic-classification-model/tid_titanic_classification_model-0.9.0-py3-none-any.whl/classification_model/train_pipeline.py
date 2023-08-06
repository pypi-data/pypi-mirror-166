from config.core import config
from pipeline import titanic_pipe
from preprocessing.data_manager import load_dataset
from sklearn.model_selection import train_test_split

from classification_model.preprocessing.data_manager import save_pipeline


def run_training() -> None:
    data = load_dataset()

    X_train, _, y_train, _ = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],  # target
        test_size=config.model_config.test_size,  # percentage of obs in test set
        random_state=config.model_config.seed,
    )  # seed to ensure reproducibility

    titanic_pipe.fit(X_train, y_train)

    save_pipeline(titanic_pipe)


if __name__ == "__main__":
    run_training()
