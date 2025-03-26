from website import create_app

app = create_app()

if __name__ == '__main__':
    # debug means everytime we make a change it will rerun the website
    app.run(debug=True)