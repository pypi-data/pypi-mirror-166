from bbot.modules.s3bucket import s3bucket


class azureblob(s3bucket):
    watched_events = ["DNS_NAME"]
    produced_events = ["STORAGE_BUCKET"]
    flags = ["active", "safe", "cloud-enum"]
    meta = {"description": "Check for Azure storage blobs related to target"}
    options = {"max_threads": 10, "permutations": False}
    options_desc = {
        "max_threads": "Maximum number of threads for HTTP requests",
        "permutations": "Whether to try permutations",
    }

    base_tags = ["azure-cloud"]
    delimiters = ("", "-")
    base_domains = ["blob.core.windows.net"]
    bucket_name_regex = r"^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$"

    def gen_tags(self, *args, **kwargs):
        return []

    def check_response(self, bucket_name, web_response):
        status_code = getattr(web_response, "status_code", 0)
        existent_bucket = status_code != 0
        event_type = "STORAGE_BUCKET"
        return existent_bucket, event_type
