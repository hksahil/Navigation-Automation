# Condition that removes all the rectangles and parallelograms except the first parallelogram

import streamlit as st
import zipfile
import io
import json

st.title('Add Next and Back buttons to your PowerBI Reports')

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


new_vc1 = {
    "x": 1053,
    "y": 15,
    "z": 130000,
    "width": 35,
    "height": 35,
    "config": "{\"name\":\"123104541ae573e00700\",\"layouts\":[{\"id\":0,\"position\":{\"x\":1053,\"y\":15,\"z\":130000,\"width\":35,\"height\":35,\"tabOrder\":60000}}],\"singleVisual\":{\"visualType\":\"actionButton\",\"drillFilterOtherVisuals\":true,\"objects\":{\"icon\":[{\"properties\":{\"shapeType\":{\"expr\":{\"Literal\":{\"Value\":\"'leftArrow'\"}}},\"lineColor\":{\"solid\":{\"color\":{\"expr\":{\"ThemeDataColor\":{\"ColorId\":0,\"Percent\":0}}}}}},\"selector\":{\"id\":\"default\"}}]},\"vcObjects\":{\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"dropShadow\":[{\"properties\":{\"angle\":{\"expr\":{\"Literal\":{\"Value\":\"0L\"}}},\"shadowDistance\":{\"expr\":{\"Literal\":{\"Value\":\"0L\"}}},\"shadowBlur\":{\"expr\":{\"Literal\":{\"Value\":\"15L\"}}},\"shadowSpread\":{\"expr\":{\"Literal\":{\"Value\":\"3L\"}}},\"transparency\":{\"expr\":{\"Literal\":{\"Value\":\"70L\"}}},\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]}}}",
    "filters": "[]",
    "tabOrder": 6000
}       
new_vc2=      {
            "x": 1105.3386454183267,
            "y": 15,
            "z": 130000,
            "width": 35,
            "height": 35,
            "config": "{\"name\":\"163f28fe1120b90b497d\",\"layouts\":[{\"id\":0,\"position\":{\"x\":1105.3386454183267,\"y\":15,\"z\":130000,\"width\":35,\"height\":35,\"tabOrder\":60000}}],\"singleVisual\":{\"visualType\":\"actionButton\",\"drillFilterOtherVisuals\":true,\"objects\":{\"icon\":[{\"properties\":{\"shapeType\":{\"expr\":{\"Literal\":{\"Value\":\"'rightArrow'\"}}},\"lineColor\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#FFFFFF'\"}}}}}},\"selector\":{\"id\":\"default\"}}]},\"vcObjects\":{\"background\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"dropShadow\":[{\"properties\":{\"angle\":{\"expr\":{\"Literal\":{\"Value\":\"0L\"}}},\"shadowDistance\":{\"expr\":{\"Literal\":{\"Value\":\"0L\"}}},\"shadowBlur\":{\"expr\":{\"Literal\":{\"Value\":\"15L\"}}},\"shadowSpread\":{\"expr\":{\"Literal\":{\"Value\":\"3L\"}}},\"transparency\":{\"expr\":{\"Literal\":{\"Value\":\"70L\"}}},\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"visualLink\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"type\":{\"expr\":{\"Literal\":{\"Value\":\"'PageNavigation'\"}}},\"navigationSection\":{\"expr\":{\"Literal\":{\"Value\":\"'ReportSectione8ac142a046f9e1a3128'\"}}}}}]}}}",
            "filters": "[]",
            "tabOrder": 10000
        }
# new_vc2 =                 {
#                     "x": 1107,
#                     "y": 15,
#                     "z": 13000,
#                     "width": 35,
#                     "height": 35,
#                     "config": "{\"name\":\"163f28fe1120b90b497d\",\"layouts\":[{\"id\":0,\"position\":{\"x\":1107,\"y\":15,\"z\":13000,\"width\":35,\"height\":35}}],\"singleVisual\":{\"visualType\":\"actionButton\",\"drillFilterOtherVisuals\":true,\"objects\":{\"icon\":[{\"properties\":{\"shapeType\":{\"expr\":{\"Literal\":{\"Value\":\"'rightArrow'\"}}},\"lineColor\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#00519C'\"}}}}}},\"selector\":{\"id\":\"default\"}}]}}}",
#                     "filters": "[]"
#                 }


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
