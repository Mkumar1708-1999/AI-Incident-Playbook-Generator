# ai_model.py
from llama_cpp import Llama

# Load the GGUF model once at startup
llm = Llama(
    model_path="./unsloth.F16.gguf",  # Adjust if needed
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=20,
    verbose=True
)

def get_ai_incident_results(incident_text):
    # Truncate long inputs for stability
    if len(incident_text) > 1500:
        incident_text = incident_text[:1500]

    prompt = f"Analyze this AI incident and provide clusters and risk level:\n\n{incident_text}\n\nResponse:"

    output = llm(
        prompt=prompt,
        max_tokens=256,
        temperature=0.7,
        stop=["</s>"]
    )

    model_output = output["choices"][0]["text"].strip()

    if "Response:" in model_output:
        clusters, response = model_output.split("Response:", 1)
    else:
        clusters = "Cluster info"
        response = model_output

    return clusters.strip(), response.strip()
