import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import create_retriever_tool
from langchain_core.messages import ToolMessage

from rag import create_vectorstore
from tools import get_order_status


# =========================================================
# 1. Load environment variables
# =========================================================

load_dotenv()


# =========================================================
# 2. Create policy vector store
# =========================================================

vectorstore = create_vectorstore()


# =========================================================
# 3. Create policy retriever
# =========================================================

policy_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


# =========================================================
# 4. Convert retriever into a tool
# =========================================================

policy_search = create_retriever_tool(
    policy_retriever,
    name="policy_search",
    description=(
        "Search company policies about returns, refunds, shipping, "
        "and cancellations. Use this when the customer asks about "
        "company rules or whether an order can be returned or refunded."
    )
)


# =========================================================
# 5. Create Gemini model
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini- 3.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)


# =========================================================
# 6. Give Gemini access to both tools
# =========================================================

tools = [
    policy_search,
    get_order_status
]


tools_by_name = {
    tool.name: tool
    for tool in tools
}


llm_with_tools = llm.bind_tools(tools)


# =========================================================
# 7. AI Customer Support Agent
# =========================================================

def ask_agent(question):

    # Prevent empty questions
    if not question or not question.strip():
        return "Please enter a question."

    messages = [
        (
            "system",
            """
You are a professional AI customer support assistant.

Your responsibilities:

1. Answer questions about orders, shipping, returns, refunds,
   and cancellations.

2. Use get_order_status for order-specific questions.

3. Use policy_search for return, refund, shipping,
   and cancellation policies.

4. For questions such as:
   "Can I return ORD1001?"
   check the order and relevant policy before answering.

5. Never show raw policy documents or large retrieved text.
   Give a clear and concise answer.

6. Never say an order is cancelled unless the database confirms it.

Conversation behavior:

7. If the customer says:
   "okay", "thanks", "thank you", or similar after receiving
   an answer, ask:
   "Is there anything else you'd like to know about your order?"

8. If the customer says:
   "no", "no thanks", "that's all", "it's okay",
   or similar, respond:
   "Thank you for contacting customer support. Have a nice day!"

9. Keep responses natural, short, and professional.
"""
        ),
        (
            "human",
            question.strip()
        )
    ]


    # =====================================================
    # 8. Allow multiple tool calls
    # =====================================================

    for _ in range(5):

        response = llm_with_tools.invoke(messages)

        # Add Gemini response to conversation
        messages.append(response)


        # =================================================
        # No tool required
        # =================================================

        if not response.tool_calls:

            if isinstance(response.content, list):

                return "".join(
                    item.get("text", "")
                    for item in response.content
                    if isinstance(item, dict)
                    and item.get("type") == "text"
                )

            return response.content


        # =================================================
        # Execute requested tools
        # =================================================

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            tool_args = tool_call["args"]

            print(
                f"\n[AI selected tool: {tool_name}]"
            )

            # Find tool
            tool = tools_by_name.get(tool_name)

            if tool is None:

                messages.append(
                    ToolMessage(
                        content=f"Unknown tool: {tool_name}",
                        tool_call_id=tool_call["id"]
                    )
                )

                continue


            # Execute tool
            result = tool.invoke(tool_args)


            # Send result back to Gemini
            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
            )


    # =====================================================
    # If agent cannot complete within 5 iterations
    # =====================================================

    return "I could not complete the request."