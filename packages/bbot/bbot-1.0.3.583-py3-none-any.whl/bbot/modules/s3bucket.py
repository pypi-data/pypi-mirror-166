import re

from bbot.modules.base import BaseModule


class s3bucket(BaseModule):
    watched_events = ["DNS_NAME"]
    produced_events = ["STORAGE_BUCKET"]
    flags = ["active", "safe", "cloud-enum"]
    meta = {"description": "Check for S3 buckets related to target"}
    options = {"max_threads": 10, "permutations": False}
    options_desc = {
        "max_threads": "Maximum number of threads for HTTP requests",
        "permutations": "Whether to try permutations",
    }

    base_tags = ["aws-cloud"]
    delimiters = ("", ".", "-")
    base_domains = ["s3.amazonaws.com"]
    bucket_name_regex = r"(?!(^xn--|-s3alias$))^[a-z0-9][a-z0-9-\.]{1,61}[a-z0-9]$"

    def setup(self):
        self.buckets_tried = set()
        self.open_only = self.config.get("open_only", True)
        self.permutations = self.config.get("permutations", False)
        self.bucket_name_regex = re.compile(self.bucket_name_regex)
        return True

    def handle_event(self, event):
        buckets = set()
        base = event.data
        stem = self.helpers.domain_stem(base)
        for b in [base, stem]:
            split = b.split(".")
            for d in self.delimiters:
                bucket_name = d.join(split)
                if self.valid_bucket_name(bucket_name):
                    buckets.add(bucket_name)

        if self.permutations:
            for b in [stem, base]:
                for mutation in self.helpers.word_cloud.mutations(b):
                    for d in self.delimiters:
                        bucket_name = d.join(mutation)
                        if self.valid_bucket_name(bucket_name):
                            buckets.add(bucket_name)

        for bucket_name in buckets:
            for base_domain in self.base_domains:
                self.submit_task(self.check_bucket, bucket_name, base_domain, event)

    def valid_bucket_name(self, bucket_name):
        valid = self.bucket_name_regex.match(bucket_name)
        if valid and not self.helpers.is_ip(bucket_name):
            bucket_hash = hash(bucket_name)
            if not bucket_hash in self.buckets_tried:
                self.buckets_tried.add(bucket_hash)
                return True
        return False

    def build_url(self, bucket_name, base_domain):
        return f"https://{bucket_name}.{base_domain}"

    def gen_tags(self, bucket_name, web_response):
        tags = []
        status_code = getattr(web_response, "status_code", 404)
        content = getattr(web_response, "text", "")
        if status_code == 200 and "Contents" in content:
            tags.append("open-bucket")
        return tags

    def check_bucket(self, bucket_name, base_domain, event):
        url = self.build_url(bucket_name, base_domain)
        web_response = self.helpers.request(url)
        tags = list(self.base_tags)
        existent_bucket, event_type = self.check_response(bucket_name, web_response)
        if existent_bucket:
            tags = list(set(self.gen_tags(bucket_name, web_response) + tags))
            self.emit_event({"name": bucket_name, "url": url}, event_type, source=event, tags=tags)

    def check_response(self, bucket_name, web_response):
        status_code = getattr(web_response, "status_code", 404)
        existent_bucket = status_code != 404
        event_type = "STORAGE_BUCKET"
        return existent_bucket, event_type
