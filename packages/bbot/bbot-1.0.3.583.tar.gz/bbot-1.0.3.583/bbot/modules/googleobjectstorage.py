from bbot.modules.s3bucket import s3bucket


class googleobjectstorage(s3bucket):
    """
    Adapted from https://github.com/RhinoSecurityLabs/GCPBucketBrute/blob/master/gcpbucketbrute.py
    """

    watched_events = ["DNS_NAME"]
    produced_events = ["STORAGE_BUCKET"]
    flags = ["active", "safe", "cloud-enum"]
    meta = {"description": "Check for Google object storage related to target"}
    options = {"max_threads": 10, "permutations": False}
    options_desc = {
        "max_threads": "Maximum number of threads for HTTP requests",
        "permutations": "Whether to try permutations",
    }

    base_tags = ["google-cloud"]
    delimiters = ("", "-", ".", "_")
    base_domains = ["storage.googleapis.com"]
    bucket_name_regex = r"^[a-z0-9][a-z0-9-_\.]{1,61}[a-z0-9]$"
    bad_permissions = [
        "storage.buckets.setIamPolicy",
        "storage.objects.list",
        "storage.objects.get",
        "storage.objects.create",
    ]

    def build_url(self, bucket_name, base_domain):
        return f"https://www.googleapis.com/storage/v1/b/{bucket_name}"

    def gen_tags(self, bucket_name, web_response):
        tags = []
        try:
            permissions = self.helpers.request(
                f"https://www.googleapis.com/storage/v1/b/{bucket_name}/iam/testPermissions?permissions=storage.buckets.delete&permissions=storage.buckets.get&permissions=storage.buckets.getIamPolicy&permissions=storage.buckets.setIamPolicy&permissions=storage.buckets.update&permissions=storage.objects.create&permissions=storage.objects.delete&permissions=storage.objects.get&permissions=storage.objects.list&permissions=storage.objects.update"
            ).json()
            if isinstance(permissions, dict):
                permissions = permissions.get("permissions", {})
                if any(p in permissions for p in self.bad_permissions):
                    tags.append("open-bucket")
        except Exception as e:
            self.warning(f'Failed to enumerate permissions for bucket "{bucket_name}": {e}')
        return tags

    def check_response(self, bucket_name, web_response):
        status_code = getattr(web_response, "status_code", 0)
        existent_bucket = status_code not in (0, 400, 404)
        event_type = "STORAGE_BUCKET"
        return existent_bucket, event_type
