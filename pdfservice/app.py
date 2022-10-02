"""Service that provides a REST API endpoint for generating a pdf"""
import os
from datetime import datetime

import boto3
import pdfkit
from jinja2 import Environment, FileSystemLoader
from chalice import Chalice, BadRequestError
from botocore.exceptions import ClientError

BUCKET = "pdfdemoatl2022"
TEMPLATE_NAME = "base.html"

s3 = boto3.client("s3")

app = Chalice(app_name="pdfservice")


def render_html_template(context):
    """Renders a html file from the template and given context.

    Args:
        context (dict): key-value pairs to be interpolated into template

    Returns:
        The local filename of the generated html
        If the generation failed, then `None` will be returned.
    """
    env = Environment(
        loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "templates"),
            encoding="utf8"
        )
    )
    template = env.get_template(TEMPLATE_NAME)
    html_string = template.render(**context)

    timestamp = str(datetime.now()).replace(".", "").replace(" ", "_")
    local_filename = f"/tmp/{timestamp}.html"

    try:
        os.unlink(local_filename)
    except FileNotFoundError:
        pass

    with open(local_filename, "w") as file_obj:
        file_obj.write(html_string)

    return local_filename


def upload_file_to_s3(filename):
    """Uploads the generated PDF to s3.

    Args:
        filename (str): Location of the file to upload to s3.

    Returns:
        The presigned url of the file in s3 if the upload was successful.
        If the upload failed, then `None` will be returned.
    """
    file_url = None
    try:
        file_key = filename.replace("/tmp/", "")
        s3.upload_file(Filename=filename, Bucket=BUCKET, Key=file_key)
        file_url = s3.generate_presigned_url(
            "get_object", Params={"Bucket": BUCKET, "Key": file_key}
        )

    except ClientError as exception_message:
        print(exception_message)
        file_url = None

    return file_url


def format_currency(value):
    """Takes a string and returns a comma-separated dollar string"""
    return "${:,.2f}".format(float(value))


@app.route("/generate", methods=["POST"], cors=True)
def generate_pdf():
    """API endpoint (via Chalice) that takes a POST payload,
    renders an html template, converts the html to a pdf,
    uploads the pdf to s3, and returns a public url for the
    generate pdf.
    """
    request = app.current_request
    body = request.json_body

    context = {
        "company_name": body.get("company_name", "(None)"),
        "num_employees": body.get("num_employees", "n/a"),
        "revenue": format_currency(body.get("revenue", "0")),
        "lucky_number": body.get(
            "lucky_number",
            "A real man makes his own luck"
        ),
        "zipcode": body.get("zipcode", "-----"),
    }

    in_file = render_html_template(context)
    out_file = in_file.replace(".html", ".pdf")
    config = pdfkit.configuration(wkhtmltopdf="/opt/bin/wkhtmltopdf")
    pdfkit.from_file(in_file, out_file, configuration=config)
    file_url = upload_file_to_s3(out_file)

    if file_url is None:
        error_message = (
            "Failed to generate PDF from the given HTML file."
            " Please check to make sure the file is valid HTML."
        )
        raise BadRequestError(error_message)

    return {"file_url": file_url}
