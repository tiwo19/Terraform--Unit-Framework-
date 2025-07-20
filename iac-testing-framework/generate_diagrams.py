"""
Architecture Diagram Generator for Phase 2 MSc Report
This script generates ASCII art diagrams for the MSc report
"""

def generate_phase2_architecture_diagram():
    """Generate the Phase 2 system architecture diagram"""
    
    architecture_diagram = """
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                          IaC Testing Framework - Phase 2                        │
    │                              System Architecture                                │
    └─────────────────────────────────────────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                                CLI Interface                                    │
    │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
    │  │ python cli.py   │  │ test_runner.py  │  │ demo_phase2.py  │                │
    │  │ static          │  │ combined        │  │                 │                │
    │  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
    └─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                              Core Framework                                     │
    │                                                                                 │
    │  ┌─────────────────────────────────┐    ┌─────────────────────────────────┐   │
    │  │        Static Analysis          │    │     Policy Compliance           │   │
    │  │         Module                  │    │         Module                  │   │
    │  │                                 │    │                                 │   │
    │  │  ┌─────────────────────────┐    │    │  ┌─────────────────────────┐    │   │
    │  │  │   terraform validate    │    │    │  │    Policy Engine        │    │   │
    │  │  │   • Syntax validation   │    │    │  │    • YAML policies      │    │   │
    │  │  │   • Configuration check │    │    │  │    • Resource validation│    │   │
    │  │  └─────────────────────────┘    │    │  └─────────────────────────┘    │   │
    │  │                                 │    │                                 │   │
    │  │  ┌─────────────────────────┐    │    │  ┌─────────────────────────┐    │   │
    │  │  │       TFLint            │    │    │  │   Compliance Checker    │    │   │
    │  │  │   • Best practices      │    │    │  │   • Rule validation     │    │   │
    │  │  │   • Linting rules       │    │    │  │   • Violation tracking  │    │   │
    │  │  └─────────────────────────┘    │    │  └─────────────────────────┘    │   │
    │  │                                 │    │                                 │   │
    │  │  ┌─────────────────────────┐    │    │  ┌─────────────────────────┐    │   │
    │  │  │       Checkov           │    │    │  │    OPA Integration      │    │   │
    │  │  │   • Security scanning   │    │    │  │    • Open Policy Agent  │    │   │
    │  │  │   • Compliance checks   │    │    │  │    • Advanced policies  │    │   │
    │  │  └─────────────────────────┘    │    │  └─────────────────────────┘    │   │
    │  └─────────────────────────────────┘    └─────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                              Reporting Layer                                   │
    │                                                                                 │
    │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
    │  │   JSON Output   │  │ Console Reports │  │  Summary Stats  │                │
    │  │   • Detailed    │  │ • Pass/Fail     │  │  • Compliance % │                │
    │  │   • Structured  │  │ • Colored       │  │  • Issue count  │                │
    │  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
    └─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                              Data Storage                                       │
    │                                                                                 │
    │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
    │  │ Terraform Files │  │ Policy Files    │  │ Report Files    │                │
    │  │ • .tf configs   │  │ • YAML policies │  │ • JSON reports  │                │
    │  │ • Examples      │  │ • Custom rules  │  │ • Demo outputs  │                │
    │  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
    └─────────────────────────────────────────────────────────────────────────────────┘
    
    Legend:
    ━━━━━ Data Flow
    ┌───┐ Component
    ▼     Direction
    """
    
    return architecture_diagram

def generate_module_interaction_flowchart():
    """Generate the module interaction flowchart"""
    
    flowchart = """
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                     Module Interaction Flowchart - Phase 2                     │
    └─────────────────────────────────────────────────────────────────────────────────┘
    
                                    ┌─────────────────┐
                                    │   User Input    │
                                    │ CLI Command     │
                                    └─────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │  Parse Command  │
                                    │  & Arguments    │
                                    └─────────────────┘
                                             │
                                   ┌─────────┴─────────┐
                                   │                   │
                                   ▼                   ▼
                           ┌─────────────┐     ┌─────────────┐
                           │   Static    │     │   Policy    │
                           │  Analysis   │     │ Compliance  │
                           │   Module    │     │   Module    │
                           └─────────────┘     └─────────────┘
                                   │                   │
                                   ▼                   ▼
                           ┌─────────────┐     ┌─────────────┐
                           │ Validate    │     │ Load        │
                           │ Directory   │     │ Policies    │
                           │ & Files     │     │ from YAML   │
                           └─────────────┘     └─────────────┘
                                   │                   │
                                   ▼                   ▼
                           ┌─────────────┐     ┌─────────────┐
                           │ Run Tools:  │     │ Parse       │
                           │ • terraform │     │ Terraform   │
                           │ • TFLint    │     │ Resources   │
                           │ • Checkov   │     │             │
                           └─────────────┘     └─────────────┘
                                   │                   │
                                   ▼                   ▼
                           ┌─────────────┐     ┌─────────────┐
                           │ Aggregate   │     │ Apply       │
                           │ Tool        │     │ Policy      │
                           │ Results     │     │ Rules       │
                           └─────────────┘     └─────────────┘
                                   │                   │
                                   ▼                   ▼
                           ┌─────────────┐     ┌─────────────┐
                           │ Generate    │     │ Calculate   │
                           │ Static      │     │ Compliance  │
                           │ Summary     │     │ Score       │
                           └─────────────┘     └─────────────┘
                                   │                   │
                                   └─────────┬─────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ Combine Results │
                                    │ & Generate      │
                                    │ Final Report    │
                                    └─────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ Output Format:  │
                                    │ • JSON File     │
                                    │ • Console       │
                                    │ • Summary       │
                                    └─────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ Framework       │
                                    │ Execution       │
                                    │ Complete        │
                                    └─────────────────┘
    
    Error Handling Flow:
    
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ Tool Not    │ ──▶ │ Graceful    │ ──▶ │ Continue    │ ──▶ │ Report      │
    │ Found       │     │ Degradation │     │ Execution   │     │ Status      │
    └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
    
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ Invalid     │ ──▶ │ Error       │ ──▶ │ Log &       │ ──▶ │ Partial     │
    │ Input       │     │ Capture     │     │ Continue    │     │ Results     │
    └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
    """
    
    return flowchart

def generate_data_flow_diagram():
    """Generate the data flow diagram"""
    
    data_flow = """
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                           Data Flow Diagram - Phase 2                          │
    └─────────────────────────────────────────────────────────────────────────────────┘
    
    Input Data Sources:
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │ Terraform Files │    │ Policy Files    │    │ Configuration   │
    │ • main.tf       │    │ • sample.yaml   │    │ • CLI args      │
    │ • variables.tf  │    │ • custom.json   │    │ • settings      │
    │ • outputs.tf    │    │ • rules.yaml    │    │ • options       │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
            │                       │                       │
            │                       │                       │
            ▼                       ▼                       ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │ File Parser     │    │ Policy Loader   │    │ Config Parser   │
    │ • Read .tf      │    │ • Parse YAML    │    │ • Parse args    │
    │ • Extract       │    │ • Validate      │    │ • Set options   │
    │   resources     │    │   schema        │    │                 │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
            │                       │                       │
            └───────────┬───────────┘                       │
                        │                                   │
                        ▼                                   │
            ┌─────────────────────────────────┐             │
            │     Processing Engine           │             │
            │                                 │             │
            │  ┌─────────────────────────┐    │             │
            │  │  Static Analysis        │    │             │
            │  │  • terraform validate   │    │             │
            │  │  • TFLint execution     │    │◀────────────┘
            │  │  • Checkov scanning     │    │
            │  └─────────────────────────┘    │
            │                                 │
            │  ┌─────────────────────────┐    │
            │  │  Policy Compliance      │    │
            │  │  • Rule application     │    │
            │  │  • Violation detection  │    │
            │  │  • Score calculation    │    │
            │  └─────────────────────────┘    │
            └─────────────────────────────────┘
                        │
                        ▼
            ┌─────────────────────────────────┐
            │     Result Aggregation          │
            │                                 │
            │  ┌─────────────────────────┐    │
            │  │  Data Combination       │    │
            │  │  • Merge results        │    │
            │  │  • Calculate summary    │    │
            │  │  • Format output        │    │
            │  └─────────────────────────┘    │
            └─────────────────────────────────┘
                        │
                        ▼
    Output Data Formats:
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │ JSON Reports    │    │ Console Output  │    │ Summary Stats   │
    │ • Detailed      │    │ • Pass/Fail     │    │ • Compliance %  │
    │ • Structured    │    │ • Colored text  │    │ • Issue counts  │
    │ • Machine       │    │ • Human readable│    │ • Scores        │
    │   readable      │    │                 │    │                 │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
    """
    
    return data_flow

def save_diagrams():
    """Save all diagrams to files"""
    
    diagrams = {
        "architecture_phase2.txt": generate_phase2_architecture_diagram(),
        "flowchart_phase2.txt": generate_module_interaction_flowchart(),
        "dataflow_phase2.txt": generate_data_flow_diagram()
    }
    
    for filename, content in diagrams.items():
        with open(f"diagrams/{filename}", 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Generated: {filename}")
    
    print("\n📊 All diagrams generated successfully!")
    print("These can be converted to PNG/PDF for the MSc report using:")
    print("- Online ASCII to image converters")
    print("- LaTeX with verbatim environments")
    print("- Markdown code blocks")

if __name__ == "__main__":
    save_diagrams()
