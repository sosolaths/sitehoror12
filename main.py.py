import os
from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# УЛУЧШЕННЫЙ МАРШРУТ С ПОТОКОВОЙ ОТДАЧЕЙ (ДЛЯ БОЛЬШИХ ФАЙЛОВ)
@app.route('/download-game')
def download_game():
    # Полный путь к архиву внутри папки static
    file_path = os.path.join(app.root_path, 'static', 'horor_gmae.zip')

    # Если вдруг забыли перенести файл в static, Python вежливо предупредит
    if not os.path.exists(file_path):
        return "Ошибка: Файл 'horor_gmae.zip' не найден в папке static!", 404

    # Функция-генератор: читает архив по кусочкам (chunks) в памяти
    def generate():
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(1024 * 1024)  # Читаем по 1 Мегабайту за раз
                if not chunk:
                    break
                yield chunk

    # Отправляем поток байтов в браузер как скачиваемый архив
    return Response(
        generate(),
        mimetype='application/zip',
        headers={'Content-Disposition': 'attachment; filename=horor_gmae.zip'}
    )


if __name__ == '__main__':
    app.run(debug=True)