from flask import Flask, jsonify, render_template
import pandas as pd
import json
import csv
import os

path = os.getcwd() + "/FlaskServer/"

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

df = pd.read_csv(path + "titanic.csv")

# Удаление пропусков
df.dropna(subset=['Age'], inplace=True)

# Обновление индексов (на всякий случай)
df.reset_index(drop=True, inplace=True)

df_query = df[(df['Age'] > 18) & (df['Survived'] == 1)]

# Удалёем столбец Survived
df_query.drop('Survived', axis=1, inplace=True)

# Сортируем по возрасту 
df_query.sort_values(by=['Age'], inplace=True, ascending=True)

headers = list(df_query.columns)
items = list(df_query.values)[:10] # Выборка топ 10

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html", items=items, headers=headers)

@app.route('/data.json', methods=['GET'])
def data():
	result = df.to_json(orient="records")
	return jsonify(json.loads(result))

if __name__ == '__main__':
	app.run()
