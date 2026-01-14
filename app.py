import math
from flask import Flask, jsonify

app = Flask(__name__)

def numerical_integral(lower, upper, N):
    """
    Computes the numerical integral of abs(sin(x)) in the interval [lower, upper]
    using the rectangle method with N subintervals.
    """
    # Width of each subinterval
    dx = (upper - lower) / N
    
    # Initialize the sum
    total_area = 0.0
    
    # Iterate over each subinterval
    for i in range(N):
        # Midpoint of the subinterval (midpoint method)
        x_mid = lower + (i + 0.5) * dx
        # Height of the rectangle: abs(sin(x))
        height = abs(math.sin(x_mid))
        # Area of the rectangle
        area = height * dx
        # Add to total
        total_area += area
    
    return total_area

@app.route('/numericalintegralservice/<path:lower>/<path:upper>', methods=['GET'])
def compute_integral(lower, upper):
    """
    Microservice endpoint that computes numerical integration of abs(sin(x))
    in the interval [lower, upper] for multiple values of N.
    """
    # Convert path parameters to float
    try:
        lower = float(lower)
        upper = float(upper)
    except ValueError:
        return jsonify({'error': 'Invalid parameters. lower and upper must be numbers.'}), 400
    # Values of N to test (7 values)
    N_values = [10, 100, 1000, 10000, 100000, 1000000]
    
    # Calculate integral for each value of N
    results = []
    for N in N_values:
        result = numerical_integral(lower, upper, N)
        diff = abs(result - 2.0)
        results.append({
            'N': N,
            'result': result,
            'difference_from_2': diff
        })
    
    # Return JSON response
    return jsonify({
        'lower': lower,
        'upper': upper,
        'results': results
    })

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    """
    return jsonify({'status': 'healthy'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)
