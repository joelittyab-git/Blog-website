from routes import app, socket

#app runner
app.run(
    host='localhost',
    port=1000,
    debug=True,
)
