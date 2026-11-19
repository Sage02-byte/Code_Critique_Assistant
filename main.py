
import sys
from engine import analyze_code_snippet
from model import CodeReviewReport

def print_seprator(char = "=", length = 60):
    print(char * length)

def main():
    print_seprator()
    print("CodeCritique AI: Local Senior Code Reviewer")
    print_seprator()
    
    print("Instructions: Paste your multi-line code snippet below.")
    print("When you are finished, type 'RUN' on a new line and press Enter to start review.\n")

    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "RUN":
                break
            lines.append(line)
        except EOFError:
            break

        code_snippet = "\n".join(lines).strip()

        if not code_snippet:
            print("\n[!] No code provided/ Exiting.")
            return
    print("Sending code to local LLama.Cpp server for analysis...")

    try:
        report: CodeReviewReport = analyze_code_snippet(code_snippet)

        print("\n" + "="*20 + " CODE REVIEW REPORT " + "="*20)
        print(f"\n Summary: {report.summary}")
        print(f"\n Severity Score: {report.severity_score}/10")

        print(f"\n Bugs & Issues Identified ({len(report.bug_identification)}):")

        if not report.bug_identification:
            print("No bug found. Clean code")

        else:
            for i, bug in enumerate(report.bug_identification, 1):
                line_str = f"[Line {bug.description}]" if bug.line_number else ""
                print(f"{i}.{line_str} {bug.description}")
                print(f"Fix: {bug.fix_suggestion}")

        print(f"\n Refactored Code:\n")
        print(report.refactored_code)

        print(f"\n Suggested Test Skeleton:\n")
        print(report.suggestion_test)
        print("\n" + "="*60)

    except Exception as e:
        print(f"\n[Error] Review failed: {e}")



if __name__ == "__main__":
    main()
