import streamlit as st
import pandas as pd
import json


def json_import(file):
	data = json.load(file)
	return data, variable_t_dict(data, data["model"]["horizon"]), variable_f_dict(data, data["model"]["horizon"])


def variable_t_dict(data, horizon):
	def list_variables(node_dict, prefix):
		if "variables" in node_dict:
			for vname, vvalues in node_dict["variables"].items():
				assert len(vvalues.keys()) == 1 and "values" in vvalues.keys() and isinstance(vvalues["values"], list)
				if len(vvalues["values"]) == horizon:
					yield ".".join(prefix + [vname]), vvalues["values"]
		if "sub_elements" in node_dict:
			for vname, vvalues in node_dict["sub_elements"].items():
				yield from list_variables(vvalues, prefix + [vname])

	return dict(list_variables({"sub_elements": data["solution"]["elements"]}, []))


def variable_f_dict(data, horizon):
	def list_variables(node_dict):
		out = {}
		if "sub_elements" in node_dict:
			for vname, vvalues in node_dict["sub_elements"].items():
				out[vname] = list_variables(vvalues)
		if "variables" in node_dict:
			for vname, vvalues in node_dict["variables"].items():
				if len(vvalues["values"]) != horizon:
					out[vname] = vvalues["values"] if len(vvalues["values"]) != 1 else vvalues["values"][0]
		return out
	return {x: list_variables(y) for x, y in data["solution"]["elements"].items()}


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
			data, variables_t, variables_f = json_import(json_file)
			horizon = data["model"]["horizon"]
			st.sidebar.metric(label="Objective", value=f"{data['solution']['objective']:.2f} €")
			st.sidebar.metric(label="Horizon", value=f"{horizon} h")

			option = st.multiselect('Select variable(s) to display', list(variables_t.keys()))

			if option is not None:
				all_var = {name: variables_t[name] for name in option}

				x_min, x_max = st.sidebar.slider('select time horizon', min_value=1, max_value=horizon,
												 value=(1, horizon), step=1)
				for k in all_var.keys():
					val = all_var[k]
					all_var[k] = val[x_min - 1:x_max - 1]
				st.line_chart(pd.DataFrame(all_var))

	elif choice == "Values":
		st.subheader("Values")
		json_file = st.file_uploader("Upload Json",type=["json"])
		if json_file is not None: 
			st.write(type(json_file))

			file_details = {"filename": json_file.name,"filetype" : json_file.type, "filesize": json_file.size}

			st.write(file_details)
			data, variables_t, variables_f = json_import(json_file)

			option = st.multiselect('Select variable(s) to display', list(variables_t.keys()))

			if option is not None:
				all_var = {name: variables_t[name] for name in option}

				for k in all_var.keys():
					val = all_var[k]
					all_var[k] = val

				st.write(pd.DataFrame(all_var))

	else : 
		st.subheader("About")
		st.write("Prototype of Post-Processing GBOML output by MIFTARI B")


if __name__ == '__main__':
	main()
