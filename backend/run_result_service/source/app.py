from backend.run_result_service.source import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
