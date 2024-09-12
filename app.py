import pandas as pd
import streamlit as st
import zipfile
import io

# Streamlit app title
st.title('Generate your webstories:😀')

# Create two tabs: Master Template Generator and Story Generator
tab1, tab2 = st.tabs(["Master Template Generator", "Story Generator"])

# Tab 1: Master Template Generator
with tab1:
    st.header('Master Template Generator')
    
    # File upload for Excel and HTML
    uploaded_excel_master = st.file_uploader("Upload the Excel file (for replacements)", type="xlsx", key="master_excel")
    uploaded_html_master = st.file_uploader("Upload the HTML file", type="html", key="master_html")

    # Proceed if both files are uploaded
    if uploaded_excel_master and uploaded_html_master:
        # Read the Excel file into a DataFrame
        df_master = pd.read_excel(uploaded_excel_master, header=None)

        # Read the uploaded HTML file
        html_content_master = uploaded_html_master.read().decode('utf-8')

        # Perform replacement using Excel data
        for i in range(len(df_master.columns)):
            actual_value = str(df_master.iloc[0, i])  # First row contains actual values
            placeholder = str(df_master.iloc[1, i])   # Second row contains placeholders
            html_content_master = html_content_master.replace(actual_value, placeholder)

        # Create a download button for the modified HTML
        st.download_button(label="Download Modified HTML", 
                           data=html_content_master, 
                           file_name='Listerr_master_template.html', 
                           mime='text/html')

        st.success("HTML content modified. Click the button above to download the modified file.")
    else:
        st.info("Please upload both an Excel file and an HTML file for the Master Template Generator.")

# Tab 2: Story Generator
with tab2:
    st.header('Story Generator')
    
    # File upload for Excel and HTML
    uploaded_excel_story = st.file_uploader("Upload the Excel file (for replacements)", type="xlsx", key="story_excel")
    uploaded_html_story = st.file_uploader("Upload the HTML file", type="html", key="story_html")

    # Proceed if both files are uploaded
    if uploaded_excel_story and uploaded_html_story:
        # Read the Excel file into a DataFrame
        df_story = pd.read_excel(uploaded_excel_story, header=None)

        # Read the uploaded HTML file
        html_content_template_story = uploaded_html_story.read().decode('utf-8')

        # First row (index 0) contains placeholders like {{storytitle}}, {{coverinfo1}}, etc.
        placeholders_story = df_story.iloc[0, :].tolist()

        # Prepare an in-memory zip file to store all modified HTML files
        zip_buffer_story = io.BytesIO()
        with zipfile.ZipFile(zip_buffer_story, "w", zipfile.ZIP_DEFLATED) as zf:
            # Loop through each row from index 1 onward to perform replacements
            for row_index in range(1, len(df_story)):
                actual_values_story = df_story.iloc[row_index, :].tolist()

                # Copy the original HTML template content
                html_content_story = html_content_template_story

                # Perform batch replacement for each placeholder in the row
                for placeholder, actual_value in zip(placeholders_story, actual_values_story):
                    html_content_story = html_content_story.replace(placeholder, str(actual_value))

                # Use the first column value of each row as the filename
                output_filename_story = f"{actual_values_story[0]}.html"

                # Add the modified HTML content to the in-memory zip
                zf.writestr(output_filename_story, html_content_story)

        # Seek to the beginning of the buffer to prepare for download
        zip_buffer_story.seek(0)

        # Create a download button for the zip file containing all modified HTML files
        st.download_button(
            label="Download All Modified HTML Files (as ZIP)",
            data=zip_buffer_story,
            file_name='modified_html_templates.zip',
            mime='application/zip'
        )

        st.success("HTML content modified for all rows. Click the button above to download the modified files.")
    else:
        st.info("Please upload both an Excel file and an HTML file for the Story Generator.")