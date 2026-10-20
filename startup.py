"""Reserve ESP-IDF Wi-Fi buffers before importing the application."""
import gc
import sys

_station = None
_failure = None


def configure_gc():
    gc.collect()
    threshold = getattr(gc, 'threshold', None)
    if threshold is not None:
        # Collect temporary allocations before a burst can grow the GC heap
        # into ESP-IDF's remaining networking memory. This is a heuristic.
        threshold(8192)


def report_memory(stage):
    gc.collect()
    free = getattr(gc, 'mem_free', None)
    if free:
        print('[Memory]', stage, 'gc_free=', free())
    try:
        import esp32
        regions = esp32.idf_heap_info(esp32.HEAP_DATA)
        print('[Memory]', stage, 'IDF (free, largest)=',
              [(region[1], region[2]) for region in regions])
    except (ImportError, AttributeError, OSError, MemoryError):
        pass


def reserve_wifi():
    global _station, _failure
    if _failure is not None:
        # A partially failed native driver must not be retried in a tight loop.
        raise OSError(_failure)
    if _station is not None:
        configure_gc()
        return _station
    print('[Boot] socket-v3: reserving WiFi before application imports')
    report_memory('before-wifi')
    try:
        import network
        _station = network.WLAN(network.STA_IF)
        _station.active(True)
    except (OSError, MemoryError) as error:
        _station = None
        _failure = str(error)
        print('[Boot] WiFi initialization failed:', _failure)
        report_memory('wifi-init-failed')
        print('[Boot] Application was not loaded. Power-cycle after updating files.')
        raise
    configure_gc()
    report_memory('wifi-reserved')
    return _station


def configure_runtime():
    # These paths take precedence over old source files left on the device.
    # Static files and the user's config.py keep their original root paths.
    for path in ('/runtime', '/runtime/lib'):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)
