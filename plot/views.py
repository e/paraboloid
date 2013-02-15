from __future__ import division
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.utils import translation
import django
    
from math import log, sqrt, pi, sin, cos
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FixedLocator

from plot.forms import DataForm

from paraboloid.settings import LANGUAGES

@csrf_protect
def home(request):
    f = request.GET.get('f') or 3
    xran = request.GET.get('xran') or 100
    size = request.GET.get('size') or 10
    shape = request.GET.get('shape')
    try:
        f = float(f)
        if f > 100:
            f = 100
        if f < 0.001:
            f = 0.001
    except ValueError:
        f = 3
    try:
        xran = int(xran)
        if xran > 5000:
            xran = 5000
        if xran < 1:
            xran = 1
    except ValueError:
        xran = 100
    try:
        size = int(size)
        if size > 100:
            size = 100
        if size < 1:
            size = 1
    except ValueError:
        size = 10

    form = DataForm(initial=request.GET)
    context = {
            'f': f,
            'xran': xran,
            'size': size,
            'dataform': form,
            'shape': shape,
            'LANGUAGES': LANGUAGES,
    }
    translation.activate(translation.get_language())
    return render_to_response('home.html', context, 
            context_instance=RequestContext(request))


def pimage(request):
    px = []
    py = []
    r = []
    cut = []
    c = []
    x45 = []
    y45 = []
    f = request.GET.get('f') or 3
    xran = request.GET.get('xran') or 100
    size = request.GET.get('size') or 10
    shape = request.GET.get('shape') or "square"
    try:
        f = float(f)
        if f > 100:
            f = 100
        if f < 0.001:
            f = 0.001
    except ValueError:
        f = 3
    xran = request.GET.get('xran') or 100

    try:
        xran = int(xran)
        if xran > 5000:
            xran = 5000
    except ValueError:
        xran = 50

    try:
        size = int(size)
        if size > 100:
            size = 100
        if size < 1:
            size = 1
    except ValueError:
        size = 10

    for xvalue in range(-xran, xran+1):
        i = xvalue + xran
        px.append(xvalue/10)
        py.append(px[i]**2/4/f)
        t = sqrt(px[i]**2 + 4 * f**2)
        if (py[i] == 0):
            r.append(0)
            cut.append(2 * pi * (r[i] - px[i]))
        else:
            r.append((px[i] * t + 4 * f**2 * log((px[i] + t) / (2 * f))) /
                    (4 * f))
            cut.append(2 * pi * (r[i] - px[i]))
        c.append(cut[i] / 16)
        x45.append(r[i] * cos(pi / 4) - c[i] * sin(pi / 4))
        y45.append(r[i] * sin(pi / 4) + c[i] * cos(pi / 4))

    x = [val for val in r]
    y = [val for val in c]
    mx = [-val for val in r]
    my = [-val for val in c]
    x45m = [-val for val in x45]
    y45m = [-val for val in y45]

    size = request.GET.get('size') or 10
    try:
        size = int(size)
        if size > 100:
            size = 100
    except ValueError:
        size = 10
    fig = Figure(figsize=(size,size), frameon=False)
    ax = fig.add_subplot(111)
    ax.plot(x, y, '-')
    ax.plot(x, my, '-')
    ax.plot(y, x, '-')
    ax.plot(y, mx, '-')
    ax.plot(x45, y45, '-')
    ax.plot(y45, x45m, '-')
    ax.plot(x45m, y45, '-')
    ax.plot(y45m, x45m, '-')
    ax.grid(True)
    ax.xaxis.set_major_locator(FixedLocator(range(int(x[0]), int(-x[0]))))
    ax.yaxis.set_major_locator(FixedLocator(range(int(x[0]), int(-x[0]))))
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.text(4, 1, "f = %d" % f)
    canvas = FigureCanvas(fig)
    fig.tight_layout(pad=0.1)
    response = django.http.HttpResponse(content_type='image/png')
    if shape == "square":
        ax.set_xlim(x45[0], -x45[0])
        ax.set_ylim(x45[0], -x45[0])
    else:
        ax.set_xlim(x[0], -x[0])
        ax.set_ylim(x[0], -x[0])

    if request.GET.get('download'):
        response['Content-Disposition'] = 'attachment; filename="paraboloid.png"'

#    import code;code.interact(local=locals())
    canvas.print_png(response, bbox_inches="tight")
    return response


