from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from rag import search_sop
from tools import (
    get_sales_data,
    get_total_sales,
    get_lowest_sales_product,
    get_highest_sales_product
)


@tool
def sales_data():
    """Get complete sales data from the CSV file."""
    return get_sales_data()


@tool
def total_sales():
    """Calculate total sales across all records."""
    return get_total_sales()


@tool
def lowest_sales_product():
    """Find the product with the lowest sales."""
    return get_lowest_sales_product()


@tool
def highest_sales_product():
    """Find the product with the highest sales."""
    return get_highest_sales_product()


@tool
def search_sales_sop(question: str):
    """Search sales SOP documents for policies and procedures."""
    return search_sop(question)


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)



SYSTEM_PROMPT = """
You are a sales assistant for a demonstration project.

Rules:
1. Use sales tools for sales numbers and product questions.
2. Use search_sales_sop for questions about policies and procedures.
3. Do not invent sales figures or policy details.
4. Answer using the information returned by the tools.
5. If the SOP does not contain the answer, clearly say
   that the information is not available in the provided SOP.
6. Keep answers clear and concise.
7. Never show raw tool-call JSON to the user.
8. For questions not answered by the SOP, say:
   "This information is not available in the provided SOP."
9. Always execute the selected tool and use its result
   before generating the final answer.





"""


agent = create_react_agent(
    model=llm,
    tools=[
        sales_data,
        total_sales,
        lowest_sales_product,
        highest_sales_product,
        search_sales_sop
    ],
    prompt=SYSTEM_PROMPT
)


def ask_agent(question: str) -> str:
    try:
        response = agent.invoke({
            "messages": [
                {"role": "user", "content": question}
            ]
        })

        for message in reversed(response["messages"]):
            if (
                getattr(message, "type", "") == "ai"
                and message.content
                and not getattr(message, "tool_calls", [])
            ):
                return str(message.content)

        return "Agent could not generate a final answer."

    except Exception as error:
        return f"Agent error: {error}"