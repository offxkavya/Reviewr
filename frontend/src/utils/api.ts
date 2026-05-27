export interface ReviewComment {
  line_number: number;
  severity: "critical" | "warning" | "info";
  message: string;
  suggestion: string;
}

export interface ReviewResponse {
  comments: ReviewComment[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function sendCodeForReview(code: string, language?: string): Promise<ReviewResponse> {
  const response = await fetch(`${API_BASE_URL}/review`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code, language }),
  });

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.detail || "Failed to analyze code. Please try again.");
  }

  return response.json();
}

export function getLocalMockComments(code: string): ReviewComment[] {
  const comments: ReviewComment[] = [];
  const lines = code.split("\n");
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    const lineNo = i + 1;
    
    if (line.includes("eval(")) {
      comments.push({
        line_number: lineNo,
        severity: "critical",
        message: "Dangerous execution via eval() detected. This is a critical security vulnerability that allows execution of arbitrary strings.",
        suggestion: "Use structural parsing (e.g., JSON.parse() or ast.literal_eval() in Python) instead."
      });
    } else if (line.includes("print(") || line.includes("console.log(")) {
      comments.push({
        line_number: lineNo,
        severity: "info",
        message: "Debugging print statements should be cleaned up or migrated to a production logger.",
        suggestion: "Replace with appropriate logging level calls (e.g. logger.info() or logging.info())."
      });
    } else if (line.includes("TODO")) {
      comments.push({
        line_number: lineNo,
        severity: "warning",
        message: "Unfinished development checklist item (TODO) identified.",
        suggestion: "Verify if this work has been scheduled or complete the implementation."
      });
    } else if (line.includes("except:") || (line.includes("catch") && line.includes("{}"))) {
      comments.push({
        line_number: lineNo,
        severity: "warning",
        message: "Empty or bare try-except/catch block. This swallows errors and makes debugging hard.",
        suggestion: "Log the exception stack trace or raise a refined custom error."
      });
    }
  }
  
  if (comments.length === 0) {
    comments.push({
      line_number: 1,
      severity: "info",
      message: "The code looks solid! No immediate bugs detected by our static rule sets.",
      suggestion: "Add standard documentation comments (docstrings or JSDoc) to explain interface logic."
    });
  }
  
  return comments;
}
