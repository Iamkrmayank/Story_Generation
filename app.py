import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Streamlit app title
st.title('Generate Your Webstories 😀')

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
        placeholder_row = df_master.iloc[-1].tolist()

        # Prepare a list of generated HTML file names and content for download
        html_files = []

        # Loop through each row except the last one (which contains placeholders)
        for row_index in range(len(df_master) - 1):
            # Get the current row data (actual values)
            row_data = df_master.iloc[row_index].tolist()

            # Make a copy of the HTML content for each row and replace placeholders
            html_content_modified = html_content_master
            for placeholder, actual_value in zip(placeholder_row, row_data):
                html_content_modified = html_content_modified.replace(str(placeholder), str(actual_value))

            # Generate the filename using the first column of the current row
            file_name = f"{str(row_data[0])}_template.html"
            html_files.append((file_name, html_content_modified))

            # Create a download button as fallback
            st.download_button(
                label=f"Download Modified HTML for {str(row_data[0])}", 
                data=html_content_modified, 
                file_name=file_name, 
                mime='text/html'
            )

        # Use JavaScript to attempt automatic downloads
        download_js = """
        <script>
        function downloadFile(filename, content) {
            const blob = new Blob([content], { type: 'text/html' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
        
        function downloadAllFiles() {
            const files = JSON.parse(document.getElementById('file_data').textContent);
            files.forEach(file => downloadFile(file.name, file.content));
        }

        window.onload = downloadAllFiles;
        </script>
        """

        # Render the HTML and JavaScript to attempt automatic download
        html_data = [{'name': f[0], 'content': f[1]} for f in html_files]
        components.html(f"""
            <div id="file_data" style="display: none;">{pd.json.dumps(html_data)}</div>
            {download_js}
        """, height=0)

# Tab 2: Story Generator (Similar to Tab 1; add download attempt code here as well if needed)
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
        placeholders_story = df_story.iloc[0].tolist()

        # Prepare a list of generated HTML files for download
        story_files = []

        # Loop through each row from index 1 onward to perform replacements
        for row_index in range(1, len(df_story)):
            actual_values_story = df_story.iloc[row_index].tolist()

            # Copy the original HTML template content
            html_content_story = html_content_template_story

            # Perform batch replacement for each placeholder in the row
            for placeholder, actual_value in zip(placeholders_story, actual_values_story):
                html_content_story = html_content_story.replace(str(placeholder), str(actual_value))

            # Use the first column value of each row as the filename
            output_filename_story = f"{actual_values_story[0]}.html"
            story_files.append((output_filename_story, html_content_story))

            # Create a download button as fallback
            st.download_button(
                label=f"Download Modified HTML for {actual_values_story[0]}",
                data=html_content_story,
                file_name=output_filename_story,
                mime='text/html'
            )

        # Render the HTML and JavaScript to attempt automatic download for story files
        story_js = """
        <script>
        function downloadFile(filename, content) {
            const blob = new Blob([content], { type: 'text/html' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
        
        function downloadAllFiles() {
            const files = JSON.parse(document.getElementById('story_file_data').textContent);
            files.forEach(file => downloadFile(file.name, file.content));
        }

        window.onload = downloadAllFiles;
        </script>
        """

        # Render the JavaScript for story file downloads
        story_data = [{'name': f[0], 'content': f[1]} for f in story_files]
        components.html(f"""
            <div id="story_file_data" style="display: none;">{pd.json.dumps(story_data)}</div>
            {story_js}
        """, height=0)
