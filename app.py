from flask import Flask, jsonify, render_template
import pymongo,os

app = Flask(__name__)

# MongoDB connection
client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client["twitter_trends"]
collection = db["trending_topics"]

@app.route("/")
def home():
    return '''
        <h1>Twitter Trending Topics</h1>
        <button onclick="window.location='/run-script'">Click here to run the script</button>
    '''

@app.route("/run-script")
def run_script():
    # Fetch the most recent record from MongoDB based on the end_time field
    record = collection.find().sort({"end_time":-1}).limit(1)
    
    if record:
        record = list(record)[0]
        trending_list = record['trending_topics']
        
        trending_html = ""
        for topic in trending_list:
            trending_html += f"""
                <li>
                    <strong>Category:</strong> {topic['category']}<br>
                    <strong>Name:</strong> {topic['name']}<br>
                    <strong>Posts:</strong> {topic['posts']}<br>
                </li>
            """
        
        return f"""
        <h1 style='padding:10px'>Twitter Trending Topics</h1>
        <p>These are the most happening topics as of {record['end_time']}</p>
        <ul>
            {trending_html}
        </ul>
        <p>The IP address used for this query was {record['ip_address']}.</p>
        <p>Here’s a JSON extract of this record from the MongoDB:</p>
        <pre>{record}</pre>
        <a href='/'>Run the query again</a>
        """
    else:
        return "No data found. Run the Selenium script first."

if __name__ == "__main__":
    app.run(debug=True)
