import bisect
import collections
import itertools
import math
import tempfile
from functools import partial
from typing import Iterable, List, Mapping, Optional, Tuple

import pygal.formatters
import pygal.serie
import pygal.style
import pygal.util


__all__ = 'decimate', 'moving_average', 'plot'

Point = Tuple[float, float]


def get_line_distance(p0: Point, p1: Point, p2: Point) -> float:
    """
    Return the distance from p0 to the line formed by p1 and p2.

    Points are represented by 2-tuples.
    """

    if p1 == p2:
        return math.hypot(p1[0] - p0[0], p1[1] - p0[1])

    slope_nom = p2[1] - p1[1]
    slope_denom = p2[0] - p1[0]

    return (
        abs(slope_nom * p0[0] - slope_denom * p0[1] + p2[0] * p1[1] - p2[1] * p1[0])
        / math.hypot(slope_denom, slope_nom)
    )


def decimate(points: List[Point], epsilon: float) -> List[Point]:
    """
    Decimate given poly-line using Ramer-Douglas-Peucker algorithm.

    It reduces the points to a simplified version that loses detail,
    but retains its peaks.
    """

    if len(points) < 3:
        return points

    dist_iter = map(partial(get_line_distance, p1=points[0], p2=points[-1]), points[1:-1])
    max_index, max_value = max(enumerate(dist_iter, start=1), key=lambda v: v[1])

    if max_value > epsilon:
        return (
            decimate(points[:max_index + 1], epsilon)[:-1]
            + decimate(points[max_index:], epsilon)
        )
    else:
        return [points[0], points[-1]]


def moving_average(points: Iterable[Point], n: int) -> Iterable[Point]:
    """
    Calculate moving average time series of given time series.

    The average is taken from an equal number of points on either side
    of a central value. This ensures that variations in the average are
    aligned with the variations in the data rather than being shifted
    in time. ``n // 2`` values are skipped from either side of the
    series. It is equivalent of::

        df = pandas.DataFrame(points, columns=('x', 'y'))
        df.y = df.y.rolling(window=n, center=True).mean()
        df.dropna()

    """

    assert n > 0, 'n must be a positive number'

    x_series, y_series = itertools.tee(points, 2)
    x_series = itertools.islice(x_series, n // 2, None)

    d = collections.deque(y_point[1] for y_point in itertools.islice(y_series, n - 1))
    d.appendleft(0)
    s = sum(d)
    for x_point, y_point in zip(x_series, y_series):
        s += y_point[1] - d.popleft()
        d.append(y_point[1])
        yield x_point[0], s / n


class CompactXLabelDateTimeLine(pygal.DateTimeLine):  # type: ignore[module-attr]

    def _compute_x_labels(self):
        """Override to make compact X labels -- no repetition of dates."""

        super()._compute_x_labels()

        last_date_str = None
        for i, (ts_str, ts) in enumerate(self._x_labels):
            if last_date_str == ts_str[:10]:
                self._x_labels[i] = ts_str[11:], ts

            last_date_str = ts_str[:10]


class DateTimeDotLine(CompactXLabelDateTimeLine):
    """
    An override of Pygal's date-time line chart that adds a few dots.

    It displays dots on each serie's line close to its intersection
    with X axis' labels. Dots show a tooltip on hover with the exact
    value and series name.
    """

    _dot_class = 'dot reactive tooltip-trigger'

    def __init__(self, config=None, **kwargs):
        super().__init__(config, **kwargs)

        # Disable default Pygal dots.
        self.config.show_dots = False

    def _get_x_label_view_points(
        self, serie: pygal.serie.Serie, rescale: bool
    ) -> Iterable[Tuple[int, Point]]:
        if rescale and self.secondary_series:
            points = self._rescale(serie.points)
        else:
            points = serie.points

        # Note that Pygal BaseGraph.prepare_values aligns with None
        # values all series on the respective axis to have the same
        # number of values
        safe_index_points = [(i, p) for i, p in enumerate(points) if p[0] is not None]
        # It is assumed that the X values are chronologically ordered
        safe_x_range = [t[1][0] for t in safe_index_points]

        # Note that dictionaries retain insertion order, so it can
        # be used here for deduplication
        label_points = {}
        for _, ts in self._x_labels:
            safe_index = bisect.bisect_left(safe_x_range, ts)
            if safe_index < len(safe_index_points):
                point_index, point = safe_index_points[safe_index]
                label_points[point_index] = point

        for i, (x, y) in zip(label_points.keys(), map(self.view, label_points.values())):
            if None in (x, y):
                continue
            elif self.logarithmic and (points[i][1] is None or points[i][1] <= 0):
                continue

            yield i, (x, y)

    def _draw_x_label_dots(
        self, serie: pygal.serie.Serie, view_points: Iterable[Tuple[int, Point]]
    ):
        serie_node = self.svg.serie(serie)
        for i, (x, y) in view_points:
            metadata = serie.metadata.get(i)
            dots = pygal.util.decorate(
                self.svg,
                self.svg.node(serie_node['overlay'], class_='dots'),
                metadata
            )

            val = self._format(serie, i)
            circle = self.svg.transposable_node(
                dots, 'circle', cx=x, cy=y, r=serie.dots_size, class_=self._dot_class
            )
            pygal.util.alter(circle, metadata)
            self._tooltip_data(dots, val, x, y, xlabel=self._get_x_label(i))
            self._static_value(
                serie_node,
                val,
                x + self.style.value_font_size,
                y + self.style.value_font_size,
                metadata,
            )

    def line(self, serie, rescale=False):
        """Override to plot dots at around X label intersections."""

        super().line(serie, rescale)

        view_points = self._get_x_label_view_points(serie, rescale)
        self._draw_x_label_dots(serie, view_points)


def plot(
    pid_series_list: List[Mapping[int, List[Point]]],
    queries: list,
    plot_file: str,
    *,
    title: Optional[str] = None,
    style: Optional[str] = None,
    formatter: Optional[str] = None,
    share_y_axis: bool = False,
    logarithmic: bool = False,
    no_dots: bool = False,
):
    assert pid_series_list and len(pid_series_list) == len(queries), 'Series must match queries'
    assert share_y_axis or len(pid_series_list) <= 2, 'Only one Y axis allowed with share_y_axis'

    if not title:
        if share_y_axis:
            title = '; '.join(f'{i}. {q.title}' for i, q in enumerate(queries, start=1))
        elif len(queries) == 1:
            title = queries[0].title
        else:
            title = f'{queries[0].title} vs {queries[1].title}'

    with tempfile.NamedTemporaryFile('w') as f:
        f.write(_ui_js)
        f.flush()

        line_cls = CompactXLabelDateTimeLine if no_dots else DateTimeDotLine
        datetimeline = line_cls(
            width=912,
            height=684,
            show_dots=False,
            logarithmic=logarithmic,
            x_label_rotation=35,
            title=title,
            value_formatter=getattr(pygal.formatters, formatter or 'human_readable'),
            style=getattr(pygal.style, style or 'DefaultStyle'),
            no_prefix=True,
            js=[f'file://{f.name}'],  # embed "svg/ui.py" converted to JavaScript
        )
        datetimeline.config.css.append(f'inline:{_ui_css}')
        datetimeline.config.style.tooltip_font_size = 11

        for i, (query, pid_series) in enumerate(zip(queries, pid_series_list)):
            for pid, points in pid_series.items():
                datetimeline.add(
                    '{name} {pid}'.format(pid=pid, name=query.name or f'№{i + 1}'),
                    points,
                    secondary=not share_y_axis and bool(i),
                )

        datetimeline.render_to_file(plot_file)


_ui_css = '''
.tooltip text.legend {font-size: 1em}
.tooltip text.value {font-size: 1.2em}
'''

_ui_js = (
    r'var t,e;function i(t){return t.set_properties=function(t,e){var i,s,n=e;for(var o in n)'
    r'n.hasOwnProperty(o)&&(i=!((s=e[o])instanceof Map||s instanceof WeakMap)&&s instanceof O'
    r'bject&&"get"in s&&s.get instanceof Function?s:{value:s,enumerable:!1,configurable:!0,wr'
    r'itable:!0},Object.defineProperty(t.prototype,o,i))},t}function s(t,...e){return functio'
    r'n(...i){return t(...e,...i)}}function*n(t){var e;e=0;for(var i,s=0,n=t,o=n.length;s<o;s'
    r'+=1)i=n[s],yield[e,i],e+=1}function o(t,e=null){var i;return e=e||document,i=[...e.quer'
    r'ySelectorAll(t)],function(){for(var t=[],s=i,n=0,o=s.length;n<o;n+=1){var r=s[n];r!==e&'
    r'&t.push(r)}return t}.call(this)}function r(t,e){return function(){for(var i=[],s=t.pare'
    r'ntElement.children,n=0,o=s.length;n<o;n+=1){var r=s[n];r===t||e&&!r.matches(e)||i.push('
    r'r)}return i}.call(this)}function l(t){var i,s;return i=e.exec,s=i.call(e,t.getAttribute'
    r'("transform"))||[],function(){for(var t=[],e=s.slice(1),i=0,n=e.length;i<n;i+=1){var o='
    r'e[i];t.push(Number.parseInt(o))}return t}.call(this)}i(t={}),e=new RegExp("translate\\('
    r'(\\d+)[ ,]+(\\d+)\\)");class a{constructor(t,e){var i;this._chartNode=t,e.no_prefix?thi'
    r's._config=e:(i=t.id.replace("chart-",""),this._config=e[i]),this._tooltipElement=o(".to'
    r'oltip",t)[0],this._setConverters(),this._setTooltipTriggerListeners(),this._setTooltipL'
    r'isteners(),this._setGraphListeners(),this._setNodeListeners()}_setConverters(){var t,e,'
    r'i,s;(s=o("svg",this._chartNode)).length?(i=s[0].parentElement,e=s[0].viewBox.baseVal,t='
    r'i.getBBox(),this._xconvert=i=>(i-e.x)/e.width*t.width,this._yconvert=i=>(i-e.y)/e.heigh'
    r't*t.height):this._xconvert=this._yconvert=t=>t}_onGraphMouseMove(t){!this._tooltipTimeo'
    r'utHandle&&t.target.matches(".background")&&this.hide(1e3)}_setGraphListeners(){o(".grap'
    r'h",this._chartNode)[0].addEventListener("mousemove",this._onGraphMouseMove.bind(this))}'
    r'_onNodeMouseLeave(){this._tooltipTimeoutHandle&&(window.clearTimeout(this._tooltipTimeo'
    r'utHandle),this._tooltipTimeoutHandle=null),this.hide()}_setNodeListeners(){this._chartN'
    r'ode.addEventListener("mouseleave",this._onNodeMouseLeave.bind(this))}_setTooltipTrigger'
    r'Listeners(){for(var t,e=0,i=o(".tooltip-trigger",this._chartNode),n=i.length;e<n;e+=1)('
    r't=i[e]).addEventListener("mouseenter",s(this.show.bind(this),t))}_onTooltipMouseEnter()'
    r'{this._tooltipElement&&this._tooltipElement.classList.remove("active")}_onTooltipMouseL'
    r'eave(){this._tooltipElement&&this._tooltipElement.classList.remove("active")}_setToolti'
    r'pListeners(){this._tooltipElement.addEventListener("mouseenter",this._onTooltipMouseEnt'
    r'er.bind(this)),this._tooltipElement.addEventListener("mouseleave",this._onTooltipMouseL'
    r'eave.bind(this))}_getSerieIndex(t){var e,i,s;for(i=null,e=t,s=[];e&&(s.push(e),!e.class'
    r'List.contains("series"));)e=e.parentElement;if(e)for(var n,o=0,r=e.classList,l=r.length'
    r';o<l;o+=1)if((n=r[o]).startsWith("serie-")){i=Number.parseInt(n.replace("serie-",""));b'
    r'reak}return i}_createTextGroup(t,e){var i,s,n,r,l,a,h,d,c;(h=o("g.text",this._tooltipEl'
    r'ement)[0]).innerHTML="",n=0,d={};for(var _,u=0,p=t,v=p.length;u<v;u+=1)_=p[u],[r,l]=_,r'
    r'&&((a=document.createElementNS(this.svg_ns,"text")).textContent=r,a.setAttribute("x",th'
    r'is.padding),a.setAttribute("dy",n),a.classList.add(l.startsWith("value")?"value":l),l.s'
    r'tartsWith("value")&&this._config.tooltip_fancy_mode&&a.classList.add(`color-${e}`),"xli'
    r'nk"===l?((i=document.createElementNS(this.svg_ns,"a")).setAttributeNS(this.xlink_ns,"hr'
    r'ef",r),i.textContent="",i.appendChild(a),a.textContent="Link >",h.appendChild(i)):h.app'
    r'endChild(a),n+=a.getBBox().height+this.padding/2,s=this.padding,a.style.dominantBaselin'
    r'e?a.style.dominantBaseline="text-before-edge":s+=.8*a.getBBox().height,a.setAttribute("'
    r'y",s),d[l]=a);return c=h.getBBox().width+2*this.padding,d.value&&d.value.setAttribute("'
    r'dx",(c-d.value.getBBox().width)/2-this.padding),d.x_label&&d.x_label.setAttribute("dx",'
    r'c-d.x_label.getBBox().width-2*this.padding),d.xlink&&d.xlink.setAttribute("dx",c-d.xlin'
    r'k.getBBox().width-2*this.padding),h}_constrainTooltip(t,e,i,s){var n,o;return[n,o]=l(th'
    r'is._tooltipElement.parentElement),t+i+n>this._config.width&&(t=this._config.width-i-n),'
    r'e+s+o>this._config.height&&(e=this._config.height-s-o),t+n<0&&(t=-n),e+o<0&&(e=-o),[t,e'
    r']}_getTooltipCoordinates(t,e,i){var s,n,o,l;return n=r(t,".x")[0],l=r(t,".y")[0],s=Numb'
    r'er.parseInt(n.textContent),n.classList.contains("centered")?s-=e/2:n.classList.contains'
    r'("left")?s-=e:n.classList.contains("auto")&&(s=this._xconvert(t.getBBox().x+t.getBBox()'
    r'.width/2)-e/2),o=Number.parseInt(l.textContent),l.classList.contains("centered")?o-=i/2'
    r':l.classList.contains("top")?o-=i:l.classList.contains("auto")&&(o=this._yconvert(t.get'
    r'BBox().y+t.getBBox().height/2)-i/2),this._constrainTooltip(s,o,e,i)}_getTooltipKeyMap(t'
    r',e){var i,s,o,l,a,h,d,c;s=[[(o=r(t,".label")).length?o[0].textContent:"","label"]];for('
    r'var _,u=0,p=[...n(r(t,".value")[0].textContent.split("\n"))],v=p.length;u<v;u+=1)_=p[u]'
    r',[i,l]=_,s.push([l,`value-${i}`]);return d=(c=r(t,".xlink")).length?c[0].textContent:""'
    r',a=(h=r(t,".x_label")).length?h[0].textContent:"",this._config.tooltip_fancy_mode&&(s.p'
    r'ush([d,"xlink"]),s.unshift([a,"x_label"]),s.unshift([e,"legend"])),s}show(t){var e,i,s,'
    r'n,r,a,h,d,c,_,u;window.clearTimeout(this._tooltipTimeoutHandle),this._tooltipTimeoutHan'
    r'dle=null,this._tooltipElement.style.opacity=1,this._tooltipElement.style.display="",r=n'
    r'ull,(h=this._getSerieIndex(t))&&(r=this._config.legends[h]),n=this._getTooltipKeyMap(t,'
    r'r),c=(d=this._createTextGroup(n,h)).getBBox().width+2*this.padding,s=d.getBBox().height'
    r'+2*this.padding,(a=o("rect",this._tooltipElement)[0]).setAttribute("width",c),a.setAttr'
    r'ibute("height",s),[_,u]=this._getTooltipCoordinates(t,c,s),[e,i]=l(this._tooltipElement'
    r'),e===_&&i===u||this._tooltipElement.setAttribute("transform",`translate(${_} ${u})`)}_'
    r'hideDelayed(){this._tooltipElement.style.display="none",this._tooltipElement.style.opac'
    r'ity=0,this._tooltipElement.classList.remove("active"),this._tooltipTimeoutHandle=null}h'
    r'ide(t=0){this._tooltipTimeoutHandle=window.setTimeout(this._hideDelayed.bind(this),t)}}'
    r't.set_properties(a,{_chartNode:null,_config:null,_tooltipElement:null,_tooltipTimeoutHa'
    r'ndle:null,_xconvert:null,_yconvert:null,padding:5,svg_ns:"http://www.w3.org/2000/svg",x'
    r'link_ns:"http://www.w3.org/1999/xlink"});class h{constructor(t){this._node=t,this._setA'
    r'ctiveSerieListeners()}_onActiveSerieMouseEnter(t){for(var e=0,i=(s=o(`.serie-${t} .reac'
    r'tive`,this._node)).length;e<i;e+=1)s[e].classList.add("active");var s;for(e=0,i=(s=o(`.'
    r'serie-${t} .showable`,this._node)).length;e<i;e+=1)s[e].classList.add("shown")}_onActiv'
    r'eSerieMouseLeave(t){for(var e=0,i=(s=o(`.serie-${t} .reactive`,this._node)).length;e<i;'
    r'e+=1)s[e].classList.remove("active");var s;for(e=0,i=(s=o(`.serie-${t} .showable`,this.'
    r'_node)).length;e<i;e+=1)s[e].classList.remove("shown")}_isSerieVisible(t){return!o(`#ac'
    r'tivate-serie-${t} rect`,this._node)[0].style.fill}_setSerieVisible(t,e){o(`#activate-se'
    r'rie-${t} rect`,this._node)[0].style.fill=e?"":"transparent";for(var i=0,s=(n=o(`.serie-'
    r'${t} .reactive`,this._node)).length;i<s;i+=1)n[i].style.display=e?"":"none";var n;for(i'
    r'=0,s=(n=o(`.text-overlay .serie-${t}`,this._node)).length;i<s;i+=1)n[i].style.display=e'
    r'?"":"none"}_onActiveSerieClick(t,e){var i,s;if(s=!this._isSerieVisible(t),this._setSeri'
    r'eVisible(t,s),2===e.detail){i=!0;for(var n=0,o=this._serie_count;n<o;n+=1)n!==t&&(i=i&&'
    r'!this._isSerieVisible(n));this._setSerieVisible(t,!0);for(n=0,o=this._serie_count;n<o;n'
    r'+=1)n!==t&&this._setSerieVisible(n,i)}}_setActiveSerieListeners(){for(var t,e,i=0,n=o("'
    r'.activate-serie",this._node),r=n.length;i<r;i+=1)e=n[i],t=Number.parseInt(e.id.replace('
    r'"activate-serie-","")),e.addEventListener("mouseenter",s(this._onActiveSerieMouseEnter.'
    r'bind(this),t)),e.addEventListener("mouseleave",s(this._onActiveSerieMouseLeave.bind(thi'
    r's),t)),e.addEventListener("click",s(this._onActiveSerieClick.bind(this),t));this._serie'
    r'_count=t+1}}function d(){if(!window.pygal.config)throw new Error("No config defined");f'
    r'or(var t,e=0,i=o(".pygal-chart"),s=i.length;e<s;e+=1)t=i[e],new h(t),new a(t,window.pyg'
    r'al.config)}t.set_properties(h,{_node:null,_serie_count:0}),"loading"!==document.readySt'
    r'ate?d():document.addEventListener("DOMContentLoaded",d);'
)
