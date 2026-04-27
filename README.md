# 🌐 Code-Mixed Language Detector

A simple Flask web app to detect and analyze code-mixed sentences in English, Hindi, Telugu, and Tamil! 🚦

## 🚀 Features

- Detects the language of each word in a sentence
- Identifies if a sentence is code-mixed
- Shows the dominant language

## 🛠️ How to Run

1. (Optional) Create a virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install Flask:
   ```cmd
   pip install flask
   ```
3. Start the app:
   ```cmd
   python app.py
   ```
4. Open your browser and go to:
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## 📝 Sample Input

```
nenu system kyun inka nuvvu result theek ippudu
```

## 📁 Project Structure

```
app.py
generated_dataset.json
templates/
    index.html
```

## 🤝 Contributing

Pull requests are welcome!

## 📜 License

MIT
