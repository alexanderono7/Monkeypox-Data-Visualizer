function _1(md){return(
md`# Versor Dragging (earlier version)

See https://observablehq.com/@d3/versor-dragging#note

See also Jason Davies’ [Rotate the World](https://www.jasondavies.com/maps/rotate/).`
)}

function _projectionName(html){return(
html`<select>
  <option value="geoOrthographic">Orthographic</option>
  <option value="geoMercator">Mercator</option>
  <option value="geoNaturalEarth1">Natural Earth</option>
</select>`
)}

function _chart(DOM,width,height,d3,projection,sphere,drag,land110,land50)
{
  const context = DOM.context2d(width, height);
  const path = d3.geoPath(projection, context);

  function render(land) {
    context.clearRect(0, 0, width, height);
    context.beginPath(), path(sphere), context.fillStyle = "#fff", context.fill();
    context.beginPath(), path(land), context.fillStyle = "#000", context.fill();
    context.beginPath(), path(sphere), context.stroke();
  }

  return d3.select(context.canvas)
    .call(drag(projection)
        .on("drag.render", () => render(land110))
        .on("end.render", () => render(land50)))
    .call(() => render(land50))
    .node();
}


function _drag(versor,d3){return(
function drag(projection) {
  let v0, q0, r0;
  
  function dragstarted() {
    v0 = versor.cartesian(projection.invert([d3.event.x, d3.event.y]));
    q0 = versor(r0 = projection.rotate());
  }
  
  function dragged() {
    const v1 = versor.cartesian(projection.rotate(r0).invert([d3.event.x, d3.event.y]));
    const q1 = versor.multiply(q0, versor.delta(v0, v1));
    projection.rotate(versor.rotation(q1));
  }
  
  return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged);
}
)}

function _projection(d3,projectionName){return(
d3[projectionName]().precision(0.1)
)}

function _height(d3,projection,width,sphere)
{
  const [[x0, y0], [x1, y1]] = d3.geoPath(projection.fitWidth(width, sphere)).bounds(sphere);
  const dy = Math.ceil(y1 - y0), l = Math.min(Math.ceil(x1 - x0), dy);
  projection.scale(projection.scale() * (l - 1) / l).precision(0.2);
  return dy;
}


function _sphere(){return(
{type: "Sphere"}
)}

function _land50(FileAttachment,topojson){return(
FileAttachment("land-50m.json").json().then(world => topojson.feature(world, world.objects.land))
)}

function _land110(FileAttachment,topojson){return(
FileAttachment("land-110m.json").json().then(world => topojson.feature(world, world.objects.land))
)}

function _versor(require){return(
require("versor@0.0.3")
)}

function _topojson(require){return(
require("topojson-client@3")
)}

function _d3(require){return(
require("d3@5")
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  function toString() { return this.url; }
  const fileAttachments = new Map([
    ["land-50m.json", {url: new URL("./files/efcaaf9f0b260e09b6afeaee6dbc1b91ad45f3328561cd67eb16a1754096c1095f70d284acdc4b004910e89265b60eba2706334e0dc84ded38fd9209083d4cef.json", import.meta.url), mimeType: "application/json", toString}],
    ["land-110m.json", {url: new URL("./files/eec657afeffb70691657f56f78ce546cc20861c628c4272d902fb7ff94d07a73737fd5356d255cef2a092de8322c56bbbc4f0f6a3c0c12864101f37ec6da9321.json", import.meta.url), mimeType: "application/json", toString}]
  ]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("viewof projectionName")).define("viewof projectionName", ["html"], _projectionName);
  main.variable(observer("projectionName")).define("projectionName", ["Generators", "viewof projectionName"], (G, _) => G.input(_));
  main.variable(observer("chart")).define("chart", ["DOM","width","height","d3","projection","sphere","drag","land110","land50"], _chart);
  main.variable(observer("drag")).define("drag", ["versor","d3"], _drag);
  main.variable(observer("projection")).define("projection", ["d3","projectionName"], _projection);
  main.variable(observer("height")).define("height", ["d3","projection","width","sphere"], _height);
  main.variable(observer("sphere")).define("sphere", _sphere);
  main.variable(observer("land50")).define("land50", ["FileAttachment","topojson"], _land50);
  main.variable(observer("land110")).define("land110", ["FileAttachment","topojson"], _land110);
  main.variable(observer("versor")).define("versor", ["require"], _versor);
  main.variable(observer("topojson")).define("topojson", ["require"], _topojson);
  main.variable(observer("d3")).define("d3", ["require"], _d3);
  return main;
}
