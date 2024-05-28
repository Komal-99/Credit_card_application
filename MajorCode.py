import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# set <your-endpoint> and <your-key> variables with the values from the Azure portal
endpoint = "https://majorproject.cognitiveservices.azure.com/"
key = "5d3045b9e9b14ab782c899197278aba8"
def format_bounding_region(bounding_regions):
    if not bounding_regions:
        return "N/A"
    return ", ".join("Page #{}: {}".format(region.page_number, format_polygon(region.polygon)) for region in bounding_regions)

def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])


def analyze_general_documents(image_path):
    # Initialize a list to store extracted text
    
    # global handwritten_text, key_value_text, line_text, selection_mark_text, table_text,row_count,table_no,col_count

    # sample document
    # docUrl = r"C:\Users\thepa\OneDrive\Desktop\MajorProj\card_data\card_data\images (5).jpeg"
    docUrl = image_path
    # create your DocumentAnalysisClient instance and AzureKeyCredential variable
    # with open(docUrl, "rb") as f:
    #     poller = document_analysis_client.begin_analyze_document(
    #         "prebuilt-document", document=f,features=[AnalysisFeature.LANGUAGES]
    #     )
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    with open(docUrl, "rb") as f:
        poller = document_analysis_client.begin_analyze_document("prebuilt-document", document=f)
    result = poller.result()

    # poller = document_analysis_client.begin_analyze_document(
    #        "prebuilt-document", document=docUrl)
    # result = poller.result()
    # print("----Languages detected in the document----")
    # # print(result.languages)
    # print(f"Detected {len(result.languages)} languages:")
    # for lang_idx, lang in enumerate(result.languages):
    #     print(f"- Language #{lang_idx}: locale '{lang.locale}'")
    #     print(f"  Confidence: {lang.confidence}")
    #     print(f"  Text: '{','.join([result.content[span.offset : span.offset + span.length] for span in lang.spans])}'")
    handwritten_text = ""
    for style in result.styles:
        if style.is_handwritten:
            handwritten_text += " ".join([result.content[span.offset:span.offset + span.length] for span in style.spans])
    # extracted_text_list.append(handwritten_text)
    extracted_text_list = []
   
    for kv_pair in result.key_value_pairs:
        key_value_dict={}
        if kv_pair.key:
            key_value_dict["Key"]=kv_pair.key.content
            # key_value_text += "Key '{}'\n".format(kv_pair.key.content)
        if kv_pair.value:
            key_value_dict["Value"]=kv_pair.value.content
            # handwritten_text+=key_value_dict
            handwritten_text += format(kv_pair.value.content)
        # extracted_text_list.append(key_value_dict)

    line_text = ""
    for line_idx, line in enumerate(result.pages[0].lines):
        handwritten_text += "{}\n".format(line.content)
    # extracted_text_list.append(line_text)

    selection_mark_text = ""
    for page in result.pages:
        for selection_mark in page.selection_marks:
            selection_mark_text += "...Selection mark is '{}' within bounding box '{}' and has a confidence of {}\n".format(
                selection_mark.state,
                format_polygon(selection_mark.polygon),
                selection_mark.confidence,
            )
    # extracted_text_list.append(selection_mark_text)

    table_text = ""
    # row_count
    for table_idx, table in enumerate(result.tables):
        table_text += "Table # {} has {} rows and {} columns\n".format(
            table_idx, table.row_count, table.column_count
        )
        table_no=table_idx
        # row_count=table.row_count
        # col_count=table.column_count
        # table_no=table_idx
        for cell in table.cells:
            if cell.content.strip():
                handwritten_text += "{}{}{} Content: '{}' \n".format(table_idx,
                    cell.row_index, cell.column_index, cell.content
                )
    return docUrl, handwritten_text



# analyze_general_documents()
# def process_images_in_folder(folder_path):
#     # List all files in the specified folder
#     image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

#     # Process each image in the folder
#     for image_file in image_files:
#         image_path = os.path.join(folder_path, image_file)
#         print(f"\nProcessing image: {image_file}")
#         analyze_general_documents(image_path)
import re
# if __name__ == "__main__":
    # d,text= analyze_general_documents()
    # # process_images_in_folder(r"C:\Users\thepa\OneDrive\Desktop\MajorProj\card_data\card_data")
    # print(text)
    # print("----------------------------------")

    # account_number_pattern = re.compile(r'\b(\d{4}\s\d{4}\s\d{4}\s\d{4})\b')
    # account_numbers = account_number_pattern.findall(text)
    # print(account_numbers)
    # expiry_date_pattern = re.compile(r'\b(\d{2}/\d{2})\b')
    # expiry_dates = expiry_date_pattern.findall(text)
    # print(expiry_dates)
    # card_type_pattern = re.compile(r'\b(?:credit |debit|visa|mastercard|Credit Card|debit Card|master card)\b', flags=re.IGNORECASE)
    # card_types = card_type_pattern.findall(text)
    # print(card_types)
    # # Card Holder Name:
    # card_holder_name_pattern = re.compile(r'\b[A-Z\s]+\b')
    # card_holder_names = card_holder_name_pattern.findall(text)
    # # Filter out entries with line breaks
    # card_holder_name_pattern = re.compile(r'\b(?:\d{2}/\d{2}\s+)([A-Z]+\.?\s+[A-Z]+)\b')
    # card_holder_names = card_holder_name_pattern.findall(text)
    # print(card_holder_names)

def extract_feilds(image_path):
    d,text= analyze_general_documents(image_path)
    # process_images_in_folder(r"C:\Users\thepa\OneDrive\Desktop\MajorProj\card_data\card_data")
    print("********************************")
    print(text)
    print("----------------------------------")

    account_number_pattern = re.compile(r'\b(\d{4}\s\d{4}\s\d{4}\s\d{4})\b')
    account_numbers = account_number_pattern.findall(text)
    print(account_numbers)
    expiry_date_pattern = re.compile(r'\b(\d{2}/\d{2})\b')
    expiry_dates = expiry_date_pattern.findall(text)
    print(expiry_dates)
    card_type_keywords = ['credit', 'debit', 'visa', 'mastercard', 'credit card', 'debit card', 'master card']

# Pattern to capture alphanumeric sequences
    alphanumeric_pattern = re.compile(r'\b[\w/]+\b')

    # Find all alphanumeric sequences in the text
    alphanumeric_sequences = alphanumeric_pattern.findall(text)

    # Find card type based on keywords
    card_types = [keyword for keyword in card_type_keywords if any(keyword.lower() in sequence.lower() for sequence in alphanumeric_sequences)]

    # Print the results
    print(card_types)
    # card_type_pattern = re.compile(r'\b(?:credit|debit|visa|mastercard|Credit Card|debit Card|master card)\b', flags=re.IGNORECASE)
    # card_types = card_type_pattern.findall(text)
    # print(card_types)
    # Card Holder Name:
    # card_holder_name_pattern = re.compile(r'\b[A-Z\s]+\b')
    # card_holder_names = card_holder_name_pattern.findall(text)
    # Filter out entries with line breaks
    card_holder_name_pattern = re.compile(r'\b(?:\d{2}/\d{2}\s+)([A-Z]+\.?\s+[A-Z]+)\b|\b([A-Z]+\.?\s+[A-Z]+)\b')
    card_holder_names = card_holder_name_pattern.findall(text)

    # Flatten the nested lists
    card_holder_names = [name for names in card_holder_names for name in names if name]

    # Print the results
    print(card_holder_names)
    # card_holder_name_pattern = re.compile(r'\b(?:\d{2}/\d{2}\s+)([A-Z]+\.?\s+[A-Z]+)\b')
    # card_holder_names = card_holder_name_pattern.findall(text)
    # print(card_holder_names)
    return account_numbers[-1],expiry_dates[-1],card_types[-1],card_holder_names[-1]

# extract_feilds()
# print(hh)