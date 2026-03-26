import json


# Based on MSc dissertation findings (Keele University, 2024)
# Random Forest model achieved 96% accuracy distinguishing normal vs disease
# cardiomyocytes using Musclemotion contraction metrics

def classify_contraction(amplitude, speed, duration):
    """
    Rule-based classifier derived from MSc dissertation findings.
    Features: amplitude, speed of contraction, contraction duration
    Normal cells show regular amplitude and consistent speed.
    Disease cells show irregular amplitude and elevated speed.
    """
    score = 0

    # Amplitude analysis
    # Disease cells show reduced or irregular contraction amplitude
    if amplitude < 0.3:
        score += 3  # strongly disease-like
    elif amplitude < 0.5:
        score += 2
    elif amplitude < 0.7:
        score += 1

    # Speed of contraction analysis
    # Disease cells show elevated or irregular contraction speed
    if speed > 2.0:
        score += 3  # strongly disease-like
    elif speed > 1.5:
        score += 2
    elif speed > 1.0:
        score += 1

    # Contraction duration analysis
    # Disease cells show prolonged or shortened contraction cycles
    if duration < 0.2 or duration > 0.8:
        score += 2
    elif duration < 0.3 or duration > 0.6:
        score += 1

    # Classification based on score
    if score >= 5:
        return "disease", "high", score
    elif score >= 3:
        return "disease", "moderate", score
    elif score >= 1:
        return "normal", "moderate", score
    else:
        return "normal", "high", score


def lambda_handler(event, context):
    """
    AWS Lambda handler for cardiac contraction analysis API.
    Accepts POST requests with contraction metrics.
    """
    try:
        # Parse input
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        elif isinstance(event.get('body'), dict):
            body = event['body']
        else:
            body = event

        # Extract features
        amplitude = float(body.get('amplitude', 0))
        speed = float(body.get('speed', 0))
        duration = float(body.get('contraction_duration', 0))

        # Validate inputs
        if not (0 <= amplitude <= 1):
            raise ValueError("Amplitude must be between 0 and 1")
        if not (0 <= speed <= 5):
            raise ValueError("Speed must be between 0 and 5")
        if not (0 <= duration <= 1):
            raise ValueError("Duration must be between 0 and 1")

        # Run classifier
        prediction, confidence, score = classify_contraction(
            amplitude, speed, duration
        )

        # Build response
        response_body = {
            "prediction": prediction,
            "confidence": confidence,
            "score": score,
            "input": {
                "amplitude": amplitude,
                "speed": speed,
                "contraction_duration": duration
            },
            "model_info": {
                "basis": "MSc dissertation - Keele University 2024",
                "researcher": "Nivedita Saha",
                "best_accuracy": "96% (Random Forest, 3D normal vs disease cells)",
                "features_used": ["amplitude", "speed_of_contraction", "contraction_duration"]
            },
            "interpretation": (
                "Disease-like contraction pattern detected. "
                "Irregular amplitude and/or elevated speed observed."
                if prediction == "disease"
                else
                "Normal contraction pattern detected. "
                "Amplitude and speed within healthy ranges."
            )
        }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response_body)
        }

    except ValueError as e:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }