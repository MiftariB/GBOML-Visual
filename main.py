import streamlit as st
import pandas as pd
import json

def json_import(file):
	data = json.load(file)
	return data

def main():
	st.title("GBOML Analyzer")

	menu = ["Plot","Values","About "]
	choice = st.sidebar.selectbox("Menu",menu)
	if choice == "Plot":
		st.subheader("Plot")
		json_file = st.file_uploader("Upload Json",type=["json"])
		if json_file is not None: 
			st.write(type(json_file))

			file_details = {"filename": json_file.name,"filetype" : json_file.type, "filesize": json_file.size}

			st.write(file_details)
			data = json_import(json_file)
			#st.write(data)
			solution = data["solution"]
			nodes = solution["nodes"]
			keys = nodes.keys()

			model = data["model"]
			horizon = model["horizon"]

			option = st.multiselect(
		    'Which node do you want to plot',
		     list(keys))

			if option is not None: 
				all_var = {}
				for node_name in option:
					node_i = nodes[node_name]
					var = node_i["variables"]
					option_var = st.multiselect(
		    		'Which variables do you want to plot in the node '+node_name,
		     		list(var.keys()))
					for k in option_var:
						full_name = node_name+"."+str(k)
						all_var[full_name] = var[k]

				x_min, x_max = st.sidebar.slider('select Abscissa',min_value=1, max_value=horizon, value=(1,horizon), step=1)
				for k in all_var.keys(): 
					val = all_var[k]
					all_var[k] = val[x_min-1:x_max-1]

				st.line_chart(pd.DataFrame(all_var))

	elif choice == "Values":
		st.subheader("Values")
		json_file = st.file_uploader("Upload Json",type=["json"])
		if json_file is not None: 
			st.write(type(json_file))

			file_details = {"filename": json_file.name,"filetype" : json_file.type, "filesize": json_file.size}

			st.write(file_details)
			data = json_import(json_file)
			#st.write(data)
			solution = data["solution"]
			nodes = solution["nodes"]
			keys = nodes.keys()

			option = st.multiselect(
		    'Which node do you want to plot',
		     list(keys))

			if option is not None: 
				all_var = {}
				for node_name in option:
					node_i = nodes[node_name]
					var = node_i["variables"]
					option_var = st.multiselect(
		    		'Which variables do you want to plot in the node '+node_name,
		     		list(var.keys()))

					for k in option_var:
						full_name = node_name+"."+str(k)
						all_var[full_name] = var[k]
						
				st.write(pd.DataFrame(all_var))

	else : 
		st.subheader("About")
		st.write("Prototype of Post-Processing GBOML output by MIFTARI B")


if __name__ == '__main__':
	main()
