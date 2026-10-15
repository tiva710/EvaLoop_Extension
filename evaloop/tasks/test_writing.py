from .code_summarization import CodeSummarizationTask
from .factory import register_task


@register_task("assert_writing")
class AssertWritingTask(CodeSummarizationTask):
    def create_prompt(self, input_text: str) -> str:
        return (
            "Write Python assert statements that fully specify what the following code does. "
            "Write as many as needed, including edge cases.\n\n"
            f"```\n{input_text}\n```\n\n"
            "Return only the assert statements, one per line."
        )

    def extract_output(self, raw_response: str) -> str:
        #Keep only asserts
        lines = [line.strip() for line in raw_response.splitlines()]
        return "\n".join(line for line in lines if line.startswith("assert"))
