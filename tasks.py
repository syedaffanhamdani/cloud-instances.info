# To use this script you must have the following environment variables set:
#   AWS_ACCESS_KEY_ID
#   AWS_SECRET_ACCESS_KEY
# as explained in AWS documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

import os
import traceback
import mimetypes
from pathlib import Path

import boto3
from invoke import task
from invocations.console import confirm
from six.moves import SimpleHTTPServer, socketserver

from rds import scrape as rds_scrape
from cache import scrape as cache_scrape
from redshift import scrape as redshift_scrape
from opensearch import scrape as opensearch_scrape
from render import render
from render import build_sitemap
from render import about_page
from scrape import scrape

from io import BytesIO
import gzip
import shutil

BUCKET_NAME = "www.ec2instances.info"

abspath = lambda filename: os.path.join(
    os.path.abspath(os.path.dirname(__file__)), filename
)

HTTP_HOST = os.getenv("HTTP_HOST", "127.0.0.1")
HTTP_PORT = os.getenv("HTTP_PORT", "8080")


@task
def build(c):
    """Scrape AWS sources for data and build the site"""
    scrape_ec2(c)
    scrape_rds(c)
    scrape_cache(c)
    scrape_redshift(c)
    scrape_opensearch(c)
    render_html(c)


@task
def scrape_ec2(c):
    """Scrape EC2 data from AWS and save to local file"""
    ec2_file = "www/instances.json"
    try:
        scrape(ec2_file)
    except Exception as e:
        print("ERROR: Unable to scrape EC2 data")
        print(traceback.print_exc())


@task
def scrape_rds(c):
    """Scrape RDS data from AWS and save to local file"""
    rds_file = "www/rds/instances.json"
    try:
        rds_scrape(rds_file)
    except Exception as e:
        print("ERROR: Unable to scrape RDS data")
        print(traceback.print_exc())


@task
def scrape_cache(c):
    """Scrape Cache instance data from AWS and save to local file"""
    cache_file = "www/cache/instances.json"
    try:
        cache_scrape(cache_file)
    except Exception as e:
        print("ERROR: Unable to scrape Cache data")
        print(traceback.print_exc())


@task
def scrape_redshift(c):
    """Scrape Redshift instance data from AWS and save to local file"""
    redshift_file = "www/redshift/instances.json"
    try:
        redshift_scrape(redshift_file)
    except Exception as e:
        print("ERROR: Unable to scrape Redshift data")
        print(traceback.print_exc())


@task
def scrape_opensearch(c):
    """Scrape OpenSearch instance data from AWS and save to local file"""
    opensearch_file = "www/opensearch/instances.json"
    try:
        opensearch_scrape(opensearch_file)
    except Exception as e:
        print("ERROR: Unable to scrape OpenSearch data")
        print(traceback.print_exc())


@task
def serve(c):
    class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):
            # The URL does not include ".html". Add it to serve the file for dev
            if "/aws/" in self.path:
                if "?" in self.path:
                    self.path = (
                        self.path.split("?")[0] + ".html?" + self.path.split("?")[1]
                    )
                else:
                    self.path += ".html"
            print(self.path)
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    """Serve site contents locally for development"""
    os.chdir("www/")
    httpd = socketserver.TCPServer((HTTP_HOST, int(HTTP_PORT)), MyHandler)
    print(
        "Serving on http://{}:{}".format(
            httpd.socket.getsockname()[0], httpd.socket.getsockname()[1]
        )
    )
    httpd.serve_forever()


@task
def render_html(c):
    """Render HTML but do not update data from Amazon"""
    sitemap = []
    sitemap.extend(render("www/instances.json", "in/index.html.mako", "www/index.html"))
    sitemap.extend(
        render("www/rds/instances.json", "in/rds.html.mako", "www/rds/index.html")
    )
    sitemap.extend(
        render("www/cache/instances.json", "in/cache.html.mako", "www/cache/index.html")
    )
    sitemap.extend(
        render(
            "www/redshift/instances.json",
            "in/redshift.html.mako",
            "www/redshift/index.html",
        )
    )
    sitemap.extend(
        render(
            "www/opensearch/instances.json",
            "in/opensearch.html.mako",
            "www/opensearch/index.html",
        )
    )
    sitemap.append(about_page())
    build_sitemap(sitemap)


@task
def bucket_create(c):
    """Creates the S3 bucket used to host the site"""
    s3 = boto3.client("s3")

    # Create bucket with public read access
    s3.create_bucket(Bucket=BUCKET_NAME, ACL="public-read")

    # Configure website hosting
    s3.put_bucket_website(
        Bucket=BUCKET_NAME,
        WebsiteConfiguration={
            "IndexDocument": {"Suffix": "index.html"},
            "ErrorDocument": {"Key": "error.html"},
        },
    )

    print(f"Bucket {BUCKET_NAME!r} created.")


@task
def bucket_delete(c):
    """Deletes the S3 bucket used to host the site"""
    if not confirm(f"Are you sure you want to delete the bucket {BUCKET_NAME!r}?"):
        print("Aborting at user request.")
        exit(1)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)

    # Delete all objects in the bucket first
    bucket.objects.all().delete()

    # Then delete the bucket
    bucket.delete()

    print(f"Bucket {BUCKET_NAME!r} deleted.")


@task
def deploy(c, root_dir="www"):
    """Deploy current content"""
    s3 = boto3.client("s3")

    for root, dirs, files in os.walk(root_dir):
        for name in files:
            if name.startswith("."):
                continue

            local_path = os.path.join(root, name)
            remote_path = local_path[len(root_dir) + 1 :]
            print(f"{local_path} -> {BUCKET_NAME}/{remote_path}")

            extra_args = {"ACL": "public-read"}

            # Handle HTML files - compress with gzip
            if name.endswith(".html"):
                # Create in-memory compressed file
                compressed_file = BytesIO()
                with gzip.GzipFile(fileobj=compressed_file, mode="wb") as gz, open(
                    local_path, "rb"
                ) as fp:
                    shutil.copyfileobj(fp, gz)

                compressed_file.seek(0)

                # Add content-type and encoding headers
                extra_args.update(
                    {"ContentType": "text/html", "ContentEncoding": "gzip"}
                )

                # Upload the compressed file
                s3.upload_fileobj(
                    Fileobj=compressed_file,
                    Bucket=BUCKET_NAME,
                    Key=remote_path,
                    ExtraArgs=extra_args,
                )
            else:
                # For non-HTML files, try to guess the content type
                content_type = mimetypes.guess_type(local_path)[0]
                if content_type:
                    extra_args["ContentType"] = content_type

                # Upload the file directly
                s3.upload_file(
                    Filename=local_path,
                    Bucket=BUCKET_NAME,
                    Key=remote_path,
                    ExtraArgs=extra_args,
                )


@task(default=True)
def update(c):
    """Build and deploy the site"""
    build(c)
    deploy(c)
