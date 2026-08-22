from app.features.feature_schema import ExtractedFeatures

class ComplexityExplainer:
    def explain(self, features: ExtractedFeatures, prediction: str) -> str:
        """
        Generates a human-readable explanation based on extracted structural features
        and the predicted time complexity.
        """
        reasons = []
        
        # Check loops
        if features.max_loop_depth == 0 and not features.recursive:
            reasons.append("The code contains no loops or recursive calls, executing in a single pass.")
            return " ".join(reasons)
            
        if features.max_loop_depth == 1:
            if features.logarithmic_loop_count > 0:
                reasons.append("The program contains a loop where the index is multiplied/divided, producing logarithmic growth.")
            else:
                reasons.append(f"The program contains {features.loop_count} non-nested linear loop(s) that iterate through the input.")
        elif features.max_loop_depth > 1:
            reasons.append(f"The program contains nested loops with a maximum depth of {features.max_loop_depth}.")
            if features.logarithmic_loop_count > 0:
                reasons.append("At least one loop updates logarithmically.")
            else:
                reasons.append("The nested loops appear to iterate linearly, compounding the execution time.")

        # Check recursion
        if features.recursive:
            if features.recursive_call_count > 1:
                reasons.append(f"The function recursively invokes itself along {features.recursive_call_count} branches, which typically results in exponential growth.")
            else:
                reasons.append("The function is recursive, traversing the input space.")
                
        # Tailor explanation based on prediction class (as a fallback or synthesis)
        if prediction == "O(1)":
            return "The program executes in constant time as there are no loops or structural patterns dependent on input size."
        elif prediction == "O(log n)":
            if not reasons: reasons.append("The loop variable is multiplied/divided by a constant factor on each iteration, producing logarithmic growth.")
        elif prediction == "O(n)":
            if not reasons: reasons.append("The program contains one loop that increases its index linearly.")
        elif prediction == "O(n log n)":
            reasons.append("The combination of linear and logarithmic operations suggests a linearithmic complexity.")
        elif prediction == "O(n²)":
            if "nested loops" not in reasons[0]:
                reasons.append("Two nested linear loops execute dependently or independently, resulting in O(n²).")
        elif prediction == "O(n³)":
            if "nested loops" not in reasons[0]:
                reasons.append("Three levels of nested loops execute, resulting in O(n³).")
        elif prediction == "O(2^n)":
            if not features.recursive:
                reasons.append("The structural complexity mimics exponential growth through deep branching or complex iterations.")
                
        return " ".join(reasons)
