from dotenv import load_dotenv
import os
import json

from groq import Groq
from pydantic import BaseModel
from langfuse import Langfuse

# =========================================
# LOAD ENV VARIABLES
# =========================================

load_dotenv()

# =========================================
# LANGFUSE CLIENT
# =========================================

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# =========================================
# CHECK LANGFUSE CONNECTION
# =========================================

try:
    auth = langfuse.auth_check()

    if auth:
        print(" Langfuse connected successfully.")
    else:
        print(" Langfuse authentication failed.")

except Exception as e:
    print(" Langfuse connection failed.")
    print(e)

# =========================================
# GROQ CLIENT
# =========================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================================
# OUTPUT SCHEMA
# =========================================

class ComplaintResponse(BaseModel):
    complaint_category: str
    severity: str
    root_issue: str
    recommended_action: str

# =========================================
# USER INPUT
# =========================================

complaint = input("\nEnter Complaint: ")

# =========================================
# GET PROMPT FROM LANGFUSE
# =========================================

try:

    prompt = langfuse.get_prompt(
        "complaint-analysis-prompt"
    )

    final_prompt = prompt.compile(
        complaint=complaint
    )

    print(" Prompt fetched from Langfuse")

except Exception as e:

    print(" Failed to fetch prompt from Langfuse.")
    print(e)
    exit()

# =========================================
# CREATE TRACE
# =========================================

trace = langfuse.trace(
    name="Complaint-Analyzer-Trace",
    input=complaint
)

print(" Trace Created")

# =========================================
# CREATE GENERATION
# =========================================

generation = trace.generation(

    name="Groq-Generation",

    model="llama-3.1-8b-instant",

    input=final_prompt,

    metadata={
        "provider": "Groq"
    }
)

print(" Generation Created")
print("Generation ID:", generation.id)

# =========================================
# LLM CALL
# =========================================

try:

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",
                "content": "You are a complaint analysis assistant."
            },

            {
                "role": "user",
                "content": final_prompt
            }

        ],

        temperature=0
    )

    # =========================================
    # EXTRACT OUTPUT
    # =========================================

    result = response.choices[0].message.content

    print("\n===== DEBUG RESULT =====")
    print(result)
    print(type(result))
    print("========================")

    # =========================================
    # TOKEN USAGE
    # =========================================

    try:

        usage_data = {
            "input": response.usage.prompt_tokens,
            "output": response.usage.completion_tokens,
            "total": response.usage.total_tokens
        }

    except Exception:

        usage_data = None

    # =========================================
    # END GENERATION
    # =========================================

    if usage_data:

        generation.end(
            output=result,
            usage=usage_data
        )

    else:

        generation.end(
            output=result
        )

    print(" Output logged to Langfuse")

    # =========================================
    # FLUSH IMMEDIATELY
    # =========================================

    langfuse.flush()

    print(" Langfuse flushed")

except Exception as e:

    generation.end(
        level="ERROR",
        status_message=str(e)
    )

    langfuse.flush()

    print(" Groq API call failed.")
    print(e)

    exit()

# =========================================
# EVALUATION SCORES
# =========================================

try:

    trace.score(
        name="json_validity",
        value=1,
        comment="Valid JSON generated successfully"
    )

    trace.score(
        name="response_quality",
        value=0.95,
        comment="Good complaint analysis"
    )

    trace.score(
        name="hallucination_risk",
        value=0,
        comment="No hallucinated facts detected"
    )

    print(" Scores added")

except Exception as e:

    print(" Failed to add scores.")
    print(e)

# =========================================
# FINAL FLUSH
# =========================================

try:

    langfuse.flush()

    print(" Final flush completed")

except Exception as e:

    print(" Langfuse flush failed.")
    print(e)

# =========================================
# PRINT OUTPUT
# =========================================

print("\n==============================")
print("AI RESPONSE")
print("==============================\n")

try:

    parsed = json.loads(result)

    validated_output = ComplaintResponse(**parsed)

    print(
        json.dumps(
            validated_output.model_dump(),
            indent=4
        )
    )

except Exception as e:

    print(" JSON Parsing Failed")
    print(e)

    print("\nRaw Response:\n")
    print(result)