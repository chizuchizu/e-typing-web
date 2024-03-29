# -*- coding: utf-8 -*-
import matplot
import hensachi
import pasento

import os
from flask import Flask, make_response, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    a = request.form.getlist("action")
    # print(request.method)

    if len(a) != 0:
        return redirect(url_for("user"))

    if request.method == "GET":
        return render_template("index.html")
    else:
        if request.form["name"]:
            return redirect(url_for("user_graph", name=request.form["name"]))

        elif not os.path.isfile("data/score_" + str(request.form["num"]) + ".npy"):
            print("error")
            return redirect(url_for("none"))
        else:
            return redirect(url_for("graph", number=request.form["num"]))
            # return graph(request.form["num"])


@app.route("/graph/<string:number>")
def graph(number):
    # number = "912"  # debug用
    data = matplot.byoga(number)
    response = make_response(data)
    response.headers["Content-Type"] = "image/png"
    response.headers["Content-Length"] = len(data)
    return response


@app.route("/none")
def error():
    return render_template("error.html")


@app.route("/user", methods=["GET", "POST"])
def user():
    # print(request.method)
    if request.method == "GET":
        # print("GET")
        return render_template("user.html")
    else:
        return redirect(url_for("user_something", number=request.form["num"]))


@app.route("/user_shosai/<string:number>", methods=["GET", "POST"])
def user_something(number):
    hensa = hensachi.keisan("955", number)
    pas = pasento.keisan("955", number)
    return render_template("user_data.html", score=number, hensa=hensa, pasento=pas)


@app.route("/user_graph/<string:name>")
def user_graph(name):
    import user_graph
    print(user_graph)
    data = user_graph.main2(str(name))
    response = make_response(data)
    response.headers["Content-Type"] = "image/png"
    response.headers["Content-Length"] = len(data)
    return response


if __name__ == '__main__':
    app.run(debug=True)
