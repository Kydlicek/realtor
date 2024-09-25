{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 146,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: langchain-openai in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (0.0.8)\n",
      "Requirement already satisfied: langchain in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (0.1.12)\n",
      "Requirement already satisfied: langchain-anthropic in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (0.1.4)\n",
      "Requirement already satisfied: scikit-learn in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (1.4.1.post1)\n",
      "Requirement already satisfied: langchain-core<0.2.0,>=0.1.27 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain-openai) (0.1.32)\n",
      "Requirement already satisfied: openai<2.0.0,>=1.10.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain-openai) (1.14.1)\n",
      "Requirement already satisfied: tiktoken<1,>=0.5.2 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain-openai) (0.6.0)\n",
      "Requirement already satisfied: PyYAML>=5.3 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain) (6.0.1)\n",
      "Requirement already satisfied: SQLAlchemy<3,>=1.4 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain) (2.0.28)\n",
      "Requirement already satisfied: aiohttp<4.0.0,>=3.8.3 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain) (3.9.3)\n",
      "Requirement already satisfied: dataclasses-json<0.7,>=0.5.7 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain) (0.6.4)\n",
      "Requirement already satisfied: jsonpatch<2.0,>=1.33 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain) (1.33)\n",
      "Requirement already satisfied: langchain-community<0.1,>=0.0.28 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain) (0.0.28)\n",
      "Requirement already satisfied: langchain-text-splitters<0.1,>=0.0.1 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain) (0.0.1)\n",
      "Requirement already satisfied: langsmith<0.2.0,>=0.1.17 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain) (0.1.27)\n",
      "Requirement already satisfied: numpy<2,>=1 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain) (1.26.4)\n",
      "Requirement already satisfied: pydantic<3,>=1 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain) (2.6.4)\n",
      "Requirement already satisfied: requests<3,>=2 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain) (2.31.0)\n",
      "Requirement already satisfied: tenacity<9.0.0,>=8.1.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain) (8.2.3)\n",
      "Requirement already satisfied: anthropic<1,>=0.17.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain-anthropic) (0.20.0)\n",
      "Requirement already satisfied: defusedxml<0.8.0,>=0.7.1 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain-anthropic) (0.7.1)\n",
      "Requirement already satisfied: scipy>=1.6.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from scikit-learn) (1.12.0)\n",
      "Requirement already satisfied: joblib>=1.2.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from scikit-learn) (1.3.2)\n",
      "Requirement already satisfied: threadpoolctl>=2.0.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from scikit-learn) (3.3.0)\n",
      "Requirement already satisfied: aiosignal>=1.1.2 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from aiohttp<4.0.0,>=3.8.3->langchain) (1.3.1)\n",
      "Requirement already satisfied: attrs>=17.3.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from aiohttp<4.0.0,>=3.8.3->langchain) (23.2.0)\n",
      "Requirement already satisfied: frozenlist>=1.1.1 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from aiohttp<4.0.0,>=3.8.3->langchain) (1.4.1)\n",
      "Requirement already satisfied: multidict<7.0,>=4.5 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from aiohttp<4.0.0,>=3.8.3->langchain) (6.0.5)\n",
      "Requirement already satisfied: yarl<2.0,>=1.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from aiohttp<4.0.0,>=3.8.3->langchain) (1.9.4)\n",
      "Requirement already satisfied: anyio<5,>=3.5.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from anthropic<1,>=0.17.0->langchain-anthropic) (4.3.0)\n",
      "Requirement already satisfied: distro<2,>=1.7.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from anthropic<1,>=0.17.0->langchain-anthropic) (1.9.0)\n",
      "Requirement already satisfied: httpx<1,>=0.23.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from anthropic<1,>=0.17.0->langchain-anthropic) (0.27.0)\n",
      "Requirement already satisfied: sniffio in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from anthropic<1,>=0.17.0->langchain-anthropic) (1.3.1)\n",
      "Requirement already satisfied: tokenizers>=0.13.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from anthropic<1,>=0.17.0->langchain-anthropic) (0.15.2)\n",
      "Requirement already satisfied: typing-extensions<5,>=4.7 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from anthropic<1,>=0.17.0->langchain-anthropic) (4.10.0)\n",
      "Requirement already satisfied: marshmallow<4.0.0,>=3.18.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from dataclasses-json<0.7,>=0.5.7->langchain) (3.21.1)\n",
      "Requirement already satisfied: typing-inspect<1,>=0.4.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from dataclasses-json<0.7,>=0.5.7->langchain) (0.9.0)\n",
      "Requirement already satisfied: jsonpointer>=1.9 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from jsonpatch<2.0,>=1.33->langchain) (2.4)\n",
      "Requirement already satisfied: packaging<24.0,>=23.2 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langchain-core<0.2.0,>=0.1.27->langchain-openai) (23.2)\n",
      "Requirement already satisfied: orjson<4.0.0,>=3.9.14 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from langsmith<0.2.0,>=0.1.17->langchain) (3.9.15)\n",
      "Requirement already satisfied: tqdm>4 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from openai<2.0.0,>=1.10.0->langchain-openai) (4.66.2)\n",
      "Requirement already satisfied: annotated-types>=0.4.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from pydantic<3,>=1->langchain) (0.6.0)\n",
      "Requirement already satisfied: pydantic-core==2.16.3 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from pydantic<3,>=1->langchain) (2.16.3)\n",
      "Requirement already satisfied: charset-normalizer<4,>=2 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from requests<3,>=2->langchain) (3.3.2)\n",
      "Requirement already satisfied: idna<4,>=2.5 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from requests<3,>=2->langchain) (3.6)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from requests<3,>=2->langchain) (2.2.1)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from requests<3,>=2->langchain) (2024.2.2)\n",
      "Requirement already satisfied: regex>=2022.1.18 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from tiktoken<1,>=0.5.2->langchain-openai) (2023.12.25)\n",
      "Requirement already satisfied: httpcore==1.* in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from httpx<1,>=0.23.0->anthropic<1,>=0.17.0->langchain-anthropic) (1.0.4)\n",
      "Requirement already satisfied: h11<0.15,>=0.13 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from httpcore==1.*->httpx<1,>=0.23.0->anthropic<1,>=0.17.0->langchain-anthropic) (0.14.0)\n",
      "Requirement already satisfied: huggingface_hub<1.0,>=0.16.4 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from tokenizers>=0.13.0->anthropic<1,>=0.17.0->langchain-anthropic) (0.21.4)\n",
      "Requirement already satisfied: mypy-extensions>=0.3.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from typing-inspect<1,>=0.4.0->dataclasses-json<0.7,>=0.5.7->langchain) (1.0.0)\n",
      "Requirement already satisfied: filelock in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from huggingface_hub<1.0,>=0.16.4->tokenizers>=0.13.0->anthropic<1,>=0.17.0->langchain-anthropic) (3.13.1)\n",
      "Requirement already satisfied: fsspec>=2023.5.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from huggingface_hub<1.0,>=0.16.4->tokenizers>=0.13.0->anthropic<1,>=0.17.0->langchain-anthropic) (2024.3.0)\n"
     ]
    }
   ],
   "source": [
    "!pip install langchain-openai langchain langchain-anthropic scikit-learn"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 133,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "with open(\"../message.txt\", \"r\") as file:\n",
    "    eval_messages = json.load(file)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 139,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "import langchain\n",
    "\n",
    "from typing import Optional\n",
    "\n",
    "from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder\n",
    "from langchain_core.pydantic_v1 import BaseModel, Field\n",
    "from langchain_openai import ChatOpenAI\n",
    "from langchain_anthropic import ChatAnthropic\n",
    "\n",
    "\n",
    "from typing import Optional\n",
    "\n",
    "from langchain_core.pydantic_v1 import BaseModel, Field\n",
    "import uuid\n",
    "from typing import Dict, List, TypedDict\n",
    "\n",
    "from langchain_core.messages import (\n",
    "    AIMessage,\n",
    "    BaseMessage,\n",
    "    HumanMessage,\n",
    "    SystemMessage,\n",
    "    ToolMessage,\n",
    ")\n",
    "from langchain_core.pydantic_v1 import BaseModel, Field\n",
    "\n",
    "\n",
    "class RealEstateParameters(BaseModel):\n",
    "    rent: Optional[int] = Field(..., description=\"The monthly rent (Nájem) in CZK. If not specified, return null.\")\n",
    "    deposit: Optional[float] = Field(..., description=\"The deposit (Kauce) in CZK. If not specified, return null.\")\n",
    "    services: Optional[int] = Field(..., description=\"The monthly services (Služby) in CZK. If not specified, return null.\")\n",
    "    energy_included: Optional[bool] = Field(..., description=\"Whether the energy (Energie) is included in the rent. If not specified, return null.\")\n",
    "    agency_fee: Optional[bool] = Field(..., description=\"Whether the real estate agent fee (Poplatek Realitní kanceláři) must be paid. If not specified, return null.\")\n",
    "\n",
    "\n",
    "examples = [\n",
    "    (\n",
    "        '+ 750 Kč poplatky na osobu, el. a plyn se převádí na nájemce, kauce a provize',\n",
    "        RealEstateParameters(rent=38000, deposit=38000, services=750, energy_included=False, agency_fee=True)\n",
    "    ),\n",
    "    (\n",
    "        '+ 3 800 Kč poplatky pro dvě osoby, elektřina se převádí na nájemce, kauce 34 000 Kč, provize',\n",
    "        RealEstateParameters(rent=16000, deposit=34000, services=3800, energy_included=False, agency_fee=True)\n",
    "    ),\n",
    "    (\n",
    "        '+popl. 4000, Cena za všechny služby a energie',\n",
    "        RealEstateParameters(rent=15000, deposit=None, services=4000, energy_included=True, agency_fee=False)\n",
    "    )\n",
    "]\n",
    "prompt = ChatPromptTemplate.from_messages(\n",
    "    [\n",
    "        (\n",
    "            \"system\",\n",
    "            \"You are prefessional real estate agent.\"\n",
    "            \"You will be given a real estate ad and you will need to extract the following information: \"\n",
    "            \"Only extract relevant information from the text. \"\n",
    "            \"If you do not know the value of an attribute asked to extract, \"\n",
    "            \"return null for the attribute's value.\"\n",
    "        ),\n",
    "        MessagesPlaceholder(\"examples\"),\n",
    "        (\"human\", \"{text}\"),\n",
    "    ]\n",
    ")\n",
    "\n",
    "\n",
    "\n",
    "class Example(TypedDict):\n",
    "    \"\"\"A representation of an example consisting of text input and expected tool calls.\n",
    "\n",
    "    For extraction, the tool calls are represented as instances of pydantic model.\n",
    "    \"\"\"\n",
    "\n",
    "    input: str  # This is the example text\n",
    "    tool_calls: List[BaseModel]  # Instances of pydantic model that should be extracted\n",
    "\n",
    "\n",
    "def tool_example_to_messages(example: Example) -> List[BaseMessage]:\n",
    "    \"\"\"Convert an example into a list of messages that can be fed into an LLM.\n",
    "\n",
    "    This code is an adapter that converts our example to a list of messages\n",
    "    that can be fed into a chat model.\n",
    "\n",
    "    The list of messages per example corresponds to:\n",
    "\n",
    "    1) HumanMessage: contains the content from which content should be extracted.\n",
    "    2) AIMessage: contains the extracted information from the model\n",
    "    3) ToolMessage: contains confirmation to the model that the model requested a tool correctly.\n",
    "\n",
    "    The ToolMessage is required because some of the chat models are hyper-optimized for agents\n",
    "    rather than for an extraction use case.\n",
    "    \"\"\"\n",
    "    messages: List[BaseMessage] = [HumanMessage(content=example[\"input\"])]\n",
    "    openai_tool_calls = []\n",
    "    for tool_call in example[\"tool_calls\"]:\n",
    "        openai_tool_calls.append(\n",
    "            {\n",
    "                \"id\": str(uuid.uuid4()),\n",
    "                \"type\": \"function\",\n",
    "                \"function\": {\n",
    "                    # The name of the function right now corresponds\n",
    "                    # to the name of the pydantic model\n",
    "                    # This is implicit in the API right now,\n",
    "                    # and will be improved over time.\n",
    "                    \"name\": tool_call.__class__.__name__,\n",
    "                    \"arguments\": tool_call.json(),\n",
    "                },\n",
    "            }\n",
    "        )\n",
    "    messages.append(\n",
    "        AIMessage(content=\"\", additional_kwargs={\"tool_calls\": openai_tool_calls})\n",
    "    )\n",
    "    tool_outputs = example.get(\"tool_outputs\") or [\n",
    "        \"You have correctly called this tool.\"\n",
    "    ] * len(openai_tool_calls)\n",
    "    for output, tool_call in zip(tool_outputs, openai_tool_calls):\n",
    "        messages.append(ToolMessage(content=output, tool_call_id=tool_call[\"id\"]))\n",
    "    return messages\n",
    "\n",
    "messages = []\n",
    "\n",
    "for text, tool_call in examples:\n",
    "    messages.extend(\n",
    "        tool_example_to_messages({\"input\": text, \"tool_calls\": [tool_call]})\n",
    "    )\n",
    "\n",
    "\n",
    "llm = ChatOpenAI(model=\"gpt-3.5-turbo\", temperature=0, api_key=\"YOUR_API_KEY_HERE\")\n",
    "\n",
    "runnable = prompt | llm.with_structured_output(schema=RealEstateParameters)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 138,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "ParametryNemovitosti(rent=28000, deposit=None, services=6000, energy_included=False, agency_fee=False)"
      ]
     },
     "execution_count": 138,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "runnable.invoke({\"text\": eval_messages[0], \"examples\": messages})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 141,
   "metadata": {},
   "outputs": [],
   "source": [
    "def extract_kauce(kauce:str, rent: int) -> Optional[float]:\n",
    "    \"\"\"Extract the deposit (Kauce) from the given text.\n",
    "\n",
    "    The deposit is expected to be a number, but it can also be a string\n",
    "    that represents a number (e.g. \"1.5\" for 1.5x rent).\n",
    "\n",
    "    If the deposit is not found, return None.\n",
    "    \"\"\"\n",
    "\n",
    "    if kauce is not None:\n",
    "        if isinstance(kauce, str):\n",
    "            if kauce.endswith(\"rent\"):\n",
    "                try:\n",
    "                    multiplier = float(kauce.replace(\"*rent\", \"\"))\n",
    "                    return rent * multiplier\n",
    "                except ValueError:\n",
    "                    return None\n",
    "            else:\n",
    "                try:\n",
    "                    return float(kauce)\n",
    "                except ValueError:\n",
    "                    return None\n",
    "        else:\n",
    "            return None\n",
    "    else:\n",
    "        return None\n",
    "\n",
    "\n",
    "eval_offers = [\n",
    "    RealEstateParameters(\n",
    "        rent=sample[\"rent\"],\n",
    "        deposit=extract_kauce(sample[\"deposit\"], sample[\"rent\"]),\n",
    "        services=sample[\"services\"],\n",
    "        energy_included=sample[\"energy\"],\n",
    "        agency_fee=sample[\"rk\"],\n",
    "    )\n",
    "    for sample in eval_messages\n",
    "]\n",
    "\n",
    "eval_ads = [\n",
    "    sample[\"add\"]\n",
    "    for sample in eval_messages\n",
    "]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 142,
   "metadata": {},
   "outputs": [],
   "source": [
    "predicted_offers = [runnable.invoke({\"text\": message, \"examples\": messages}) for message in eval_messages]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.metrics import precision_recall_fscore_support\n",
    "\n",
    "def evaluate(y_pred, y_true):\n",
    "    y_true = [{k: -1 if v is None else v for k, v in sample.items()} for sample in y_true]\n",
    "    y_pred = [{k: -1 if v is None else v for k, v in sample.items()} for sample in y_pred]\n",
    "\n",
    "    # Calculate precision, recall, and f1-score for each label\n",
    "    precision_list = []\n",
    "    recall_list = []\n",
    "    f1_list = []\n",
    "    \n",
    "    precision_list = []\n",
    "    recall_list = []\n",
    "    f1_list = []\n",
    "\n",
    "    for label in y_true[0].keys():\n",
    "        true_label_values = [sample[label] for sample in y_true]\n",
    "        pred_label_values = [sample[label] for sample in y_pred]\n",
    "        precision, recall, f1, _ = precision_recall_fscore_support(true_label_values, pred_label_values, average='weighted')\n",
    "        precision_list.append(precision)\n",
    "        recall_list.append(recall)\n",
    "        f1_list.append(f1)\n",
    "\n",
    "    avg_precision = sum(precision_list) / len(precision_list)\n",
    "    avg_recall = sum(recall_list) / len(recall_list)\n",
    "    avg_f1 = sum(f1_list) / len(f1_list)\n",
    "    \n",
    "    # Calculate and return the average precision, recall, and f1-score\n",
    "    avg_precision = sum(precision_list) / len(precision_list)\n",
    "    avg_recall = sum(recall_list) / len(recall_list)\n",
    "    avg_f1 = sum(f1_list) / len(f1_list)\n",
    "    \n",
    "    return {\"average_precision\": avg_precision, \"average_recall\": avg_recall, \"average_f1\": avg_f1}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 143,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[RealEstateParameters(rent=28000, deposit=None, services=6000, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=25000, deposit=None, services=4500, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=38000, deposit=None, services=750, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=16000, deposit=34000.0, services=3800, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=15500, deposit=31000.0, services=950, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=17900, deposit=None, services=3033, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=5500, deposit=None, services=1800, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=37500, deposit=None, services=8000, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=36000, deposit=None, services=8323, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=11500, deposit=None, services=4300, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=19900, deposit=None, services=2900, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=27000, deposit=None, services=4000, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=24000, deposit=24000.0, services=5400, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=28000, deposit=56000.0, services=1250, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=28000, deposit=56000.0, services=7000, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=26000, deposit=26000.0, services=5400, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=16000, deposit=16000.0, services=4000, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=34900, deposit=69800.0, services=6750, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=27000, deposit=54000.0, services=7500, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=25000, deposit=None, services=5400, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=28000, deposit=56000.0, services=1250, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=58000, deposit=58000.0, services=7000, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=26000, deposit=52000.0, services=7500, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=40000, deposit=None, services=5400, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=50000, deposit=None, services=12500, energy_included=True, agency_fee=False),\n",
       " RealEstateParameters(rent=24800, deposit=None, services=800, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=15000, deposit=None, services=4000, energy_included=True, agency_fee=False),\n",
       " RealEstateParameters(rent=15000, deposit=None, services=3000, energy_included=True, agency_fee=False),\n",
       " RealEstateParameters(rent=28000, deposit=None, services=6000, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=25000, deposit=None, services=4500, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=38000, deposit=None, services=750, energy_included=False, agency_fee=True)]"
      ]
     },
     "execution_count": 143,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "predicted_offers"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 144,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[RealEstateParameters(rent=28000, deposit=None, services=6000, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=25000, deposit=None, services=4500, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=38000, deposit=None, services=750, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=16000, deposit=None, services=3800, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=15500, deposit=31000.0, services=950, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=17900, deposit=None, services=3033, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=5500, deposit=None, services=1800, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=37500, deposit=None, services=8000, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=36000, deposit=None, services=8323, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=11500, deposit=None, services=4300, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=19900, deposit=None, services=2900, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=27000, deposit=None, services=4000, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=24000, deposit=None, services=5400, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=28000, deposit=56000.0, services=1250, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=28000, deposit=56000.0, services=7000, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=26000, deposit=None, services=5400, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=16000, deposit=None, services=4000, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=34900, deposit=69800.0, services=6750, energy_included=False, agency_fee=True),\n",
       " RealEstateParameters(rent=27000, deposit=54000.0, services=7500, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=25000, deposit=None, services=5400, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=28000, deposit=56000.0, services=1250, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=58000, deposit=None, services=7000, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=26000, deposit=52000.0, services=7500, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=40000, deposit=None, services=5400, energy_included=True, agency_fee=True),\n",
       " RealEstateParameters(rent=50000, deposit=None, services=12500, energy_included=True, agency_fee=False),\n",
       " RealEstateParameters(rent=24800, deposit=None, services=800, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=15000, deposit=None, services=4000, energy_included=True, agency_fee=False),\n",
       " RealEstateParameters(rent=15000, deposit=None, services=3000, energy_included=True, agency_fee=False),\n",
       " RealEstateParameters(rent=28000, deposit=None, services=6000, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=25000, deposit=None, services=4500, energy_included=False, agency_fee=False),\n",
       " RealEstateParameters(rent=38000, deposit=None, services=750, energy_included=False, agency_fee=True)]"
      ]
     },
     "execution_count": 144,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "eval_offers"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 145,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages/sklearn/metrics/_classification.py:1509: UndefinedMetricWarning: Recall is ill-defined and being set to 0.0 in labels with no true samples. Use `zero_division` parameter to control this behavior.\n",
      "  _warn_prf(average, modifier, f\"{metric.capitalize()} is\", len(result))\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "{'average_precision': 1.0,\n",
       " 'average_recall': 0.967741935483871,\n",
       " 'average_f1': 0.9819954988747186}"
      ]
     },
     "execution_count": 145,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "evaluate([\n",
    "    x.dict() for x in predicted_offers\n",
    "], [\n",
    "    x.dict() for x in eval_offers\n",
    "])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting scikit-learn\n",
      "  Downloading scikit_learn-1.4.1.post1-cp312-cp312-macosx_12_0_arm64.whl.metadata (11 kB)\n",
      "Requirement already satisfied: numpy<2.0,>=1.19.5 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from scikit-learn) (1.26.4)\n",
      "Collecting scipy>=1.6.0 (from scikit-learn)\n",
      "  Downloading scipy-1.12.0-cp312-cp312-macosx_12_0_arm64.whl.metadata (217 kB)\n",
      "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m217.9/217.9 kB\u001b[0m \u001b[31m2.1 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0ma \u001b[36m0:00:01\u001b[0m\n",
      "\u001b[?25hCollecting joblib>=1.2.0 (from scikit-learn)\n",
      "  Using cached joblib-1.3.2-py3-none-any.whl.metadata (5.4 kB)\n",
      "Collecting threadpoolctl>=2.0.0 (from scikit-learn)\n",
      "  Downloading threadpoolctl-3.3.0-py3-none-any.whl.metadata (13 kB)\n",
      "Downloading scikit_learn-1.4.1.post1-cp312-cp312-macosx_12_0_arm64.whl (10.5 MB)\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m10.5/10.5 MB\u001b[0m \u001b[31m2.4 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m00:01\u001b[0m00:01\u001b[0mm\n",
      "\u001b[?25hUsing cached joblib-1.3.2-py3-none-any.whl (302 kB)\n",
      "Downloading scipy-1.12.0-cp312-cp312-macosx_12_0_arm64.whl (31.4 MB)\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m31.4/31.4 MB\u001b[0m \u001b[31m2.0 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m00:01\u001b[0m00:01\u001b[0m\n",
      "\u001b[?25hDownloading threadpoolctl-3.3.0-py3-none-any.whl (17 kB)\n",
      "Installing collected packages: threadpoolctl, scipy, joblib, scikit-learn\n",
      "Successfully installed joblib-1.3.2 scikit-learn-1.4.1.post1 scipy-1.12.0 threadpoolctl-3.3.0\n"
     ]
    }
   ],
   "source": [
    "!pip install "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting pandas\n",
      "  Using cached pandas-2.2.1-cp312-cp312-macosx_11_0_arm64.whl.metadata (19 kB)\n",
      "Requirement already satisfied: numpy<2,>=1.26.0 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from pandas) (1.26.4)\n",
      "Requirement already satisfied: python-dateutil>=2.8.2 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from pandas) (2.9.0.post0)\n",
      "Collecting pytz>=2020.1 (from pandas)\n",
      "  Using cached pytz-2024.1-py2.py3-none-any.whl.metadata (22 kB)\n",
      "Collecting tzdata>=2022.7 (from pandas)\n",
      "  Using cached tzdata-2024.1-py2.py3-none-any.whl.metadata (1.4 kB)\n",
      "Requirement already satisfied: six>=1.5 in /Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages (from python-dateutil>=2.8.2->pandas) (1.16.0)\n",
      "Using cached pandas-2.2.1-cp312-cp312-macosx_11_0_arm64.whl (11.3 MB)\n",
      "Using cached pytz-2024.1-py2.py3-none-any.whl (505 kB)\n",
      "Using cached tzdata-2024.1-py2.py3-none-any.whl (345 kB)\n",
      "Installing collected packages: pytz, tzdata, pandas\n",
      "Successfully installed pandas-2.2.1 pytz-2024.1 tzdata-2024.1\n"
     ]
    }
   ],
   "source": [
    "!pip install pandas"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages/sklearn/metrics/_classification.py:1509: UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.\n",
      "  _warn_prf(average, modifier, f\"{metric.capitalize()} is\", len(result))\n",
      "/Users/hynky/.pyenv/versions/3.12.2/envs/experiments/lib/python3.12/site-packages/sklearn/metrics/_classification.py:1509: UndefinedMetricWarning: Recall is ill-defined and being set to 0.0 in labels with no true samples. Use `zero_division` parameter to control this behavior.\n",
      "  _warn_prf(average, modifier, f\"{metric.capitalize()} is\", len(result))\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "(0.0, 0.0, 0.0, None)"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "from sklearn.metrics import precision_recall_fscore_support\n",
    "import pandas as pd\n",
    "\n",
    "precision_recall_fscore_support([1,2], [0,0], average='weighted')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[('+ 750 Kč poplatky na osobu, el. a plyn se převádí na nájemce, kauce a provize',\n",
       "  RealEstateAd(nájem=38000, kauce=1.0, služby=750, včetně_energií=False, poplatek_realitní_kanceláři=True)),\n",
       " ('+ 3 800 Kč poplatky pro dvě osoby, elektřina se převádí na nájemce, kauce 34 000 Kč, provize',\n",
       "  RealEstateAd(nájem=16000, kauce=2.125, služby=3800, včetně_energií=False, poplatek_realitní_kanceláři=True)),\n",
       " ('+popl. 4000, Cena za všechny služby a energie',\n",
       "  RealEstateAd(nájem=15000, kauce=None, služby=4000, včetně_energií=True, poplatek_realitní_kanceláři=False))]"
      ]
     },
     "execution_count": 25,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "examples"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 70,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "34900"
      ]
     },
     "execution_count": 70,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "examples[2][\"rent\"]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Input: {\"n\\u00e1jem\": 28000, \"kauce\": null, \"slu\\u017eby\": 6000, \"v\\u010detn\\u011b_energi\\u00ed\": false, \"poplatek_realitn\\u00ed_kancel\\u00e1\\u0159i\": false}\n",
      "Output: Záloha na společné služby, vytápění, vodu a údržbu garáže: 6.000 Kč/měs. Elektřina se platí zvlášť.\n",
      "\n",
      "\n",
      "Input: {\"n\\u00e1jem\": 25000, \"kauce\": null, \"slu\\u017eby\": 4500, \"v\\u010detn\\u011b_energi\\u00ed\": false, \"poplatek_realitn\\u00ed_kancel\\u00e1\\u0159i\": false}\n",
      "Output: Zálohy na poplatky za společné domovní služby, vodu a vytápění 4.500 Kč/měs. pro 2 osoby. Elektřina se hradí zvlášť.\n",
      "\n",
      "\n",
      "Input: {\"n\\u00e1jem\": 34900, \"kauce\": \"2*rent\", \"slu\\u017eby\": 6750, \"v\\u010detn\\u011b_energi\\u00ed\": false, \"poplatek_realitn\\u00ed_kancel\\u00e1\\u0159i\": true}\n",
      "Output: Poplatky fix 900 Kč/os./měs. + zál. voda 350 Kč/os./měs. + zál. plyn 5 500 Kč/byt/měs. + převod elektřiny. Kauce 2 nájmy. RK provize 1 nájem, neplatít\n",
      "\n",
      "('{\"n\\\\u00e1jem\": 28000, \"kauce\": 24500, \"slu\\\\u017eby\": 8500, \"v\\\\u010detn\\\\u011b_energi\\\\u00ed\": true, \"poplatek_realitn\\\\u00ed_kancel\\\\u00e1\\\\u0159i\": false}', 'Nájem: 28.000 Kč/měs., kauce: 24.500 Kč. Záloha na služby včetně energií: 8.500 Kč/měs. Poplatek realitní kanceláři neplatíte.')\n"
     ]
    }
   ],
   "source": [
    "from langchain.prompts import (\n",
    "    ChatPromptTemplate,\n",
    "    FewShotChatMessagePromptTemplate,\n",
    ")\n",
    "import json\n",
    "\n",
    "def create_example():\n",
    "    # This is a prompt template used to format each individual example.\n",
    "    import random\n",
    "    examples = random.sample(eval_messages, 3)\n",
    "\n",
    "    def example_to_message(example):\n",
    "        return (\n",
    "f\"\"\"\\\n",
    "Input: {json.dumps({ \"nájem\": example[\"nájem\"], \"kauce\": example[\"kauce\"], \"služby\": example[\"služby\"], \"včetně_energií\": example[\"včetně_energií\"], \"poplatek_realitní_kanceláři\": example[\"poplatek_realitní_kanceláři\"] })}\n",
    "Output: {example[\"ad\"]}\n",
    "\"\"\"\n",
    ")\n",
    "    example_messages = \"\\n\\n\".join(example_to_message(example) for example in examples)\n",
    "    print(example_messages)\n",
    "    final_prompt = ChatPromptTemplate.from_messages(\n",
    "        [\n",
    "            (\"system\", \n",
    "\"\"\"\\\n",
    "You are an profesional real estate agent. \n",
    "\n",
    "# Task\n",
    "You will be given a real estate parameters and your task is to create a real estate ad in Czech.\n",
    "\n",
    "# Input Format\n",
    "You will be given a JSON object with the following parameters:\n",
    "- nájem: The monthly rent (Nájem) in CZK.\n",
    "- kauce: The deposit (Kauce) in terms of multiple of rent.\n",
    "- služby: The monthly services (Služby) in CZK.\n",
    "- včetně_energií: Whether the energy (Energie) is included in the rent.\n",
    "- poplatek_realitní_kanceláři: Whether the real estate agent fee (Poplatek Realitní kanceláři) must be paid.\n",
    "\n",
    "# Output Format\n",
    "You must output the ad in Czech. The ad must be in the the similar format as examples.\n",
    "\n",
    "# Examples\n",
    "{examples}\n",
    "\n",
    "\n",
    "You must exactly follow the parameters and include all of them that are filled. You must output the ad in Czech. The ad must be in the same format as Examples.\\\n",
    "\"\"\"),\n",
    "            (\"human\", \"{input}\"),\n",
    "        ]\n",
    "    )\n",
    "    from langchain_community.chat_models import ChatOpenAI, ChatAnthropic\n",
    "\n",
    "    llm = ChatOpenAI(model=\"gpt-4-1106-preview\", temperature=0.7, api_key=\"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\")\n",
    "    chain = final_prompt | llm\n",
    "\n",
    "\n",
    "    def generate_random_real_estate_parameters():\n",
    "        rent_options = list(range(15000, 35001, 500))\n",
    "        deposit_options = [None, \"1*rent\", \"2*rent\", \"3*rent\"] + list(range(15000, 35001, 500))\n",
    "        services_options = list(range(500, 15001, 250))\n",
    "        energy_options = [True, False]\n",
    "        rk_options = [True, False]\n",
    "        \n",
    "        rent = random.choice(rent_options)\n",
    "        deposit = random.choice(deposit_options)\n",
    "        services = random.choice(services_options)\n",
    "        energy = random.choice(energy_options)\n",
    "        rk = random.choice(rk_options)\n",
    "        \n",
    "        real_estate_parameters = {\n",
    "            \"nájem\": rent,\n",
    "            \"kauce\": deposit,\n",
    "            \"služby\": services,\n",
    "            \"včetně_energií\": energy,\n",
    "            \"poplatek_realitní_kanceláři\": rk\n",
    "        }\n",
    "        \n",
    "        return json.dumps(real_estate_parameters)\n",
    "    query = generate_random_real_estate_parameters()\n",
    "    return query, chain.invoke({\"input\": query, \"examples\": example_messages}).content\n",
    "\n",
    "\n",
    "generated_pairs = []\n",
    "for i in range(1):\n",
    "    generated_pairs.append(create_example())\n",
    "    print(generated_pairs[-1])\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "('{\"n\\\\u00e1jem\": 28000, \"kauce\": 24500, \"slu\\\\u017eby\": 8500, \"v\\\\u010detn\\\\u011b_energi\\\\u00ed\": true, \"poplatek_realitn\\\\u00ed_kancel\\\\u00e1\\\\u0159i\": false}',\n",
       " 'Nájem: 28.000 Kč/měs., kauce: 24.500 Kč. Záloha na služby včetně energií: 8.500 Kč/měs. Poplatek realitní kanceláři neplatíte.')"
      ]
     },
     "execution_count": 43,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "generated_pairs[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{\"messages\": [{\"role\": \"user\", \"content\": \"N\\u00e1jem: 28.000 K\\u010d/m\\u011bs., kauce: 24.500 K\\u010d. Z\\u00e1loha na slu\\u017eby v\\u010detn\\u011b energi\\u00ed: 8.500 K\\u010d/m\\u011bs. Poplatek realitn\\u00ed kancel\\u00e1\\u0159i neplat\\u00edte.\"}, {\"role\": \"assistant\", \"function_call\": {\"name\": \"parametry_nemovitosti\", \"arguments\": \"{\\\"n\\\\u00e1jem\\\": 28000, \\\"kauce\\\": 24500, \\\"slu\\\\u017eby\\\": 8500, \\\"v\\\\u010detn\\\\u011b_energi\\\\u00ed\\\": true, \\\"poplatek_realitn\\\\u00ed_kancel\\\\u00e1\\\\u0159i\\\": false}\"}}], \"functions\": [{\"name\": \"parametry_nemovitosti\", \"parameters\": {\"title\": \"ParametryNemovitosti\", \"type\": \"object\", \"properties\": {\"n\\u00e1jem\": {\"title\": \"N\\u00e1jem\", \"description\": \"The monthly rent (N\\u00e1jem) in CZK. If not specified, return null.\", \"type\": \"integer\"}, \"kauce\": {\"title\": \"Kauce\", \"description\": \"The deposit (Kauce) in terms of multiple of rent. If not specified, return null.\", \"type\": \"number\"}, \"slu\\u017eby\": {\"title\": \"Slu\\u017eby\", \"description\": \"The monthly services (Slu\\u017eby) in CZK. If not specified, return null.\", \"type\": \"integer\"}, \"v\\u010detn\\u011b_energi\\u00ed\": {\"title\": \"V\\u010detn\\u011b Energi\\u00ed\", \"description\": \"Whether the energy (Energie) is included in the rent. If not specified, return null.\", \"type\": \"boolean\"}, \"poplatek_realitn\\u00ed_kancel\\u00e1\\u0159i\": {\"title\": \"Poplatek Realitn\\u00ed Kancel\\u00e1\\u0159i\", \"description\": \"Whether the real estate agent fee (Poplatek Realitn\\u00ed kancel\\u00e1\\u0159i) must be paid. If not specified, return null.\", \"type\": \"boolean\"}}, \"required\": [\"n\\u00e1jem\", \"kauce\", \"slu\\u017eby\", \"v\\u010detn\\u011b_energi\\u00ed\", \"poplatek_realitn\\u00ed_kancel\\u00e1\\u0159i\"]}}]}\n"
     ]
    }
   ],
   "source": [
    "tunning_messages = [\n",
    "    {\"messages\": [\n",
    "        {\n",
    "            \"role\": \"user\",\n",
    "            \"content\": m[1]\n",
    "        },\n",
    "        {\n",
    "            \"role\": \"assistant\",\n",
    "            \"function_call\": {\n",
    "                \"name\": \"parametry_nemovitosti\",\n",
    "                \"arguments\": json.dumps(json.loads(m[0]))\n",
    "            }\n",
    "        }\n",
    "    ],\n",
    "    \"functions\": [\n",
    "        {\n",
    "        \"name\": \"parametry_nemovitosti\",\n",
    "        \"parameters\": RealEstateParameters.schema()\n",
    "        }\n",
    "    ]\n",
    "\n",
    "}\n",
    "for m in generated_pairs]\n",
    "\n",
    "print(json.dumps(tunning_messages[0]))\n",
    "\n",
    "with open('generated_lines.jsonl', 'w') as file:\n",
    "    for pair in tunning_messages:\n",
    "        file.write(json.dumps(pair) + '\\n')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "AIMessage(content='Pronájem bytu za 24 500 Kč/měsíc včetně služeb ve výši 14 500 Kč/měsíc. Kauce ve výši 21 000 Kč. Pro více informací nás kontaktujte.', response_metadata={'finish_reason': 'stop', 'logprobs': None})"
      ]
     },
     "execution_count": 23,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {},
   "outputs": [],
   "source": [
    "runnable = prompt | llm.with_structured_output(schema=RealEstateParameters)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "nájem=None kauce=2.0 služby=8000 včetně_energií=True poplatek_realitní_kanceláři=True\n",
      "0.0010665\n"
     ]
    }
   ],
   "source": [
    "from langchain.callbacks import get_openai_callback\n",
    "text = \"+ 8.000,- Kč zálohy na služby a energie + kauce + provize RK\"\n",
    "\n",
    "with get_openai_callback() as cb:\n",
    "    print(runnable.invoke({\"text\": text, \"examples\":messages}))\n",
    "    print(cb.total_cost)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.00558"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cb.total_cost"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'sklearn'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[11], line 1\u001b[0m\n\u001b[0;32m----> 1\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01msklearn\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mmetrics\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m precision_recall_fscore_support\n\u001b[1;32m      3\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21mevaluate\u001b[39m(data_list):\n\u001b[1;32m      4\u001b[0m     y_true \u001b[38;5;241m=\u001b[39m []\n",
      "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'sklearn'"
     ]
    }
   ],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
