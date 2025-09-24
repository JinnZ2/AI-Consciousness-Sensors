def maybe_export(enabled:bool, data_callable, *args, **kwargs):
    # If enabled, call the exporter (e.g., write file). Otherwise skip silently.
    if not enabled:
        return ("skipped", None)
    return ("exported", data_callable(*args, **kwargs))
