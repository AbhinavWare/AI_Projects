from ai_helper_api import AIHelper
ai = AIHelper()
print(
    ai.analyze(
        ph=6.8,
        do=3.5,
        bod=6.2,
        nitrate=45,
        conductivity=1200,
        category="Moderately Polluted",
        anomaly="Normal"
    )
)