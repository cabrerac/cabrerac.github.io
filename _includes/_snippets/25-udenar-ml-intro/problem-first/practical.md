<!-- NOTEBOOK: -->

# Practical Introduction

#### Submission Guidelines
- Submit your solution as a Jupyter notebook with the following name format: cease_ml_intro_session_1_<email_username>.ipynb
- Include clear comments explaining your code
- Provide a written analysis of your results
- Include test cases and their outputs
- Due date: [29/05/2025]

#### Interactive ML Project Canvas

The following blocks of code create and interactive Canvas we can use in our practical session

Run the code and then fill the form to populate the ML Project Canvas. The canvas will update in real-time as you type.

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
        description='Business Objectives:',
        placeholder='Enter business objectives...',
        rows=3
    )
    widgets_dict['success_criteria'] = widgets.Textarea(
        description='Success Criteria:',
        placeholder='Enter success criteria...',
        rows=3
    )
    widgets_dict['stakeholders'] = widgets.Textarea(
        description='Stakeholders:',
        placeholder='Enter stakeholders...',
        rows=3
    )
    widgets_dict['user_requirements'] = widgets.Textarea(
        description='User Requirements:',
        placeholder='Enter user requirements...',
        rows=3
    )
    widgets_dict['project_constraints'] = widgets.Textarea(
        description='Project Constraints:',
        placeholder='Enter project constraints...',
        rows=3
    )
    
    # Data
    widgets_dict['available_data'] = widgets.Textarea(
        description='Available Data:',
        placeholder='Enter available data...',
        rows=2
    )
    widgets_dict['data_quality'] = widgets.Textarea(
        description='Data Quality:',
        placeholder='Enter data quality considerations...',
        rows=2
    )
    widgets_dict['data_requirements'] = widgets.Textarea(
        description='Data Requirements:',
        placeholder='Enter data requirements...',
        rows=2
    )
    
    # Model
    widgets_dict['model_selection'] = widgets.Textarea(
        description='Model Selection:',
        placeholder='Enter model selection criteria...',
        rows=2
    )
    widgets_dict['performance_metrics'] = widgets.Textarea(
        description='Performance Metrics:',
        placeholder='Enter performance metrics...',
        rows=2
    )
    widgets_dict['model_constraints'] = widgets.Textarea(
        description='Model Constraints:',
        placeholder='Enter model constraints...',
        rows=2
    )
    
    # Infrastructure
    widgets_dict['computing_resources'] = widgets.Textarea(
        description='Computing Resources:',
        placeholder='Enter computing resources...',
        rows=2
    )
    widgets_dict['deployment_environment'] = widgets.Textarea(
        description='Deployment Environment:',
        placeholder='Enter deployment environment...',
        rows=2
    )
    widgets_dict['scalability_needs'] = widgets.Textarea(
        description='Scalability Needs:',
        placeholder='Enter scalability needs...',
        rows=2
    )
    
    # Monitoring
    widgets_dict['performance_monitoring'] = widgets.Textarea(
        description='Performance Monitoring:',
        placeholder='Enter performance monitoring plan...',
        rows=2
    )
    widgets_dict['model_updates'] = widgets.Textarea(
        description='Model Updates:',
        placeholder='Enter model update strategy...',
        rows=2
    )
    widgets_dict['maintenance_plan'] = widgets.Textarea(
        description='Maintenance Plan:',
        placeholder='Enter maintenance plan...',
        rows=2
    )
    
    # Ethics & Compliance
    widgets_dict['bias_fairness'] = widgets.Textarea(
        description='Bias & Fairness:',
        placeholder='Enter bias and fairness considerations...',
        rows=2
    )
    widgets_dict['privacy_security'] = widgets.Textarea(
        description='Privacy & Security:',
        placeholder='Enter privacy and security measures...',
        rows=2
    )
    widgets_dict['regulatory_requirements'] = widgets.Textarea(
        description='Regulatory Requirements:',
        placeholder='Enter regulatory requirements...',
        rows=2
    )
    widgets_dict['social_impact'] = widgets.Textarea(
        description='Social Impact:',
        placeholder='Enter social impact considerations...',
        rows=2
    )
    widgets_dict['environmental_impact'] = widgets.Textarea(
        description='Environmental Impact:',
        placeholder='Enter environmental impact considerations...',
        rows=2
    )
    
    return widgets_dict
```

We then define the function to create the canvas display. The display uses the diagram we saw in the slides.

```python
def create_canvas_display():
    # Try to load the SVG from the local file system first
    local_paths = [
        '{{ site.url }}/assets/media/diagrams/ml-project-canvas.svg',
        '../assets/media/diagrams/ml-project-canvas.svg',
        '../../assets/media/diagrams/ml-project-canvas.svg'
    ]
    
    svg_content = None
    for path in local_paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                svg_content = f.read()
            break
    
    # If local file not found, try to download from the web
    if svg_content is None:
        try:
            # Try to get the SVG from the web
            response = requests.get('{{ site.url }}/assets/media/diagrams/ml-project-canvas.svg')
            if response.status_code == 200:
                svg_content = response.text
        except:
            pass
    
    # If still no content, use a fallback SVG
    if svg_content is None:
        svg_content = '''
        <svg width="1200" height="800" viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
            <!-- Add a message if SVG file is not found -->
            <text x="600" y="400" font-family="Arial" font-size="24" text-anchor="middle">
                ML Project Canvas SVG file not found. Please ensure the file exists at assets/media/diagrams/ml-project-canvas.svg
            </text>
        </svg>
        '''
    
    # Create an HTML widget to display the SVG
    svg_widget = widgets.HTML(value=f'<div style="width: 100%; height: 800px;">{svg_content}</div>')
    return svg_widget, svg_content
```

Now, we define a function to create the layout and puts all elements together.

```python
def create_layout():
    widgets_dict = create_form_widgets()
    
    # Create the form layout
    form_layout = widgets.VBox([
        widgets.HTML('<h3>Problem Definition</h3>'),
        widgets_dict['business_objectives'],
        widgets_dict['success_criteria'],
        widgets_dict['stakeholders'],
        widgets_dict['user_requirements'],
        widgets_dict['project_constraints'],
        
        widgets.HTML('<h3>Data</h3>'),
        widgets_dict['available_data'],
        widgets_dict['data_quality'],
        widgets_dict['data_requirements'],
        
        widgets.HTML('<h3>Model</h3>'),
        widgets_dict['model_selection'],
        widgets_dict['performance_metrics'],
        widgets_dict['model_constraints'],
        
        widgets.HTML('<h3>Infrastructure</h3>'),
        widgets_dict['computing_resources'],
        widgets_dict['deployment_environment'],
        widgets_dict['scalability_needs'],
        
        widgets.HTML('<h3>Monitoring</h3>'),
        widgets_dict['performance_monitoring'],
        widgets_dict['model_updates'],
        widgets_dict['maintenance_plan'],
        
        widgets.HTML('<h3>Ethics & Compliance</h3>'),
        widgets_dict['bias_fairness'],
        widgets_dict['privacy_security'],
        widgets_dict['regulatory_requirements'],
        widgets_dict['social_impact'],
        widgets_dict['environmental_impact']
    ])
    
    # Create the canvas display
    canvas_display, original_svg = create_canvas_display()
    
    # Define the mapping between widgets and SVG text elements
    svg_mapping = {
        # Problem Definition section (x: 50, y: 100)
        'business_objectives': {'x': 80, 'y': 120, 'group': 0},
        'success_criteria': {'x': 80, 'y': 150, 'group': 0},
        'stakeholders': {'x': 80, 'y': 180, 'group': 0},
        'user_requirements': {'x': 80, 'y': 210, 'group': 0},
        'project_constraints': {'x': 80, 'y': 240, 'group': 0},
        
        # Data section (x: 500, y: 100)
        'available_data': {'x': 530, 'y': 120, 'group': 1},
        'data_quality': {'x': 530, 'y': 150, 'group': 1},
        'data_requirements': {'x': 530, 'y': 180, 'group': 1},
        
        # Model section (x: 850, y: 100)
        'model_selection': {'x': 880, 'y': 120, 'group': 2},
        'performance_metrics': {'x': 880, 'y': 150, 'group': 2},
        'model_constraints': {'x': 880, 'y': 180, 'group': 2},
        
        # Infrastructure section (x: 500, y: 325)
        'computing_resources': {'x': 530, 'y': 345, 'group': 3},
        'deployment_environment': {'x': 530, 'y': 375, 'group': 3},
        'scalability_needs': {'x': 530, 'y': 405, 'group': 3},
        
        # Monitoring section (x: 850, y: 325)
        'performance_monitoring': {'x': 880, 'y': 345, 'group': 4},
        'model_updates': {'x': 880, 'y': 375, 'group': 4},
        'maintenance_plan': {'x': 880, 'y': 405, 'group': 4},
        
        # Ethics & Compliance section (x: 500, y: 550)
        'bias_fairness': {'x': 530, 'y': 570, 'group': 5},
        'privacy_security': {'x': 530, 'y': 600, 'group': 5},
        'regulatory_requirements': {'x': 530, 'y': 630, 'group': 5},
        'social_impact': {'x': 880, 'y': 570, 'group': 5},
        'environmental_impact': {'x': 880, 'y': 600, 'group': 5}
    }
    
    def update_svg(change):
        # Get the current SVG content
        current_svg = original_svg
        
        # Update each text element based on widget values
        for widget_id, coords in svg_mapping.items():
            if widget_id in widgets_dict:
                value = widgets_dict[widget_id].value
                if value:
                    # Split the value into lines and create multiple text elements
                    lines = value.split('\n')
                    text_elements = []
                    for i, line in enumerate(lines):
                        if line.strip():  # Only add non-empty lines
                            y_offset = i * 25  # Add vertical spacing between lines
                            text_element = f'<text x="{coords["x"]}" y="{coords["y"] + y_offset}" font-family="Arial, sans-serif" font-size="16" fill="#224466">{line}</text>'
                            text_elements.append(text_element)
                    
                    # Join all text elements
                    text_content = '\n'.join(text_elements)
                    
                    # Find the appropriate group to insert the text
                    groups = re.findall(r'<g transform="translate\([^)]*\)">', current_svg)
                    if coords['group'] < len(groups):
                        group_pattern = groups[coords['group']]
                        # Remove any existing text elements in this group
                        current_svg = re.sub(f'{group_pattern}.*?<text x="{coords["x"]}"[^>]*>.*?</text>', group_pattern, current_svg)
                        # Add the new text elements
                        current_svg = re.sub(group_pattern, f'{group_pattern}{text_content}', current_svg, count=1)
        
        # Update the SVG display
        canvas_display.value = f'<div style="width: 100%; height: 800px;">{current_svg}</div>'
    
    # Add observers to all widgets
    for widget in widgets_dict.values():
        widget.observe(update_svg, names='value')
    
    # Create the main layout
    main_layout = widgets.HBox([form_layout, canvas_display])
    
    return main_layout, widgets_dict
```

We now can display the interactive canvas

```python
layout, widgets_dict = create_layout()
display(layout)
```

We might want to save the canvas data so we need a function for that.

```python
def save_canvas_state():
    state = {key: widget.value for key, widget in widgets_dict.items()}
    with open('ml_canvas_state.json', 'w') as f:
        json.dump(state, f, indent=2)
    print("Canvas state saved to ml_canvas_state.json")
```

And a button that enables the functionality.

```python
save_button = widgets.Button(description='Save Canvas State')
save_button.on_click(lambda b: save_canvas_state())
display(save_button)
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