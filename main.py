"""Small entry point: reserve Wi-Fi before importing the real application."""

def start():
    print('[Main] socket-v3: starting application')
    from startup import reserve_wifi, configure_runtime, report_memory
    try:
        reserve_wifi()
        configure_runtime()
        import gc
        gc.collect()
        from app import run
        run()
        return True
    except Exception as error:
        print('[Fatal Error]', type(error).__name__, str(error))
        report_memory('startup-stopped')
        return False


if __name__ == '__main__':
    start()
