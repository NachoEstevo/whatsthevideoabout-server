from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS
import openai
import os

app = Flask(__name__)

# Set up the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/get-transcript/<video_id>", methods=["GET"])
def get_transcript(video_id):
    # Get the transcript from the YouTube Transcript API
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    # Extract the text from the transcript
    transcript_text = ""
    for line in transcript:
        transcript_text += line["text"] + " "

    return transcript_text


# Endpoint to extract the transcript from a YouTube video

# Endpoint to summarize the transcript using the OpenAI API
@app.route("/api/summarizeKeyIdeas/<video_id>", methods=["POST"])
def summarize_transcript(video_id):
    transcript = get_transcript(video_id)
    prompt = f"The following text is a transcript from a youtube video. It may lack punctuation and not be totally accurate. Summarize its key ideas:\n{transcript}",
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0)

    # get the response text
    answer = response.choices[0].text.strip()
    resp = jsonify({"summary": answer})
    resp.headers.add("Access-Control-Allow-Origin", "*")
    resp.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return resp


@app.route("/api/summarizeBulletPoint/<video_id>", methods=["POST"])
def summarize_transcript_bullet(video_id):
    transcript = get_transcript(video_id)

    prompt = f"The following text is a transcript from a youtube video. It may lack punctuation and not be totally accurate. Summarize its key ideas using bullet points:\n{transcript}"

    # define the parameters for the API request
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0)

    # get the response text
    answer = response.choices[0].text.strip()

    # Add CORS headers to the response
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")

    return jsonify({"summary": answer})


if __name__ == "__main__":
    CORS(app)
