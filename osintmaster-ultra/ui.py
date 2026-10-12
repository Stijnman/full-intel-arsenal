"""Small Gradio interface to real public-domain checks."""
from __future__ import annotations

import gradio as gr

from engine import scan_domain


def run_scan(target: str) -> dict:
    try:
        return scan_domain(target)
    except ValueError as exc:
        return {"status": "invalid_target", "error": str(exc)}


with gr.Blocks(title="OSINTMaster Ultra — Public Domain MVP") as demo:
    gr.Markdown("# OSINTMaster Ultra — Public Domain MVP")
    gr.Markdown(
        "Real DNS and HTTPS evidence for publicly reachable domains. "
        "This MVP does not enumerate people's accounts, emails or breaches."
    )
    with gr.Row():
        target = gr.Textbox(
            label="Public domain", placeholder="example.com", scale=3
        )
        run_button = gr.Button("Inspect domain", variant="primary", scale=1)
    output = gr.JSON(label="Source-backed observations")
    run_button.click(fn=run_scan, inputs=target, outputs=output)
    target.submit(fn=run_scan, inputs=target, outputs=output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8501, share=False)
