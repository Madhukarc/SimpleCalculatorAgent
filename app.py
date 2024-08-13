import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import StdOutCallbackHandler

# Load environment variables
load_dotenv()

app = Flask(__name__)


# Set up a simple calculator tool
def calculator(expression):
    try:
        return str(eval(expression))
    except:
        return "Error: Invalid expression"


tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="useful for when you need to perform mathematical calculations",
    )
]

# Set up the LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Initialize the agent
agent = initialize_agent(
    tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)


@app.route("/query", methods=["POST"])
def query_agent():
    data = request.json
    if "question" not in data:
        return jsonify({"error": "No question provided"}), 400

    question = data["question"]
    try:
        response = agent.run(question)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
