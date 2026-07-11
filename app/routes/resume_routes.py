from flask import Blueprint, jsonify, request

from services.resume.validator import Validator
from services.resume.parser import Parser
from services.resume.cleaner import TextCleaner
from schemas.resume import ResumeUploadResponse


resume_bp = Blueprint(
    "resume",
    __name__,
    url_prefix="/resume",
)


@resume_bp.post("/upload")
def upload_resume():
    """
    Upload, validate, parse and clean a resume.
    """

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files["file"]

    validator = Validator(file)
    valid, message = validator.validate()

    if not valid:
        return jsonify({"error": message}), 400

    parser = Parser(file)

    raw_text, page_count = parser.extract_text()

    cleaned_text = TextCleaner.clean(raw_text)

    response = ResumeUploadResponse(
        filename=file.filename,
        pages=page_count,
        character_count=len(cleaned_text),
        extracted_text=cleaned_text,
    )

    return jsonify(response.model_dump()), 200