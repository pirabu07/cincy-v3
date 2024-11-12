try:
    from ccc import create_app
except ImportError as e:
    print(f'Error importing create_app from ccc: {e}')
    raise
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
