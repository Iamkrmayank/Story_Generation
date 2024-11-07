import pandas as pd
import streamlit as st
import zipfile
import io
import json  # Import json module for JSON encoding
import streamlit.components.v1 as components

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

        # Get the last row for placeholders
        placeholder_row = df_master.iloc[-1]

        # Prepare data for JavaScript to download each HTML page automatically
        html_data = []
        for row_index in range(len(df_master) - 1):
            row_data = df_master.iloc[row_index]
            html_content_modified = html_content_master

            for col_index in range(len(df_master.columns)):
                actual_value = str(row_data[col_index])  # Actual value from the current row
                placeholder = str(placeholder_row[col_index])  # Placeholder from the last row
                html_content_modified = html_content_modified.replace(placeholder, actual_value)

            file_name = f"{str(row_data[0])}_template.html"
            html_data.append({"content": html_content_modified, "filename": file_name})

        # JavaScript to trigger download for each HTML file
        download_js = """
        <script>
        const htmlData = JSON.parse(document.getElementById("file_data").textContent);
        htmlData.forEach(file => {
            const blob = new Blob([file.content], { type: 'text/html' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = file.filename;
            link.click();
        });
        </script>
        """

        # Inject the data and the JavaScript into the app
        components.html(f"""
            <div id="file_data" style="display: none;">{json.dumps(html_data)}</div>
            {download_js}
        """, height=0)

        st.success("HTML content modified for all rows and downloading should start automatically.")
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

        # Prepare data for JavaScript to download each HTML page automatically
        story_data = []
        for row_index in range(1, len(df_story)):
            actual_values_story = df_story.iloc[row_index, :].tolist()
            html_content_story = html_content_template_story

            for placeholder, actual_value in zip(placeholders_story, actual_values_story):
                html_content_story = html_content_story.replace(placeholder, str(actual_value))

            output_filename_story = f"{actual_values_story[0]}.html"
            story_data.append({"content": html_content_story, "filename": output_filename_story})

        # JavaScript to trigger download for each HTML file
        story_js = """
        <script>
        const storyFiles = JSON.parse(document.getElementById("story_file_data").textContent);
        storyFiles.forEach(file => {
            const blob = new Blob([file.content], { type: 'text/html' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = file.filename;
            link.click();
        });
        </script>
        """

        # Inject the data and the JavaScript into the app
        components.html(f"""
            <div id="story_file_data" style="display: none;">{json.dumps(story_data)}</div>
            {story_js}
        """, height=0)

        st.success("HTML content modified for all rows and downloading should start automatically.")
    else:
        st.info("Please upload both an Excel file and an HTML file for the Story Generator.")
