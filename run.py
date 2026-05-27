from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # This builds your local SQLite database file instantly inside the folder
        db.create_all()
    
    print("\n[SUCCESS] NetLogic Secure Kernel Online.")
    print("[RUNNING] Operational Portal: http://127.0.0.1:5000/\n")
    app.run(host='127.0.0.1', port=5000, debug=True)