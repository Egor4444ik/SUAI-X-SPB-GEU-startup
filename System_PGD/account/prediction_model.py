import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.losses import MeanSquaredError

class PredictionModel:
    def __init__(self, model_path, categories_path, scaler_path):
        """
        Инициализация модели, загрузка категорий и MinMaxScaler.
        """
        self.model = load_model(model_path, custom_objects={'mse': MeanSquaredError()})
        with open(categories_path, 'rb') as file:
            self.categories = pickle.load(file)
        with open(scaler_path, 'rb') as file:
            self.scaler = pickle.load(file)

    def predict_next_days(self, last_sequence, num_days):
        """
        Предсказывает значения на несколько дней вперёд.
        :param last_sequence: Последовательность данных для предсказания.
        :param num_days: Количество дней для предсказания.
        :return: Декодированные предсказания.
        """
        predictions = []
        input_sequence = last_sequence.copy()

        for _ in range(num_days):
            pred = self.model.predict(np.expand_dims(input_sequence, axis=0))
            predictions.append(pred[0])

            input_sequence = np.vstack((input_sequence[1:], pred))

        predictions = np.array(predictions)
        return self.scaler.inverse_transform(predictions)

    def plot_predictions(self, predictions, start_date):
        """
        Строит график предсказаний для каждой категории.
        :param predictions: Предсказанные значения.
        """
        dates = pd.date_range(start=start_date, periods=len(predictions), freq='D')

        plt.figure(figsize=(12, 6))
        for idx, category in enumerate(self.categories):
            plt.plot(dates, predictions[:, idx], label=category)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        plt.gcf().autofmt_xdate()

        plt.title("Предсказания на следующие дни")
        plt.xlabel("Дата")
        plt.ylabel("Значение")
        plt.legend()
        plt.show()

    @staticmethod
    def prepare_data(data, sequence_length):
        """
        Подготавливает последовательности для обучения.
        :param data: Масштабированные данные.
        :param sequence_length: Длина последовательности.
        :return: X, y
        """
        X, y = [], []
        for i in range(len(data) - sequence_length):
            X.append(data[i:i + sequence_length])
            y.append(data[i + sequence_length])
        return np.array(X), np.array(y)

    @staticmethod
    def train_and_save_model(data, sequence_length, categories, model_path, categories_path, scaler_path, epochs=50):
        """
        Обучает модель и сохраняет её вместе с категориями и масштабировщиком.
        :param data: Исходные данные для обучения.
        :param sequence_length: Длина последовательности.
        :param categories: Список категорий.
        :param model_path: Путь для сохранения модели.
        :param categories_path: Путь для сохранения категорий.
        :param scaler_path: Путь для сохранения масштабировщика.
        :param epochs: Количество эпох.
        """
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data)

        os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
        with open(scaler_path, 'wb') as file:
            pickle.dump(scaler, file)

        X, y = PredictionModel.prepare_data(scaled_data, sequence_length)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        model = Sequential([
            LSTM(64, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
            Dropout(0.2),
            LSTM(32, activation='relu'),
            Dense(len(categories))
        ])
        model.compile(optimizer='adam', loss=MeanSquaredError())

        history = model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=epochs,
            batch_size=32
        )

        model.save(model_path)
        with open(categories_path, 'wb') as file:
            pickle.dump(categories, file)

        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.legend()
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.title('Training Loss')
        plt.show()

        print(f"Модель сохранена в {model_path}")
        print(f"Категории сохранены в {categories_path}")
        print(f"Масштабировщик сохранён в {scaler_path}")