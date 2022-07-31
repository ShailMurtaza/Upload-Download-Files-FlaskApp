from flask import Flask, render_template, send_file, redirect, request
import os
import shutil

app = Flask(__name__)
app.secret_key = "Secret"
main_path = "uploads" + "/"
main_path = "E:/Partition/Games setup/"


def cleaner(url):
    # cleanr = re.compile('http://.*?/')
    # cleantext = re.sub(cleanr, '', url).
    # replace("%20", ' ').replace('get/', '')
    url = url.replace("%20", ' ')
    url = '/'.join(url.split('/')[::2])
    return url


def path_format(filname):
    path = filname.split('/')[1:-1]
    new_path = []
    for i in path:
        new_path.append('get')
        new_path.append(i)
    path = '/' + '/'.join(new_path)
    return path


# Make list of files and directory
def uploaded(path):
    new_dirs = []
    dirs = os.listdir(path)
    path = path + '/'
    for x, name in enumerate(dirs):
        form = os.path.isdir(path + name)
        form = 'folder' if form is True else 'file'
        new_dirs.append((x, name, form))
    if not new_dirs:
        new_dirs = "None"
    return new_dirs


@app.route('/')
@app.route('/get/')
@app.route('/get/<path:url>')
def lister(url=""):
    # print((request.url + "\n")*3)
    # path = cleaner(request.url)
    path = cleaner(url)
    # print("#####")
    # print(path)
    # print("#####")
    path2 = "/get/" + "/get/".join(path.split("/")[:-1])
    if path2 == "/get/": path2 = "/"
    print(path2)
    path = (main_path + path)
    if path:
        if path[-1] == "/":
            path = path[:-1]
    if os.path.isfile(path):
        return send_file(path)
    else:
        dirs = uploaded(path)
        return render_template("dir.html", dirs=dirs, path=path2)


@app.route('/', methods=['POST'])
@app.route('/get/<path:url>', methods=['POST'])
def upload_file(url='/'):
    url = cleaner(url)
    if url:
        url += '/'
    path = (main_path + url)
    files = request.files.getlist('files')
    for file in files:
        filename = path + file.filename
        file.save(filename)
    print(path)
    path = path_format(path)
    print(path)
    return redirect(path)


@app.route('/back/<path:url>')
def back(url):
    print(url)
    url = path_format(url)
    print(url)
    return redirect(url)


@app.route('/delete/<path:filename>')
def delete(filename):
    if filename:
        if os.path.isfile(filename):
            os.remove(filename)
        elif os.path.isdir(filename):
            shutil.rmtree(filename)
        path = path_format(filename)
        return redirect(path)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
