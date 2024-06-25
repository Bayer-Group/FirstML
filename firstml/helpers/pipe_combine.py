class PipeCombine:
    def __init__(self):
        print("initiate PipeCombine")

    @staticmethod
    def combine_pipelines(gr):

        if "pipelines" in gr and len(gr["pipelines"]) > 0:

            nb_combined = []
            for pipeline in gr["pipelines"]:
                nodebooks = []
                for nodebook in pipeline["nodebooks"]:
                    nodebook["layer"] = pipeline["layer"]
                    nodebooks.extend(nodebook)
                nb_combined.extend(pipeline["nodebooks"])
            gr_combined = {"layer": "combined", "nodebooks": nb_combined}
        else:
            nodebooks = []
            for nodebook in gr["nodebooks"]:
                nodebook["layer"] = gr["layer"]
                nodebooks.append(nodebook)
            gr["nodebooks"] = nodebooks
            gr_combined = gr

        return gr_combined

    @staticmethod
    def inject_layer(gr):
        print("nothing")
