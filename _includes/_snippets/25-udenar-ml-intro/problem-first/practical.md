<!-- NOTEBOOK: -->

# Practical Introduction

#### Submission Guidelines
- Submit your solution as a Jupyter notebook with the following name format: cease_ml_intro_session_1_<email_username>.ipynb
- Include clear comments explaining your code
- Provide a written analysis of your results
- Include test cases and their outputs
- Due date: [29/05/2025]

#### Interactive ML Project Canvas

The following blocks of code create an interactive Canvas we can use in our practical session.

Run the code and then fill the form to populate the ML Project Canvas. Once you have filled out all the fields, click the "Generate Canvas" button to create a new SVG file with your content.

We start by importing the relevant Python libraries.

```python
import ipywidgets as widgets
from IPython.display import display, HTML, SVG
import json
import os
import requests
from pathlib import Path
import re
```

We now define a function to create the interactive widgets.

```python
def create_form_widgets():
    widgets_dict = {}
    
    # Problem Definition
    widgets_dict['business_objectives'] = widgets.Textarea(
        placeholder='Enter business objectives...',
        rows=3,
    )
    widgets_dict['success_criteria'] = widgets.Textarea(
        placeholder='Enter success criteria...',
        rows=3
    )
    widgets_dict['stakeholders'] = widgets.Textarea(
        placeholder='Enter stakeholders...',
        rows=3
    )
    widgets_dict['user_requirements'] = widgets.Textarea(
        placeholder='Enter user requirements...',
        rows=3
    )
    widgets_dict['project_constraints'] = widgets.Textarea(
        placeholder='Enter project constraints...',
        rows=3
    )
    
    # Data
    widgets_dict['available_data'] = widgets.Textarea(
        placeholder='Enter available data...',
        rows=2
    )
    widgets_dict['data_quality'] = widgets.Textarea(
        placeholder='Enter data quality considerations...',
        rows=2
    )
    widgets_dict['data_requirements'] = widgets.Textarea(
        placeholder='Enter data requirements...',
        rows=2
    )
    
    # Model
    widgets_dict['model_selection'] = widgets.Textarea(
        placeholder='Enter model selection criteria...',
        rows=2
    )
    widgets_dict['performance_metrics'] = widgets.Textarea(
        placeholder='Enter performance metrics...',
        rows=2
    )
    widgets_dict['model_constraints'] = widgets.Textarea(
        placeholder='Enter model constraints...',
        rows=2
    )
    
    # Infrastructure
    widgets_dict['computing_resources'] = widgets.Textarea(
        placeholder='Enter computing resources...',
        rows=2
    )
    widgets_dict['deployment_environment'] = widgets.Textarea(
        placeholder='Enter deployment environment...',
        rows=2
    )
    widgets_dict['scalability_needs'] = widgets.Textarea(
        placeholder='Enter scalability needs...',
        rows=2
    )
    
    # Monitoring
    widgets_dict['performance_monitoring'] = widgets.Textarea(
        placeholder='Enter performance monitoring plan...',
        rows=2
    )
    widgets_dict['model_updates'] = widgets.Textarea(
        placeholder='Enter model update strategy...',
        rows=2
    )
    widgets_dict['maintenance_plan'] = widgets.Textarea(
        placeholder='Enter maintenance plan...',
        rows=2
    )
    
    # Ethics & Compliance
    widgets_dict['bias_fairness'] = widgets.Textarea(
        placeholder='Enter bias and fairness considerations...',
        rows=2
    )
    widgets_dict['privacy_security'] = widgets.Textarea(
        placeholder='Enter privacy and security measures...',
        rows=2
    )
    widgets_dict['regulatory_requirements'] = widgets.Textarea(
        placeholder='Enter regulatory requirements...',
        rows=2
    )
    widgets_dict['social_impact'] = widgets.Textarea(
        placeholder='Enter social impact considerations...',
        rows=2
    )
    widgets_dict['environmental_impact'] = widgets.Textarea(
        placeholder='Enter environmental impact considerations...',
        rows=2
    )
    
    return widgets_dict
```

We define a function to generate the SVG file with the widget contents.

```python
def generate_svg(widgets_dict):
    # SVG template with placeholders for content
    svg_template = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="1200" height="800" viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
    <!-- Background -->
    <rect width="1200" height="750" fill="#ffffff" stroke="#224466" stroke-width="2"/>
    
    <!-- Title -->
    <text x="600" y="50" font-family="Arial, sans-serif" font-size="40" text-anchor="middle" fill="#224466" font-weight="bold">ML Project Canvas</text>
    
    <!-- Main Sections -->
    <!-- Problem Definition (Larger) -->
    <g transform="translate(50, 100)">
        <rect width="400" height="625" fill="#f0f7ff" stroke="#224466" stroke-width="2"/>
        <text x="200" y="40" font-family="Arial, sans-serif" font-size="28" text-anchor="middle" fill="#224466" font-weight="bold">Problem Definition</text>
        <text x="30" y="80" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Business Objectives:</text>
        {business_objectives}
        <text x="30" y="140" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Success Criteria:</text>
        {success_criteria}
        <text x="30" y="200" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Stakeholders:</text>
        {stakeholders}
        <text x="30" y="260" font-family="Arial, sans-serif" font-size="20" fill="#224466">• User Requirements:</text>
        {user_requirements}
        <text x="30" y="320" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Project Constraints:</text>
        {project_constraints}
    </g>
    
    <!-- Data -->
    <g transform="translate(500, 100)">
        <rect width="300" height="180" fill="#f0f7ff" stroke="#224466" stroke-width="2"/>
        <text x="150" y="40" font-family="Arial, sans-serif" font-size="28" text-anchor="middle" fill="#224466" font-weight="bold">Data</text>
        <text x="30" y="80" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Available Data:</text>
        {available_data}
        <text x="30" y="120" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Data Quality:</text>
        {data_quality}
        <text x="30" y="160" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Data Requirements:</text>
        {data_requirements}
    </g>
    
    <!-- Model -->
    <g transform="translate(850, 100)">
        <rect width="300" height="180" fill="#f0f7ff" stroke="#224466" stroke-width="2"/>
        <text x="150" y="40" font-family="Arial, sans-serif" font-size="28" text-anchor="middle" fill="#224466" font-weight="bold">Model</text>
        <text x="30" y="80" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Model Selection:</text>
        {model_selection}
        <text x="30" y="120" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Performance Metrics:</text>
        {performance_metrics}
        <text x="30" y="160" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Model Constraints:</text>
        {model_constraints}
    </g>
    
    <!-- Infrastructure -->
    <g transform="translate(500, 325)">
        <rect width="300" height="180" fill="#f0f7ff" stroke="#224466" stroke-width="2"/>
        <text x="150" y="40" font-family="Arial, sans-serif" font-size="28" text-anchor="middle" fill="#224466" font-weight="bold">Infrastructure</text>
        <text x="30" y="80" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Computing Resources:</text>
        {computing_resources}
        <text x="30" y="120" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Deployment Environment:</text>
        {deployment_environment}
        <text x="30" y="160" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Scalability Needs:</text>
        {scalability_needs}
    </g>
    
    <!-- Monitoring -->
    <g transform="translate(850, 325)">
        <rect width="300" height="180" fill="#f0f7ff" stroke="#224466" stroke-width="2"/>
        <text x="150" y="40" font-family="Arial, sans-serif" font-size="28" text-anchor="middle" fill="#224466" font-weight="bold">Monitoring</text>
        <text x="30" y="80" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Performance Monitoring:</text>
        {performance_monitoring}
        <text x="30" y="120" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Model Updates:</text>
        {model_updates}
        <text x="30" y="160" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Maintenance Plan:</text>
        {maintenance_plan}
    </g>
    <!-- Ethics &amp Compliance (Larger) -->
    <g transform="translate(500, 550)">
        <rect width="650" height="175" fill="#f0f7ff" stroke="#224466" stroke-width="2"/>
        <text x="325" y="40" font-family="Arial, sans-serif" font-size="28" text-anchor="middle" fill="#224466" font-weight="bold">Ethics &amp; Compliance</text>
        <text x="30" y="80" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Bias &amp; Fairness:</text>
        {bias_fairness}
        <text x="30" y="120" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Privacy &amp; Security:</text>
        {privacy_security}
        <text x="30" y="160" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Regulatory Requirements:</text>
        {regulatory_requirements}
        <text x="380" y="80" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Social Impact:</text>
        {social_impact}
        <text x="380" y="120" font-family="Arial, sans-serif" font-size="20" fill="#224466">• Environmental Impact:</text>
        {environmental_impact}
    </g>
</svg>'''
    def process_text(text, x, y, line_height=20):
        if not text:
            return ""
        lines = text.split('\n')
        svg_text = []
        for i, line in enumerate(lines):
            if line.strip():  # Only add non-empty lines
                svg_text.append(f'<text x="{x}" y="{y + i * line_height}" font-family="Arial, sans-serif" font-size="16" fill="#224466">{line}</text>')
        return '\n'.join(svg_text)
    # Get values from widgets and process them
    values = {}
    for key, widget in widgets_dict.items():
        text = widget.value
        if key in ['business_objectives', 'success_criteria', 'stakeholders', 'user_requirements', 'project_constraints']:
            values[key] = process_text(text, 30, 100)
        elif key in ['available_data', 'data_quality', 'data_requirements']:
            values[key] = process_text(text, 30, 100)
        elif key in ['model_selection', 'performance_metrics', 'model_constraints']:
            values[key] = process_text(text, 30, 100)
        elif key in ['computing_resources', 'deployment_environment', 'scalability_needs']:
            values[key] = process_text(text, 30, 100)
        elif key in ['performance_monitoring', 'model_updates', 'maintenance_plan']:
            values[key] = process_text(text, 30, 100)
        elif key in ['bias_fairness', 'privacy_security', 'regulatory_requirements']:
            values[key] = process_text(text, 30, 100)
        elif key in ['social_impact', 'environmental_impact']:
            values[key] = process_text(text, 380, 100)
    # Replace placeholders with processed values
    svg_content = svg_template.format(**values)
    
    # Save the SVG file
    with open('ml_project_canvas.svg', 'w') as f:
        f.write(svg_content)
    
    # Display the generated SVG
    display(SVG(svg_content))
    print("SVG file generated as 'ml_project_canvas.svg'")
```

Now, we define a function to create the layout and puts all elements together.

```python
def create_layout():
    widgets_dict = create_form_widgets()
    
    # Create the form layout
    form_layout_def = widgets.VBox([
        widgets.HTML('<h3>Problem Definition</h3>'),
        widgets_dict['business_objectives'],
        widgets_dict['success_criteria'],
        widgets_dict['stakeholders'],
        widgets_dict['user_requirements'],
        widgets_dict['project_constraints']
    ])
    form_layout_data = widgets.VBox([
        widgets.HTML('<h3>Data</h3>'),
        widgets_dict['available_data'],
        widgets_dict['data_quality'],
        widgets_dict['data_requirements']
    ])
    form_layout_model = widgets.VBox([
        widgets.HTML('<h3>Model</h3>'),
        widgets_dict['model_selection'],
        widgets_dict['performance_metrics'],
        widgets_dict['model_constraints']
    ])
    form_layout_infra = widgets.VBox([
        widgets.HTML('<h3>Infrastructure</h3>'),
        widgets_dict['computing_resources'],
        widgets_dict['deployment_environment'],
        widgets_dict['scalability_needs']
    ])
    form_layout_mon = widgets.VBox([
        widgets.HTML('<h3>Monitoring</h3>'),
        widgets_dict['performance_monitoring'],
        widgets_dict['model_updates'],
        widgets_dict['maintenance_plan']
    ])
    form_layout_eth = widgets.VBox([        
        widgets.HTML('<h3>Ethics & Compliance</h3>'),
        widgets_dict['bias_fairness'],
        widgets_dict['privacy_security'],
        widgets_dict['regulatory_requirements'],
        widgets_dict['social_impact'],
        widgets_dict['environmental_impact']
    ])
    # Add the widgets in horizontal layout
    form_layout_widgets = widgets.HBox([form_layout_def, form_layout_eth, form_layout_data, form_layout_model, form_layout_infra, form_layout_mon])
    # Create the generate button
    generate_button = widgets.Button(description='Generate Canvas')
    generate_button.on_click(lambda b: generate_svg(widgets_dict))
    # Add the button to the layout
    form_layout = widgets.VBox([form_layout_widgets, generate_button])
    return form_layout, widgets_dict
```

We now can display the interactive canvas

```python
layout, widgets_dict = create_layout()
display(layout)
```

#### Exercise 1: Problem Analysis and Requirements Engineering
In this exercise, you will analyze a real-world problem and apply the systems engineering approach to determine if ML is an appropriate solution.

**Scenario**: A local hospital wants to improve patient wait times in their emergency department.

**Tasks**:
1. Using the ML Project Canvas framework:
   - Define the business objectives
   - Identify key stakeholders
   - List potential success criteria
   - Document user requirements
   - Identify project constraints

2. Analyze whether ML is necessary for this problem:
   - What are the key variables to consider?
   - What metrics would be important to track?
   - What data would be needed?
   - Could this be solved without ML?

**Deliverables**:
- A detailed problem analysis document
- A decision matrix comparing ML vs non-ML solutions
- A data requirements specification

#### Exercise 2: Systems Thinking and Context Analysis
This exercise focuses on understanding the broader context of ML applications.

**Scenario**: A city wants to implement an AI-based traffic management system.

**Tasks**:
1. Apply systems thinking to analyze the problem:
   - Identify different system views (technical, social, economic)
   - Map the system dynamics
   - Consider agility requirements

2. Evaluate potential impacts:
   - Social impact analysis
   - Environmental considerations
   - Ethical implications
   - Security and privacy concerns

**Deliverables**:
- A systems analysis report
- An impact assessment matrix
- A risk mitigation plan

#### Exercise 3: ML Project Planning
This exercise helps develop skills in planning ML projects using the systems engineering approach.

**Scenario**: You are tasked with developing a predictive maintenance system for industrial machinery.

**Tasks**:
1. Create a comprehensive project plan:
   - Define the problem scope
   - Identify required resources
   - Plan the development phases
   - Define monitoring and maintenance requirements

2. Develop a technical specification:
   - Model requirements
   - Data requirements
   - Infrastructure needs
   - Performance metrics

**Deliverables**:
- A detailed project plan
- A technical specification document
- A monitoring and maintenance strategy

#### Resources
- [ML Project Canvas Template](https://cabrerac.github.io/assets/slides/25-udenar-ml-intro/problem-first.html#60)
- [NASA Systems Engineering Guide](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)
- [Ethical AI Guidelines](https://www.unesco.org/en/artificial-intelligence/recommendation-ethics)

<!-- end NOTEBOOK: -->