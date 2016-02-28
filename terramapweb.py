from subprocess import check_output
from os import listdir
from flask import Flask, send_file, abort, request, render_template
from datetime import *
import getpass
app = Flask(__name__)

path_to_world_dir = "C:\Users\{0}\Documents\My Games\Terraria\Worlds"
path_to_file = path_to_world_dir + "\{1}"
user = getpass.getuser()


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/worlds")
def get_worlds():
    worlds = [f for f in listdir(path_to_world_dir.format(user)) if (f.endswith(".wld"))]
    return render_template("worlds.html", worlds=worlds)


@app.route("/maps")
def get_maps():
    maps = [f for f in listdir(path_to_world_dir.format(user)) if (f.endswith(".png"))]
    return render_template("maps.html", maps=maps)


@app.route("/worlds/<world>", methods=['POST'])
def post_world(world):
    tileIds = request.form["tiles"]
    itemIds = request.form["items"]
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = "{0}_{1}_tiles_{2}_items_{3}.png".format(world, timestamp, tileIds, itemIds)
    input_file_path = path_to_file.format(user, world)
    output_file_path = path_to_file.format(user, filename)
    terramap_output = check_output('terramapcmd -i \"{0}\" -o \"{1}\" -t \"{2}\" -m \"{3}\"'.format(input_file_path, output_file_path, tileIds, itemIds), shell=True)

    viewmodel = {"terramap_lines": terramap_output.split("\r\n"), "filename": filename}
    return render_template("map_created.html", viewmodel=viewmodel)


@app.route("/worlds/<file_name>", methods=['GET'])
def get_world(file_name):
    if not file_name.endswith(".wld"):
        return abort(404)
    return send_file(path_to_file.format(user, file_name))


@app.route("/maps/<file_name>")
def get_map(file_name):
    if not file_name.endswith(".png"):
        return abort(404)
    return send_file(path_to_file.format(user, file_name), mimetype="image/png")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
