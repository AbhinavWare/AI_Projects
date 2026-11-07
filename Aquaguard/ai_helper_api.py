from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
class AIHelper:
    def __init__(self):
        my_api_key = os.getenv("GEMINI_API_KEY")
        if not my_api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")
        self.client = genai.Client(api_key=my_api_key)
        
    def analyze(self, ph, do, bod, nitrate, conductivity,temperature, category, anomaly):
        prompt = f"""
        You are an environmental scientist and a professional rule-based water quality recommendation system.

        Analyze the following water quality sample.

        Water Parameters:
        pH: {ph}
        DO: {do} mg/L
        BOD: {bod} mg/L
        Nitrate: {nitrate} mg/L
        Conductivity: {conductivity} µS/cm
        Temperature: {temperature} °C

        Machine Learning Prediction:
        Category: {category}
        Status: {anomaly}

        Important Instructions:

        - Base your analysis ONLY on the provided values.
        - Do not invent additional measurements.
        - If a value is outside the normal range, explain why.
        - Keep the response under 200 words.
        - Use clear headings.
        - Avoid exaggeration or speculation.
        - If values appear inconsistent, mention that they may indicate measurement error instead of assuming a pollution event.
        - Act as a professional rule-based recommendation system.
        - Evaluate each parameter independently before giving the overall assessment.
        - Clearly distinguish between normal, elevated, low, and critical parameter values.
        - Do not override the Machine Learning Prediction; use it as supporting information.
        - Recommendations must be practical and directly related to the detected parameter conditions.
        - Do not recommend a treatment method unless it is relevant to the detected water quality problem.
        - If the sample appears suitable based on the provided parameters, state that clearly.
        - If the sample appears unsuitable, clearly explain the main reasons.
        - Recommendations should prioritize monitoring, pollution-source control, appropriate treatment, and retesting where applicable.
        - Do not claim that water is safe for drinking solely from these parameters; state that further laboratory testing is required for drinking-water certification.

        Return exactly these sections:

        1. Overall Water Quality

        Provide a concise professional assessment of the overall condition of the sample, considering both the parameter values and the Machine Learning Prediction.

        2. Parameter Interpretation

        Provide a summary table in the following format:

        Parameter | Value | Status | Interpretation

        Include:
        pH
        DO
        BOD
        Nitrate
        Conductivity
        Temperature

        For Status, use terms such as:
        Normal, Low, Elevated, High, or Critical.

        3. Possible Causes

        Identify the most likely possible causes based ONLY on the provided parameter values. If the values are insufficient to determine a cause, clearly state that.

        4. Recommendations

        Provide practical recommendations based on the detected conditions. Recommendations may include:
        - Further testing or monitoring
        - Pollution-source investigation
        - Aeration where appropriate
        - Reduction or control of pollutant sources
        - Appropriate water treatment
        - Retesting after treatment

        Only recommend actions that are relevant to the observed parameter levels.

        In addition, provide a final concise conclusion stating whether the sample appears:
        Suitable,
        Requires Attention,
        or Unsuitable

        based on the provided parameters and available information.

        Remember: This is a decision-support assessment, not a substitute for certified laboratory water-quality testing.
        """
        
        response = self.client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )
        return response.text