from diagrams import Cluster, Diagram, Edge
from diagrams.programming.framework import Vue, FastAPI
from diagrams.programming.flowchart import Action
from diagrams.programming.language import Python
from diagrams.custom import Custom

graph_attr = {"dpi": "400", "rank": "same", "bgcolor": "transparent"}

with Diagram(
    "",
    filename="readme_images/tech_stack_image",
    show=False,
    graph_attr=graph_attr,
):
    # host = Custom("Hosted on Render", "./readme_images/render_logo.png")
    with Cluster("Hosted on Render"):
        start1 = Action("Inputs from User")
        start2 = Python("Default Items")
        route1 = FastAPI()
        with Cluster("Web App"):
            web_app_nodes = [
                Vue("Positions"),
                Vue("Prices"),
                Vue("Optimizer Inputs"),
                Vue("Generate Team"),
            ]
        route2 = FastAPI()
        backend_main = Python(f"app.py")
        with Cluster("Backend Operations"):
            main_actions = [
                Python("Save to Data Files"),
                Python("Compute Constructor\nPositions"),
                Python("Execute Optimizer"),
                Python("Send Data to UI"),
            ]
        # route1 >> host
        start1 >> route1
        start2 >> route1
        route1 << Edge() >> web_app_nodes
        web_app_nodes << Edge() >> route2
        route2 << Edge() >> backend_main
        backend_main << Edge() >> main_actions
