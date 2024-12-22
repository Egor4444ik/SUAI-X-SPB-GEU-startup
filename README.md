# Как пользоваться PredictionModel

пример входных данных на нейросеть

```csv
order_date,fuel,cinema,vkusvill,travel,restaurants,concerts,games,books,theater,sports,beauty,flowers,technology
2022-01-01,0,128,0,5,0,0,0,1,2,0,0,0,0
2022-01-02,0,145,0,3,0,0,0,0,0,0,0,0,0
2022-01-03,0,142,0,6,0,2,0,0,1,0,0,0,0
```

пример преобразования таблицы в подобные данные

```python
import pandas as pd

file_path = 'data/dano_xakaton_filled_sessions_original.csv'
df = pd.read_csv(file_path)

categories = ['fuel', 'cinema', 'vkusvill', 'travel', 'restaurants', 'concerts', 
              'games', 'books', 'theater', 'sports', 'beauty', 'flowers', 'technology']

result = df.groupby('order_date')[categories].sum().reset_index()

output_path = 'data/result.csv'
result.to_csv(output_path, index=False)
```

пример кода

```python
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler
from prediction_model import PredictionModel

data_file = "data/result.csv"
df = pd.read_csv(data_file)

last_date = pd.to_datetime(df['order_date']).max()
print(f"Последняя дата в таблице: {last_date}")

data = df.drop(columns=['order_date']).values
categories = list(df.columns[1:])

categories_path = 'data/test_categories.pkl'
with open(categories_path, 'wb') as file:
    pickle.dump(categories, file)

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

scaler_path = 'data/test_scaler.pkl'
with open(scaler_path, 'wb') as file:
    pickle.dump(scaler, file)

sequence_length = 200  # Как далеко анализируем
X, y = PredictionModel.prepare_data(scaled_data, sequence_length)

model_path = 'data/test_model.h5'
PredictionModel.train_and_save_model(data, sequence_length, categories, model_path, categories_path, scaler_path, epochs=20)

model = PredictionModel(model_path, categories_path, scaler_path)
last_sequence = scaled_data[-sequence_length:]

predictions = model.predict_next_days(last_sequence, 30)
model.plot_predictions(predictions, start_date=last_date.strftime('%Y-%m-%d'))
```
