---
author: Christian Cabrera Jojoa
course_code: 25-udenar-ml-intro
department: Department of Computer Science and Technology
description: This lecture presents the Artificial Intelligence and Machine Learning
  concepts. Their definition, history, implications, and applications.
email: chc79@cam.ac.uk
end_time: TBD
hours: 4
institution: University of Cambridge
layout: lecture
lecture_code: ml-introduction
lecture_date: 10/05/2025
permalink: /teaching/25-udenar-ml-intro/ml-introduction/
position: Senior Research Associate and Affiliated Lecturer
session: 1
start_time: TBD
title: Artificial Intelligence and Machine Learning
visible: true
---

<link rel="stylesheet" href="/assets/css/slides.css">
<div class="lecture-resources">  
  <p>
    <a href="/assets/slides/25-udenar-ml-intro/ml-introduction.pdf" target="_blank">[PDF Slides]</a>
    <a href="/assets/slides/25-udenar-ml-intro/ml-introduction.html" target="_blank">[HTML Slides]</a>    
    <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/25-udenar-ml-intro/ml-introduction.ipynb" target="_blank">[Colab Notebook]</a>
  </p>
</div>
  
<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
<script>
    async function main() {
        let pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'});
        await pyodide.loadPackage("numpy");
        await pyodide.loadPackage("matplotlib");
    }
    main();
</script>

# Expert Systems (1970-1990)

## The Rise of Knowledge-Based Systems

Expert systems represented the first commercially successful AI applications in the 1970s and 1980s. These knowledge-based systems captured human expertise in narrow domains to solve specific problems that typically required human specialists.

### Key Components of Expert Systems

1. **Knowledge Base**: Domain-specific knowledge represented as facts and rules
2. **Inference Engine**: Mechanism for applying rules to facts to derive conclusions
3. **User Interface**: Mechanism for users to interact with the system and receive explanations

### Notable Expert Systems

- **MYCIN (1972)**: Diagnosed bacterial infections and recommended antibiotics
- **DENDRAL (1965-1970)**: Identified unknown organic compounds from mass spectrometry data
- **PROSPECTOR (1978)**: Identified potential mineral deposits, successfully predicting a molybdenum deposit
- **XCON/R1 (1980)**: Configured VAX computer systems for Digital Equipment Corporation, saving estimated $40 million annually
- **CADUCEUS/INTERNIST-I (1982)**: Diagnosed complex internal medicine cases covering over 500 diseases

### Reasoning Approaches

Expert systems typically used one of two reasoning approaches:

```python
# Example of forward chaining (data-driven reasoning)
def forward_chaining(facts, rules):
    new_facts = set(facts)
    while True:
        # Find all rules that can fire based on current facts
        fired = False
        for rule in rules:
            if rule.condition.issubset(new_facts) and rule.conclusion not in new_facts:
                new_facts.add(rule.conclusion)
                print(f"Applied rule: {rule}")
                fired = True
        
        # If no new facts were derived, we're done
        if not fired:
            break
    
    return new_facts

# Example of backward chaining (goal-driven reasoning)
def backward_chaining(goal, rules, facts):
    if goal in facts:
        return True
    
    # Find rules that could prove this goal
    relevant_rules = [rule for rule in rules if rule.conclusion == goal]
    
    for rule in relevant_rules:
        # Check if all conditions can be satisfied
        all_conditions_met = True
        for condition in rule.conditions:
            if not backward_chaining(condition, rules, facts):
                all_conditions_met = False
                break
        
        if all_conditions_met:
            return True
    
    return False
```

### Legacy and Impact

Expert systems represented the first wave of commercially successful AI applications. They demonstrated that AI could provide practical value in specific domains, even with limited computing resources. However, they also faced significant limitations:

1. **Knowledge Acquisition Bottleneck**: Extracting knowledge from human experts was difficult and time-consuming
2. **Brittleness**: Systems could not reason beyond their pre-programmed knowledge
3. **Scaling Limitations**: Adding more rules often led to rule interaction problems and combinatorial explosion

Despite these limitations, expert systems established knowledge engineering as a discipline and laid the groundwork for future rule-based and knowledge-based applications. Many modern business rule management systems and decision support tools trace their lineage to expert systems.
