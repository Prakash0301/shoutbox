from flask import Flask, request, redirect
import redis, os

app = Flask(__name__)
r = redis.Redis(host=os.environ['REDIS_HOST'], port=6379, decode_responses=True)

@app.route('/')
def index():
    msgs = r.lrange('shouts', 0, 20)
    items = "".join(f"<li>{m}</li>" for m in msgs)
    return f'''
    <html><body style="font-family:sans-serif;max-width:500px;margin:60px auto;
    background:#0d1117;color:#e6edf3;padding:30px;border-radius:10px;">
      <h1 style="color:#58a6ff;">📣 Shoutbox</h1>
      <form method="POST" action="/add">
        <input name="msg" placeholder="Shout something..." style="padding:8px;width:70%;">
        <button style="padding:8px 16px;">Post</button>
      </form>
      <ul>{items}</ul>
    </body></html>
    '''

@app.route('/add', methods=['POST'])
def add():
    msg = request.form.get('msg')
    if msg:
        r.lpush('shouts', msg)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
