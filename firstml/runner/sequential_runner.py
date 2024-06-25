import getpass
import os
import time

import papermill as pm

import yaml

from firstml.graph.graph_resolver import GraphResolver
from firstml.helpers.pipe_combine import PipeCombine


class SequentialRunner:
    def __init__(self):

        self.g_resolver = GraphResolver()
        self.pipe_combine = PipeCombine()

    @staticmethod
    def _build_source_nb_path(nb_layer, nb_id, params):

        nb_source = f"{params['base_path']}{params['nodebook_path']}/{nb_layer}/{nb_id}.ipynb"

        return nb_source

    @staticmethod
    def _build_result_nb_path(project_name, nb_layer, nb_id, ts, params):

        dev_usr = getpass.getuser()
        results_dir = f"{params['base_path'] + params['data_home'] }/nodebook_runs/{dev_usr}/"

        nb_result = None
        if nb_layer is not None:
            if not os.path.exists(f"{results_dir}/{ts}/{project_name}/{nb_layer}"):
                os.makedirs(f"{results_dir}/{ts}/{project_name}/{nb_layer}/")

            nb_result = f"{results_dir}/{ts}/{project_name}/{nb_layer}/{nb_id}.ipynb"
        else:
            nb_result = f"{results_dir}/{ts}/{project_name}/{nb_id}.ipynb"

        return nb_result

    @staticmethod
    def _build_result_nb_link(project_name, nb_layer, nb_id, ts, params):

        dev_usr = getpass.getuser()

        nb_link = None
        if nb_layer is not None:
            nb_link = (
                f"{params['base_url']}/{params['data_home']}/"
                f"nodebook_runs/{dev_usr}/{ts}/{project_name}/{nb_layer}/{nb_id}.ipynb"
            )
        else:
            nb_link = (
                f"{params['base_url']}/{params['data_home']}/"
                f"nodebook_runs/{dev_usr}/{ts}/{project_name}/{nb_id}.ipynb"
            )

        return nb_link

    def _execute_intro(self, ts, project_name, pipeline, common_params, catalog):
        dev_usr = getpass.getuser()
        intro_parameters = dict()
        intro_parameters.update({"parameters": common_params})
        intro_parameters.update({"pipeline": pipeline})
        intro_parameters.update({"catalog": catalog})
        print("..saving pipeline definitions and lineage")

        results_dir = f"{common_params['base_path'] + common_params['data_home'] }/nodebook_runs/{dev_usr}/"

        nb_source = f"{common_params['nodebook_path']}/intro.ipynb"

        nb_result = self._build_result_nb_path(project_name, None, "intro", ts, common_params)

        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        if not os.path.exists(f"{results_dir}/{ts}"):
            os.makedirs(f"{results_dir}/{ts}")

        if not os.path.exists(f"{results_dir}/{ts}/{project_name}"):
            os.makedirs(f"{results_dir}/{ts}/{project_name}/")

        nb_link = self._build_result_nb_link(project_name, None, "intro", ts, common_params)

        print(f"..open here once completed: [INTRO]({nb_link}) ")

        pm.execute_notebook(nb_source, nb_result, parameters=intro_parameters)

        intro_config_yml = {
            "title": project_name,
            "author": dev_usr,
            "logo": "bayer.jpeg",
            "execute": {"execute_notebooks": "off"},
            "bibtex_bibfiles": ["references.bib"],
        }

        with open(f"{results_dir}/{ts}/{project_name}/_config.yml", "w") as file:
            yaml.dump(intro_config_yml, file, sort_keys=False)

    def _execute_nodebook(self, ts, project_name, nb_layer, nodebook, common_params, catalog):
        nb_parameters = dict(common_params)
        nb_parameters.update(nodebook["params"])
        print(
            f"..running nodebook {nodebook['nodebook_id']}_{nodebook['nodebook_id_suffix']}"
            f" - inputs: {nodebook['inputs']} - outputs: {nodebook['outputs']} "
        )

        if nodebook["type"] == "common":
            self._nb_custom_op(
                ts,
                project_name,
                nodebook["nodebook_id"],
                nodebook["nodebook_id_suffix"],
                nb_layer,
                "common",
                nodebook["inputs"],
                nodebook["outputs"],
                nb_parameters,
                catalog,
            )

        if nodebook["type"] == "custom":
            self._nb_custom_op(
                ts,
                project_name,
                nodebook["nodebook_id"],
                nodebook["nodebook_id_suffix"],
                nb_layer,
                nb_layer,
                nodebook["inputs"],
                nodebook["outputs"],
                nb_parameters,
                catalog,
            )

        if nodebook["type"] == "model":
            dev_usr = getpass.getuser()
            experiment = {"experiment": f"{nodebook['nodebook_id']}_{nodebook['nodebook_id_suffix']}_{dev_usr}_{ts}"}
            nb_parameters["tags"].update(experiment)
            mod_registry_dir = {
                "mod_registry_dir": f"file:///{common_params['base_path'] + common_params['data_home']}/ml_runs"
            }
            nb_parameters.update(mod_registry_dir)

            nb_data_path = {
                "nb_data_path": f"{common_params['base_path']+common_params['data_home']}"
                f"/nodebook_runs/{dev_usr}/{ts}/{project_name}/{nb_layer}/"
                f"{nodebook['nodebook_id']}_{nodebook['nodebook_id_suffix']}_artifacts"
            }

            if not os.path.exists(nb_data_path["nb_data_path"]):
                os.makedirs(nb_data_path["nb_data_path"])
            nb_data_folder = {
                "nb_data_folder": f"./{nodebook['nodebook_id']}_{nodebook['nodebook_id_suffix']}_artifacts"
            }
            nb_parameters.update(nb_data_path)
            nb_parameters.update(nb_data_folder)

            self._nb_custom_op(
                ts,
                project_name,
                nodebook["nodebook_id"],
                nodebook["nodebook_id_suffix"],
                nb_layer,
                nb_layer,
                nodebook["inputs"],
                nodebook["outputs"],
                nb_parameters,
                catalog,
            )

    @staticmethod
    def _catalog_lookup(datasets, catalog):
        cl_datasets = []
        for dataset in datasets:
            cl_dataset = catalog[dataset]
            cl_dataset["id"] = dataset
            cl_datasets.append(cl_dataset)

        return cl_datasets

    def _nb_custom_op(self, ts, project_name, nb_id, nb_id_sfx, layer, subdir, inputs, outputs, params, catalog):

        nb_source = self._build_source_nb_path(subdir, nb_id, params)
        nb_result = self._build_result_nb_path(project_name, layer, f"{nb_id}_{nb_id_sfx}", ts, params)
        nb_link = self._build_result_nb_link(project_name, layer, f"{nb_id}_{nb_id_sfx}", ts, params)

        nb_parameters = dict(params)

        catalog_inputs = self._catalog_lookup(inputs, catalog)
        nb_parameters.update({"inputs": catalog_inputs})

        catalog_outputs = self._catalog_lookup(outputs, catalog)
        nb_parameters.update({"outputs": catalog_outputs})

        nb_parameters.update({"nb_link": nb_link})

        nb_parameters.update({"project_name": project_name})
        nb_parameters.update({"ts": ts})

        print(f"..open here once completed: [{nb_id}_{nb_id_sfx}]({nb_link}) ")

        pm.execute_notebook(nb_source, nb_result, parameters=nb_parameters)

    def run(self, project_name, graph, common_params, catalog):
        dev_usr = getpass.getuser()

        ts = time.time_ns()

        graph = self.pipe_combine.combine_pipelines(graph)

        sorted_graph = self.g_resolver.resolve_run(graph)

        tos_config_yml = {"format": "jb-book", "root": "intro", "chapters": []}

        results_dir = f"{common_params['base_path'] + common_params['data_home'] }/nodebook_runs/{dev_usr}/"

        id_count = 1
        for x in sorted_graph:
            nodebook = [
                node for node in graph["nodebooks"] if (node["nodebook_id"] + "_" + node["nodebook_id_suffix"]) == x
            ]
            self._execute_nodebook(ts, project_name, nodebook[0]["layer"], nodebook[0], common_params, catalog)
            file = {
                "file": f"{nodebook[0]['layer']}/{nodebook[0]['nodebook_id']+'_'+nodebook[0]['nodebook_id_suffix']}",
                "title": f"{str(id_count)+'_'+nodebook[0]['nodebook_id']+'_'+nodebook[0]['nodebook_id_suffix']}",
            }
            tos_config_yml["chapters"].append(file)
            id_count += 1

        with open(f"{results_dir}/{ts}/{project_name}/_toc.yml", "w") as file:
            yaml.dump(tos_config_yml, file, sort_keys=False)
