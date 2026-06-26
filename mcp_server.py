from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

#Use mcp dev mcp_server.py to run the server

# Write a tool to read a doc
@mcp.tool(
    name="read_document",
    description="Reads the contents of a document and returns it as a string."
)

# Defines the read_doc tool that retrieves the content of a document by its ID
def read_document(
    doc_id: str = Field(description="Id of the document to read.")

):
    #Checks if the document exists in the docs dictionary
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found.")

    return docs[doc_id]

# Write a tool to edit a doc
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)

def edit_document(
    doc_id: str = Field(description="Id of the document to edit."),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace"),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found.")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

# Write a tool to return the contents of a document by ID
@mcp.tool(
    name="get_document_contents",
    description="Returns the contents of a document by its ID."
)

def get_document_contents(
    doc_id: str = Field(description="Id of the document to retrieve.")
):
    if doc_id in docs:
        return docs[doc_id]
    else:
        raise ValueError(f"Document with id {doc_id} not found.")

# Write a tool to add two numbers
@mcp.tool(
    name="add_numbers",
    description="Returns the sum of two numbers."
)

def add_numbers(
    x: float = Field(description="The first number to add."),
    y: float = Field(description="The second number to add.")
):
    if x is None or y is None:
        raise ValueError("Both x and y must be provided.")
    return x + y

# Write a tool to subtract two numbers
@mcp.tool(
    name="subtract_numbers",
    description="Returns the subtraction of two numbers."
)

def subtract_numbers(
    x: float = Field(description="The first number to subtract from"),
    y: float = Field(description="The second number to subtract")
):
    if x is None or y is None:
        raise ValueError("Both x and y must be provided.")
    return x - y
    
@mcp.resource(
    "docs://documents",
    #Returning a string that contains structured JSON data
    mime_type="application/json"
)

# Returns a list of document IDs available in the docs dictionary
def list_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    #Returning a string that contains the plain text content of the document
    mime_type="text/plain"
)

def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
