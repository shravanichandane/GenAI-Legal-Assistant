"""
Module 14: Research Layer
Generates a LaTeX paper summarizing the findings, methodology, and results.
"""
import os

def generate_latex_paper(title: str, authors: str, abstract: str, results_summary: str, output_path: str):
    """
    Generates a basic LaTeX document with the provided content.
    """
    latex_template = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{graphicx}}
\\usepackage{{hyperref}}

\\title{{{title}}}
\\author{{{authors}}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
{abstract}
\\end{{abstract}}

\\section{{Introduction}}
This paper presents the methodology and results of our recent experiments in building a scalable GenAI system. We discuss the architecture, the models evaluated, and the performance benchmarks achieved.

\\section{{Methodology}}
Our approach involved building a modular architecture comprising data ingestion, processing, modeling, and analytics layers. We utilized state-of-the-art LLMs and benchmarked their throughput and accuracy.

\\section{{Results}}
{results_summary}

\\section{{Conclusion}}
The findings indicate significant improvements in processing speed and reliability when utilizing the proposed architecture. Future work will focus on optimizing the models further and expanding the dataset.

\\end{{document}}
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(latex_template)
    
    print(f"LaTeX paper generated successfully at {output_path}")

if __name__ == "__main__":
    sample_results = "The experiments showed a 20\\% increase in throughput using the turbo model compared to the baseline v1. Accuracy remained stable at 95\\%."
    generate_latex_paper(
        title="Scaling GenAI Workloads: A Comprehensive Benchmark",
        authors="AI Research Team",
        abstract="In this paper, we evaluate the performance of various LLM endpoints in a production-like environment, highlighting key metrics such as latency, throughput, and accuracy.",
        results_summary=sample_results,
        output_path="research_output/draft_paper.tex"
    )
