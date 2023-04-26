# Condition that removes all the rectangles and parallelograms except the first parallelogram

import streamlit as st
import zipfile
import io
import json

st.title('Automate your PowerBI Reports')

# Upload the Source zip file
ss = st.file_uploader('Upload a PBIX file')

# --------- Removing Streamlit's Hamburger and Footer starts ---------
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            a {text-decoration: none;}
            .css-15tx938 {font-size: 18px !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# --------- Removing Streamlit's Hamburger and Footer ends ------------
new_vc1 =                 {
                    "x": 69.38388625592417,
                    "y": 660.8530805687204,
                    "z": 0,
                    "width": 35.26066350710901,
                    "height": 29.57345971563981,
                    "config": "{\"name\":\"123104541ae573e00700\",\"layouts\":[{\"id\":0,\"position\":{\"x\":69.38388625592417,\"y\":660.8530805687204,\"z\":0,\"width\":35.26066350710901,\"height\":29.57345971563981}}],\"singleVisual\":{\"visualType\":\"actionButton\",\"drillFilterOtherVisuals\":true,\"objects\":{\"icon\":[{\"properties\":{\"shapeType\":{\"expr\":{\"Literal\":{\"Value\":\"'leftArrow'\"}}},\"lineColor\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#00519C'\"}}}}}},\"selector\":{\"id\":\"default\"}}]}}}",
                    "filters": "[]"
                },
new_vc2 =                 {
                    "x": 122.8436018957346,
                    "y": 660.8530805687204,
                    "z": 1,
                    "width": 32.985781990521325,
                    "height": 29.57345971563981,
                    "config": "{\"name\":\"163f28fe1120b90b497d\",\"layouts\":[{\"id\":0,\"position\":{\"x\":122.8436018957346,\"y\":660.8530805687204,\"z\":1,\"width\":32.985781990521325,\"height\":29.57345971563981}}],\"singleVisual\":{\"visualType\":\"actionButton\",\"drillFilterOtherVisuals\":true,\"objects\":{\"icon\":[{\"properties\":{\"shapeType\":{\"expr\":{\"Literal\":{\"Value\":\"'rightArrow'\"}}},\"lineColor\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#00519C'\"}}}}}},\"selector\":{\"id\":\"default\"}}]}}}",
                    "filters": "[]"
                }


if ss:
    if 1==1:
        # In-memory byte stream to hold the destination zip file data
        zip_data = io.BytesIO()

        # Extract the files from the source zip file and re-zip them into a destination zip file
        with zipfile.ZipFile(ss, 'r') as source_zip:
            with zipfile.ZipFile(zip_data, 'w') as destination_zip:
                # Iterate over the files in the source zip file
                for name in source_zip.namelist():

                    # Skip the Security Binding file
                    if name == 'SecurityBindings':
                        continue

                    # Manipulate the Layout file
                    if name == 'Report/Layout':
                        # Read the contents of the layout file
                        data = source_zip.read(name).decode('utf-16 le')
                        # Old layout file
                        with open('app-og.json', 'w') as f:
                            a=json.loads(data)
                            json.dump(a, f)
                        try:
                            data=json.loads(data)
                            ##### Changing attributes of certain elements
                            for section in data['sections']:
                                # print(section,'section')
                                section['visualContainers'].append(new_vc1)
                                section['visualContainers'].append(new_vc2)
                                    
                            # New Layout file
                            with open('app-generated.json', 'w') as f:
                                json.dump(data, f)
                        
                        except:
                            print('hi')
                        # Add the manipulated layout data to the destination zip file
                        data = json.dumps(data)
                        destination_zip.writestr(name, data.encode('utf-16 le'))
                    
                    else:
                        # Add the file to the destination zip file as-is
                        binary_data = source_zip.read(name)
                        destination_zip.writestr(name, binary_data)


        # Download the destination file
        st.download_button(
            label='Download Destination PBIX File',
            data=zip_data.getvalue(),
            file_name='destination.pbix',
            mime='application/pbix'
        )
    else:
        print('')


st.markdown('---')
st.markdown('Made with :heart: by [Sahil Choudhary](https://www.sahilchoudhary.ml/)')
