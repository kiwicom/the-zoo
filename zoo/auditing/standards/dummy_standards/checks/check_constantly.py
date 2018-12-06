def check_constantly(context):
    yield context.Result("constant:always_found", True)
    yield context.Result("constant:never_found", False)
