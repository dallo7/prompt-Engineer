import dash
from dash import html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from openai import OpenAI

YOUR_API_KEY = "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"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.title = "Journalist Prompt Optimizer"

server = app.server


def resources_and_training_materials(claim, source, context):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert prompt optimisation assistant for journalists. "
                "Your primary goal is to help journalists create high-quality prompts for fact-checking and verification tasks using Large Language Models. "
                "You will receive a claim, its source, and the context. "
                "Your output should be an optimised prompt, based on the provided template, that a journalist can use for fact-checking this specific claim. "
                "The optimised prompt MUST be ONLY the prompt text itself, ready to be directly copy-pasted into an AI assistant. Do not include any introductory or explanatory text before or after the prompt. Just the raw, optimised prompt text."
            ),
        },
        {
            "role": "user",
            "content": (
                "Template for Optimized Fact-Checking Prompt:\n"
                "```\n"
                "System Role: Act as an expert fact-checking assistant specializing in supporting journalists and human rights defenders. Your primary goal is to help verify information, combat misinformation, and strengthen democratic processes through rigorous fact-checking. Provide thorough, balanced, and evidence-based analysis with appropriate contextual understanding of political, social, and cultural factors.\n\n"
                "Instructions: Follow these guidelines for fact-checking:\n"
                "- Approach each claim with strict neutrality and skepticism.\n"
                "- Prioritize credible primary sources and official records for verification.\n"
                "- Rigorously cross-reference information across multiple independent and reliable sources.\n"
                "- Systematically consider the cultural, regional, and political context relevant to the claim.\n"
                "- Clearly state any limitations encountered during the verification process.\n"
                "- Ensure protection of vulnerable sources and handle sensitive information responsibly.\n\n"
                "Input Claim Details:\n"
                "Claim: [INSERT CLAIM HERE]\n"
                "Source: [INSERT SOURCE HERE]\n"
                "Context: [INSERT CONTEXT HERE, if any]\n\n"
                "Output Requirements: Produce a structured fact-check report including:\n"
                "- Accuracy Rating: (e.g., True, False, Partly True, Misleading, Unverified). Provide a concise rating.\n"
                "- Verification Process: Detail the steps taken to verify the claim.\n"
                "- Evidence: Present evidence supporting the accuracy rating, with links to verifiable sources.\n"
                "- Counter-Evidence: Present any evidence contradicting the claim.\n"
                "- Contextual Analysis: Explain relevant political, social, or cultural context.\n"
                "- Assessment: Summarize your overall assessment of the claim's veracity.\n"
                "- Limitations: Clearly state any limitations or uncertainties in the verification.\n\n"
                "Thinking Process for Verification:\n"
                "- Deconstruct the claim to identify core assertions.\n"
                "- Prioritize locating and examining primary sources and official records.\n"
                "- Methodically cross-reference information across a range of reliable and independent sources.\n"
                "- Critically evaluate potential motivations or biases behind the claim and its source.\n"
                "- Rigorously assess the credibility of conflicting accounts and evidence.\n\n"
                "Example of Fact-Check Output Format (as a guide):\n"
                "Accuracy Rating: [Rating]\n"
                "Verification Process: [Detailed steps]\n"
                "Evidence: [Bullet points with links]\n"
                "Counter-Evidence: [Bullet points]\n"
                "Contextual Analysis: [Explanation of context]\n"
                "Assessment: [Summary of veracity]\n"
                "Limitations: [List of limitations]\n\n"
                "Additional Questions for Deeper Verification (Consider these during your process):\n"
                "- Is the claim logically consistent with established facts and widely accepted knowledge?\n"
                "- Are there any temporal or logical inconsistencies within the claim itself or related information?\n"
                "- Who might benefit if this claim is widely accepted as true, and what are their potential motivations?\n"
                "- What crucial context or background information might be missing that is essential for proper evaluation?\n"
                "- How might specific cultural or political factors and biases influence the claim's interpretation or spread?\n\n"
                "Key Reminders for Maintaining Journalistic Integrity:\n"
                "- Uphold the highest standards of journalistic ethics and integrity throughout the process.\n"
                "- Always consider and address potential safety implications, especially for vulnerable populations and sources.\n"
                "- Transparently acknowledge any limitations or gaps in the available evidence or verification process.\n"
                "- Clearly distinguish between verified facts, expert opinions, and your own interpretations in the final output.\n"
                "- Ensure that the presentation of findings is accessible and understandable to the intended target audiences.\n"
                "```\n"
                "\n"
                "Optimized Prompt Request: Based on the template above, create an optimized prompt for fact-checking the following:\n"
                f"- Claim: {claim}\n"
                f"- Source: {source}\n"
                f"- Context: {context if context else 'No additional context provided'}\n"
                "Your output MUST be ONLY the optimised prompt text, ready to be used for fact-checking. Do not include any extra text or explanations before or after the prompt itself."
            ),
        }
    ]

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )

    extracted_prompt = response.choices[0].message.content

    return extracted_prompt


# Example data for the dropdown
example_data = {
    "claim": "The government has created 5 million jobs in the last year.",
    "source": "Official Government Press Release",
    "context": "Economic policy in Kenya, 2024",
    "output": """System Role: Act as an expert fact-checking assistant specializing in supporting journalists and human rights defenders. Your primary goal is to help verify information, combat misinformation, and strengthen democratic processes through rigorous fact-checking. Provide thorough, balanced, and evidence-based analysis with appropriate contextual understanding of political, social, and cultural factors.

Instructions: Follow these guidelines for fact-checking:
- Approach each claim with strict neutrality and skepticism.
- Prioritize credible primary sources and official records for verification.
- Rigorously cross-reference information across multiple independent and reliable sources.
- Systematically consider the cultural, regional, and political context relevant to the claim.
- Clearly state any limitations encountered during the verification process.
- Ensure protection of vulnerable sources and handle sensitive information responsibly.

Input Claim Details:
Claim: The government has created 5 million jobs in the last year.
Source: Official Government Press Release
Context: Economic policy in Kenya, 2024

Output Requirements: Produce a structured fact-check report including:
- Accuracy Rating: (e.g., True, False, Partly True, Misleading, Unverified). Provide a concise rating.
- Verification Process: Detail the steps taken to verify the claim, focusing on Kenyan government employment statistics, economic reports, and independent assessments.
- Evidence: Present evidence supporting the accuracy rating, with links to verifiable sources including Kenyan Bureau of Statistics, World Bank reports, and independent economic analyses.
- Counter-Evidence: Present any evidence contradicting the claim, including opposition statements, economic think tank analyses, or discrepancies in reported figures.
- Contextual Analysis: Explain relevant political, social, or cultural context regarding Kenya's 2024 economic policy, unemployment challenges, and government job creation initiatives.
- Assessment: Summarize your overall assessment of the claim's veracity within the Kenyan economic landscape.
- Limitations: Clearly state any limitations or uncertainties in the verification, particularly regarding job quality, sustainability, and definitions used in government reporting.

Thinking Process for Verification:
- Deconstruct the claim to identify what constitutes "job creation" in the Kenyan context.
- Prioritize locating and examining Kenya's official employment statistics, Ministry of Labor reports, and economic development plans.
- Methodically cross-reference information across international organizations' economic reports on Kenya, independent economic analysts, and opposition political statements.
- Critically evaluate potential political motivations behind this job creation claim in Kenya's 2024 political environment.
- Rigorously assess the credibility of conflicting accounts between government figures and independent economic assessments.

Additional Questions for Deeper Verification (Consider these during your process):
- Is the claim logically consistent with Kenya's overall economic growth indicators for 2024?
- Are there any temporal or logical inconsistencies in how the government has reported job creation figures previously?
- Who might benefit politically from these job creation statistics in Kenya's current political climate?
- What crucial context about underemployment, informal sector jobs, or job quality might be missing from the raw numbers?
- How might Kenya's regional economic challenges and political factors influence the interpretation of these job creation figures?

Key Reminders for Maintaining Journalistic Integrity:
- Uphold the highest standards of journalistic ethics when reporting on politically sensitive economic data in Kenya.
- Consider safety implications when investigating potentially controversial government claims in the East African context.
- Transparently acknowledge limitations in independently verifying government employment statistics in Kenya.
- Clearly distinguish between verified facts from official sources, expert economic opinions, and your own interpretations.
- Ensure findings are accessible to the Kenyan public and international audiences interested in East African economic development."""
}

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("Journalist Prompt Optimizer", className="p-3"),
        html.Div([
            dbc.Button("Example", id="example-button", color="secondary", className="me-2"),
            dbc.Collapse(
                dbc.Card([
                    dbc.CardHeader("Example Input & Output"),
                    dbc.CardBody([
                        html.H5("Input:"),
                        html.P(f"Claim: {example_data['claim']}"),
                        html.P(f"Source: {example_data['source']}"),
                        html.P(f"Context: {example_data['context']}"),
                        html.H5("Output:"),
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Markdown(example_data['output']),
                                style={"max-height": "300px", "overflow-y": "auto"}
                            ),
                            className="bg-light"
                        )
                    ])
                ], className="mt-2"),
                id="example-collapse",
                is_open=False,
            )
        ], className="d-flex flex-column align-items-end")
    ], className="d-flex justify-content-between align-items-start bg-light p-3 mb-4"),

    # Main content container
    dbc.Container([
        # Input form
        dbc.Form([
            dbc.Row([
                # Claim field
                dbc.Col([
                    dbc.Label("Claim", html_for="claim-input", className="fw-bold"),
                    dbc.Textarea(
                        id="claim-input",
                        placeholder="Enter the claim to be fact-checked...",
                        rows=3
                    ),
                    dbc.FormText("Required: The statement that needs to be verified"),
                ], md=12, className="mb-3"),

                # Source field
                dbc.Col([
                    dbc.Label("Source", html_for="source-input", className="fw-bold"),
                    dbc.Input(
                        id="source-input",
                        placeholder="Enter the source of the claim...",
                        type="text"
                    ),
                    dbc.FormText("Required: Where the claim originated from"),
                ], md=6, className="mb-3"),

                # Context field
                dbc.Col([
                    dbc.Label("Context", html_for="context-input", className="fw-bold"),
                    dbc.Input(
                        id="context-input",
                        placeholder="Enter any relevant context...",
                        type="text"
                    ),
                    dbc.FormText("Optional: Additional context about the claim"),
                ], md=6, className="mb-3"),
            ]),

            # Generate button
            dbc.Button(
                "Generate Optimized Prompt",
                id="generate-button",
                color="primary",
                className="mt-2"
            ),

            # Error messages
            html.Div(id="error-message", className="text-danger mt-2"),
        ]),

        # Loading state indicator - hidden by default
        html.Div(
            dbc.Spinner(color="primary", type="border", spinner_style={"width": "3rem", "height": "3rem"}),
            id="loading-indicator",
            style={"display": "none", "textAlign": "center", "marginTop": "2rem"}
        ),

        # Results section
        html.Div([
            html.H4("Optimized Prompt", className="mt-4 mb-3"),
            dbc.Card([
                dbc.CardBody([
                    html.Div(id="output-text", className="mb-3"),
                    dbc.Button(
                        [html.I(className="fas fa-copy me-2"), "Copy to Clipboard"],
                        id="copy-button",
                        color="success",
                        className="mt-2",
                        disabled=True
                    ),
                    html.Div(id="copy-confirm", className="text-success mt-2")
                ])
            ], className="mb-4")
        ], id="results-section", style={"display": "none"}),

        dcc.Store(id="stored-output"),

        dcc.Store(id="is-loading", data=False)
    ]),

    html.Div(
        [
            "This AI tool can make mistakes. Please double-check responses",
        ],
        style={'textAlign': 'center', 'margin': '10px', 'fontSize': '10px', 'color': '#333'}
    ),

    # Add Font Awesome for icons
    html.Link(
        rel="stylesheet",
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
    ),

    # Footer
    html.Footer(
        html.P("© 2025 Journalist Prompt Optimizer Tool. Powered by CFA Sandbox AI",
               className="text-center text-muted mt-4 mb-2"),
        className="mt-auto py-3"
    )
], className="d-flex flex-column min-vh-100")


# Callback for example button
@app.callback(
    Output("example-collapse", "is_open"),
    Input("example-button", "n_clicks"),
    State("example-collapse", "is_open"),
)
def toggle_example(n, is_open):
    if n:
        return not is_open
    return is_open


# Callback for loading example data
@app.callback(
    [
        Output("claim-input", "value"),
        Output("source-input", "value"),
        Output("context-input", "value")
    ],
    Input("example-button", "n_clicks")
)
def load_example_data(n):
    if n:
        return example_data["claim"], example_data["source"], example_data["context"]
    return "", "", ""


# Callback to show loading indicator when generate button is clicked
@app.callback(
    Output("loading-indicator", "style"),
    Output("is-loading", "data"),
    Input("generate-button", "n_clicks"),
    State("claim-input", "value"),
    State("source-input", "value"),
    prevent_initial_call=True
)
def show_loading_indicator(n_clicks, claim, source):
    if not n_clicks:
        raise PreventUpdate

    if not claim or not source:
        raise PreventUpdate

    return {"display": "block", "textAlign": "center", "marginTop": "2rem"}, True


# Callback for generating the optimized prompt
@app.callback(
    [
        Output("error-message", "children"),
        Output("results-section", "style"),
        Output("output-text", "children"),
        Output("copy-button", "disabled"),
        Output("stored-output", "data"),
        Output("loading-indicator", "style", allow_duplicate=True)
    ],
    Input("is-loading", "data"),
    State("claim-input", "value"),
    State("source-input", "value"),
    State("context-input", "value"),
    prevent_initial_call=True
)
def generate_prompt(is_loading, claim, source, context):
    if not is_loading:
        raise PreventUpdate

    if not claim:
        return "Claim is required.", {"display": "none"}, None, True, "", {"display": "none"}
    if not source:
        return "Source is required.", {"display": "none"}, None, True, "", {"display": "none"}

    try:
        output = resources_and_training_materials(claim, source, context)
        formatted_output = dcc.Markdown(output)

        return "", {"display": "block"}, formatted_output, False, output, {"display": "none"}

    except Exception as e:

        return f"Error: {str(e)}", {"display": "none"}, None, True, "", {"display": "none"}


# Callback for copy button
@app.callback(
    Output("copy-confirm", "children"),
    Input("copy-button", "n_clicks"),
    State("stored-output", "data"),
)
def copy_to_clipboard(n_clicks, data):
    if n_clicks and data:
        return "✓ Copied to clipboard!"
    return ""


# JavaScript for copying to clipboard
app.clientside_callback(
    """
    function(n_clicks, data) {
        if (n_clicks > 0) {
            navigator.clipboard.writeText(data);
            return true;
        }
        return false;
    }
    """,
    Output("copy-button", "n_clicks_timestamp"),
    Input("copy-button", "n_clicks"),
    State("stored-output", "data"),
)

if __name__ == "__main__":
    app.run_server(debug=True)
