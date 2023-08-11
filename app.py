if __name__ == "__main__":

    import requests
    import os
    import shutil

    import yaml
    import flask
    import flask_cors

    # 仅支持native算法
    from sites import mux
    
    # 激活适配器
    import sites.github

    # 检查server.yaml是否存在
    if not os.path.exists("server.yaml"):
        shutil.copyfile("server-template.yaml", "server.yaml")

    cfg: dict = None
    # 读取配置文件
    with open("server.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
        
    PORT = cfg["port"]

    app = flask.Flask(__name__)

    flask_cors.CORS(app, origins=[f"http://localhost:{PORT}", "https://chat.openai.com"])

    @app.route("/.well-known/ai-plugin.json")
    def ai_plugin_json():
        # 发送static/ai-plugin.json
        return flask.send_from_directory("static", "ai-plugin.json")

    @app.route("/openapi.yaml")
    def openapi_yaml():
        # 发送static/openapi.yaml
        return flask.send_from_directory("static", "openapi.yaml")
    
    @app.route("/legal_info.html")
    def legal_info_html():
        # 发送static/legal_info.html
        return flask.send_from_directory("static", "legal_info.html")

    @app.route("/logo.png")
    def logo_png():
        # 发送static/logo.png
        return flask.send_from_directory("static", "logo.png")

    @app.route("/access_web", methods=["GET"])
    def access_web():
        return mux.process(**flask.request.args)

    app.run(host=cfg["host"], port=cfg["port"])
