def Response(status: str, data_field: str, data: any):
    return {
        "status": status,
        data_field: data
    }